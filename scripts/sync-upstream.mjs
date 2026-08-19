#!/usr/bin/env node
// Sync vendored third-party skills declared in UPSTREAM.json.
//
//   node scripts/sync-upstream.mjs check   # report drift, exit 1 if any
//   node scripts/sync-upstream.mjs apply   # re-vendor and update the manifest
//
// No dependencies. Requires `git` on PATH.

import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync, cpSync, readFileSync, writeFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const MANIFEST = join(ROOT, 'UPSTREAM.json');

const mode = process.argv[2];
if (mode !== 'check' && mode !== 'apply') {
  console.error('usage: node scripts/sync-upstream.mjs <check|apply>');
  process.exit(2);
}

const git = (args, cwd) =>
  execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();

// Windows path separators -> POSIX, so output and comparisons are platform-stable.
const toPosix = (p) => p.split(sep).join('/');

// Recursively list files under `p` as POSIX paths relative to `base`.
function listFiles(p, base = p, out = []) {
  if (!existsSync(p)) return out;
  if (statSync(p).isFile()) {
    out.push(toPosix(relative(base, p)));
    return out;
  }
  for (const entry of readdirSync(p).sort()) listFiles(join(p, entry), base, out);
  return out;
}

// Compare a vendored path against the freshly cloned upstream path.
// Line endings are normalised so Windows checkouts do not report phantom drift.
const CRLF = new RegExp(String.fromCharCode(13) + String.fromCharCode(10), 'g');
const readNormalised = (f) => readFileSync(f, 'utf8').replace(CRLF, String.fromCharCode(10));

function diffPath(upstreamPath, localPath) {
  const changes = [];
  const upstreamIsFile = statSync(upstreamPath).isFile();
  const upstreamFiles = upstreamIsFile ? [''] : listFiles(upstreamPath);
  const localFiles = upstreamIsFile ? (existsSync(localPath) ? [''] : []) : listFiles(localPath);

  for (const rel of upstreamFiles) {
    const u = rel ? join(upstreamPath, rel) : upstreamPath;
    const l = rel ? join(localPath, rel) : localPath;
    if (!existsSync(l)) changes.push(`  + ${toPosix(relative(ROOT, l))} (new upstream)`);
    else if (readNormalised(u) !== readNormalised(l)) changes.push(`  ~ ${toPosix(relative(ROOT, l))} (content differs)`);
  }
  for (const rel of localFiles) {
    if (!upstreamFiles.includes(rel)) {
      const l = rel ? join(localPath, rel) : localPath;
      changes.push(`  - ${toPosix(relative(ROOT, l))} (removed upstream)`);
    }
  }
  return changes;
}

const manifest = JSON.parse(readFileSync(MANIFEST, 'utf8'));
let drifted = false;

for (const src of manifest.sources) {
  const tmp = mkdtempSync(join(tmpdir(), `upstream-${src.plugin}-`));
  try {
    git(['clone', '--quiet', '--depth', '1', '--branch', src.ref, src.url, tmp]);
    const head = git(['rev-parse', 'HEAD'], tmp);
    const commitMoved = head !== src.commit;

    console.log(`\n${src.plugin}  <-  ${src.url}@${src.ref}`);
    console.log(`  pinned ${src.commit.slice(0, 12)}  upstream ${head.slice(0, 12)}` +
      (commitMoved ? '  (MOVED)' : '  (up to date)'));

    const changes = [];
    for (const m of src.map) {
      const upstreamPath = join(tmp, m.from);
      if (!existsSync(upstreamPath)) {
        changes.push(`  ! ${m.from} missing upstream -- update the map in UPSTREAM.json`);
        continue;
      }
      changes.push(...diffPath(upstreamPath, join(ROOT, m.to)));
    }

    if (changes.length === 0) {
      console.log('  no file drift');
      if (commitMoved && mode === 'apply') {
        src.commit = head;
        console.log('  manifest commit re-pinned (no content change)');
      }
      continue;
    }

    drifted = true;
    console.log(changes.join('\n'));

    if (mode === 'apply') {
      for (const m of src.map) {
        const upstreamPath = join(tmp, m.from);
        if (!existsSync(upstreamPath)) continue;
        const dest = join(ROOT, m.to);
        rmSync(dest, { recursive: true, force: true });
        cpSync(upstreamPath, dest, { recursive: true });
      }
      src.commit = head;
      src.vendoredAt = new Date().toISOString().slice(0, 10);
      console.log('  re-vendored');
    }
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

if (mode === 'apply') {
  writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + '\n');
  console.log('\nUPSTREAM.json updated. Review the diff before committing.');
  process.exit(0);
}

if (drifted) {
  console.log('\nDrift detected. Run: node scripts/sync-upstream.mjs apply');
  process.exit(1);
}
console.log('\nAll vendored sources match upstream.');
