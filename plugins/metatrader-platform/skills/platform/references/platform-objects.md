# Platform Objects — Analytical and Graphical Drawing Workflow

This reference covers the terminal UI for drawing and editing chart objects,
not the MQL5 `ObjectCreate` / `ObjectSet*` API surface (see
`object-api.md`). The platform groups objects into families.

---

## Object Families

| Family | What traders use it for |
|--------|------------------------|
| Arrows and lines | Mark entries, levels, trend direction, and cycle structure |
| Channels | Visualise trend envelopes, pitchforks, regressions, and deviation bands |
| Fibonacci and Gann | Project retracement, extension, fan, grid, and time relationships |
| Elliott | Annotate wave counts and theory-guided structure |
| Shapes | Highlight regions, scenarios, and discretionary markup |
| Graphical widgets | Add labels, text, buttons, charts, bitmaps, and simple chart-embedded UI controls |

---

## UI Distinctions That Matter

- Some graphical objects are chart-anchored and move with the chart; others
  are window-anchored and stay fixed while the chart scrolls
- The chart object list and analysis pages are the operational entry points
  when a user needs to inspect, organise, or remove drawn objects
- Use this reference for platform drawing workflow questions; use the
  `object-api.md` reference or MQL5 skills for programmatic object
  manipulation

---

## References

- `docs/metatrader5_com_-_terminal_help/charts_analysis-objects.md`
- `docs/metatrader5_com_-_terminal_help/objects-arrows.md`
- `docs/metatrader5_com_-_terminal_help/objects-channels.md`
- `docs/metatrader5_com_-_terminal_help/objects-channels-andrews_pitchfork.md`
- `docs/metatrader5_com_-_terminal_help/objects-channels-equidistant_channel.md`
- `docs/metatrader5_com_-_terminal_help/objects-channels-regression_channel.md`
- `docs/metatrader5_com_-_terminal_help/objects-channels-stddev_channel.md`
- `docs/metatrader5_com_-_terminal_help/objects-elliott.md`
- `docs/metatrader5_com_-_terminal_help/objects-elliott-elliott_theory.md`
- `docs/metatrader5_com_-_terminal_help/objects-elliott-waves_applying.md`
- `docs/metatrader5_com_-_terminal_help/objects-fibo.md`
- `docs/metatrader5_com_-_terminal_help/objects-fibo-fibo_arcs.md`
- `docs/metatrader5_com_-_terminal_help/objects-fibo-fibo_channel.md`
- `docs/metatrader5_com_-_terminal_help/objects-fibo-fibo_expansion.md`
- `docs/metatrader5_com_-_terminal_help/objects-fibo-fibo_fan.md`
- `docs/metatrader5_com_-_terminal_help/objects-fibo-fibo_retracement.md`
- `docs/metatrader5_com_-_terminal_help/objects-fibo-fibo_timezones.md`
- `docs/metatrader5_com_-_terminal_help/objects-gann.md`
- `docs/metatrader5_com_-_terminal_help/objects-gann-gann_fan.md`
- `docs/metatrader5_com_-_terminal_help/objects-gann-gann_grid.md`
- `docs/metatrader5_com_-_terminal_help/objects-gann-gann_line.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_bitmap.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_bitmap_label.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_button.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_chart.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_edit.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_event.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_rect_label.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_text.md`
- `docs/metatrader5_com_-_terminal_help/objects-graphical_objects-obj_text_label.md`
- `docs/metatrader5_com_-_terminal_help/objects-lines.md`
- `docs/metatrader5_com_-_terminal_help/objects-lines-arrowed_line.md`
- `docs/metatrader5_com_-_terminal_help/objects-lines-cycle_lines.md`
- `docs/metatrader5_com_-_terminal_help/objects-lines-hor_line.md`
- `docs/metatrader5_com_-_terminal_help/objects-lines-trend_line.md`
- `docs/metatrader5_com_-_terminal_help/objects-lines-trend_line_angle.md`
- `docs/metatrader5_com_-_terminal_help/objects-lines-vert_line.md`
- `docs/metatrader5_com_-_terminal_help/objects-shapes.md`
- `docs/metatrader5_com_-_terminal_help/objects-shapes-ellipse.md`
- `docs/metatrader5_com_-_terminal_help/objects-shapes-rectangle.md`
- `docs/metatrader5_com_-_terminal_help/objects-shapes-triangle.md`
