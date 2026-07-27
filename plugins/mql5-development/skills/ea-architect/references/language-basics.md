# Language Foundations

## BA-1: Types, Variables, Scope, and Namespaces

**Source families:** `basis.md`, `basis-syntax*.md`, `basis-types*.md`, `basis-variables*.md`, `basis-namespace.md`

| Area | What to keep straight | EA design consequence |
|------|----------------------|----------------------|
| Syntax and identifiers | Reserved words, identifier rules, comments, namespaces | Keep module names and public API names stable so include files remain predictable |
| Scalar and structured types | Integer family, `bool`, `color`, `datetime`, `double`, `complex`, strings, enums, `typedef`, casts, `this` | Choose explicit types for prices, timestamps, flags, and enum-driven state instead of loose numeric reuse |
| Variable classes | Global, local, static, input, extern, formal parameters | Put configuration in `input`, durable module state in members/statics only when required, transient calculations in locals |
| Scope rules | Declaration order controls initialisation order; narrower blocks create narrower lifetime | Keep mutable state close to the event handler or module that owns it |

**Lifetime rules:**
- Global and static variables initialised when the program loads, in declaration order
- Automatic locals initialised only when execution reaches their declaration
- Deinitialisation runs in reverse order for automatically managed objects
- Namespaces and `typedef` aliases help keep multi-module EA code readable

**Architectural guidance:**
- Prefer enums and named types over raw literals for trade state, regime labels, and execution modes
- Use `input` variables only for user-facing knobs; do not let business logic depend on mutable globals spread across files
- Keep symbol, timeframe, and broker-specific values derived at runtime instead of cached as magic numbers

---

## BA-2: Expressions, Operators, and Control Flow

**Source families:** `basis-operations*.md`, `basis-operators*.md`

| Operator family | MQL5 detail | Usage pattern |
|----------------|-------------|---------------|
| Assignment and compound assignment | Standard assignment plus compound forms | Use for concise state updates, but avoid chaining when debugging order logic |
| Boolean and relational operators | Standard comparisons with precedence rules | Parenthesise mixed conditions in entry filters instead of relying on precedence memory |
| Bitwise operators | Needed for flag-style enums and masks | Use for property and permission flags; document the mask being tested |
| Ternary operator | Compact conditional expression | Fine for small value selection, not for branching trade workflows |
| `new` / `delete` | Dynamic object lifecycle hooks | Use only when object lifetime must outlive the current block |
| Matrix multiplication | `@` and matrix/vector methods support linear algebra | Useful for portfolio math, covariance work, or feature transforms without nested loops |

**Control-flow rules:**
- `if`/`switch` should branch on already-computed intent, not recompute indicator state repeatedly
- `for`, `while`, and `do while` loops are valid, but event-driven EAs should keep loops bounded and explicit
- `break`, `continue`, and `return` should make failure or skip paths obvious in order scans

**Gotchas:**
- Operator precedence is easy to misread in long signal conditions; add parentheses on purpose
- Bitwise logic matters whenever a property exposes multiple allowed flags, not just one enum value
- Use matrix/vector support when the problem is algebraic; avoid rebuilding NumPy-like behaviour with raw arrays unless necessary

---

## BA-3: Functions, Parameter Passing, Overloads

**Source families:** `basis-function*.md`

| Topic | Rule | Practical consequence |
|-------|------|----------------------|
| Pass by value | Scalars can be copied into the callee | Safe for small immutable inputs like thresholds and counters |
| Pass by reference | Arrays, structures, and class objects are always passed by reference | Use `const` aggressively when helpers should read but not mutate caller-owned data |
| Parameter evaluation | Arguments are calculated in reverse order | Do not hide side effects like `i++` inside function-call arguments |
| Function overloading | Resolution depends on signature | Keep overload sets narrow and explicit to avoid ambiguous API surfaces |
| Operator overloading | Supported for custom types | Use sparingly for domain containers, not to make trade logic opaque |
| External and exported functions | `#import` and `export` define boundaries to DLLs or external use | Isolate these calls so the rest of the EA remains testable |

**Architectural guidance:**
- Treat helper functions as pure whenever possible: pass inputs, return results, avoid mutating unrelated state
- Use reference parameters for large or structured data intentionally, not accidentally
- Keep event handlers thin and delegate into named module methods

**Named gotcha:**
- Reverse argument evaluation means expressions like `func(a[i], a[i++])` are not safe shorthand. Compute side-effecting values first, then call the function.

---

## BA-4: Object-Oriented Design, Virtual Dispatch, and Templates

**Source families:** `basis-oop*.md`

| OOP feature | MQL5 use | EA architecture use |
|-------------|----------|---------------------|
| Encapsulation | `private`, `protected`, `public` state and methods | Keep risk, signal, and trade state owned by their respective modules |
| Inheritance | Shared base behaviour with specialisation | Good for base engines, reusable filters, and common trade helpers |
| Virtual functions and polymorphism | Runtime dispatch across derived classes | Use when you want interchangeable signal or money-management implementations behind one interface |
| Abstract types | Contract-first design | Useful for base module interfaces and strategy hooks |
| Static members | Class-level shared data | Reserve for counters, registries, or constants that truly span instances |
| Function and class templates | Compiler generates concrete implementations per type | Useful for reusable containers, safe arrays, and math helpers across `double`, `int`, `datetime`, or structs |

**Template guidance:**
- Templates remove repetitive overload boilerplate when behaviour is identical across types
- Class templates are a good fit for containers and utility wrappers
- Do not template business logic prematurely; template the infrastructure around it

**Polymorphism guidance:**
- Prefer interfaces and virtual methods when the strategy must swap implementations at runtime
- Prefer templates when behaviour is fixed at compile time and only the data type changes

---

## BA-5: Memory Model, Object Descriptors, Dynamic Arrays, and Matrix/Vector Types

**Source families:** `basis-types-object_pointers.md`, `basis-types-dynamic_array.md`, `basis-types-matrix_vector.md`, `basis-variables-object_live.md`

| Area | Key rule | EA consequence |
|------|----------|----------------|
| Object descriptors | Pointer-like syntax refers to descriptors, not raw addresses | Think ownership and validity, not manual pointer arithmetic |
| Pointer safety | `CheckPointer()` should guard dynamic-object use | Validate before dereferencing objects that may be null or deleted |
| Dynamic objects | Objects created with `new` should be removed with `delete` | Delete long-lived dynamic helpers explicitly instead of relying on unload cleanup |
| Automatic objects | Locals/global objects initialise automatically by scope rules | Prefer automatic lifetime unless the object must survive outside the current block |
| Dynamic arrays | Resize and release deliberately | Avoid repeated unnecessary reallocation in hot paths |
| Matrix/vector types | Native `matrix`, `vector`, and related methods mirror many NumPy-style operations | Use built-in math structures for portfolio, correlation, and model features instead of hand-rolled nested loops |

**Lifecycle rules:**
- Constructors fire when automatic objects are initialised or when `new` executes
- Destructors fire when automatic objects leave scope or when `delete` runs
- Undeleted dynamic objects are reported in the Experts journal during unload
- Memory used by dynamic arrays is returned immediately; class-object memory is returned to the class pool

**Named gotcha:**
- A descriptor can become invalid after `delete`; treat `CheckPointer()` as a guardrail, not optional ceremony

---

## BA-6: Preprocessor, Imports, Includes, and Build-Time Configuration

**Source families:** `basis-preprosessor*.md`

| Directive area | What it does | Recommended use |
|----------------|--------------|----------------|
| `#include` | Pulls shared headers into the current translation unit | Centralise module interfaces and shared constants in `.mqh` files |
| `#import` | Declares external functions | Keep DLL boundaries isolated and well documented |
| `#define` and constant macros | Names compile-time constants and helpers | Use for compile-time switches and small utility macros, not as a replacement for typed constants everywhere |
| Conditional compilation | `#ifdef`, `#ifndef`, `#else`, `#endif` | Gate debug instrumentation, alternate integrations, or broker-specific shims |
| Compilation-mode macros | `__MQL5__`, `__MQL4__`, `_DEBUG`, `_RELEASE` | Use to keep diagnostics and compatibility code explicit |

**Guidelines:**
- One directive per line; if a directive is long, continue it with `\`
- Use conditional compilation to isolate debug-only logging and experimental paths
- Keep runtime branching separate from build-time branching so the final EA is easier to reason about

---

## References

- `docs/mql5_com_-_docs/basis.md`
- `docs/mql5_com_-_docs/basis-syntax*.md`
- `docs/mql5_com_-_docs/basis-types*.md`
- `docs/mql5_com_-_docs/basis-variables*.md`
- `docs/mql5_com_-_docs/basis-operations*.md`
- `docs/mql5_com_-_docs/basis-operators*.md`
- `docs/mql5_com_-_docs/basis-function*.md`
- `docs/mql5_com_-_docs/basis-oop*.md`
- `docs/mql5_com_-_docs/basis-preprosessor*.md`
- `docs/mql5_com_-_docs/basis-namespace.md`
