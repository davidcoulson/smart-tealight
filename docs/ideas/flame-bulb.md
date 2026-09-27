# Idea: E26 "flame" bulb (Linkind T19 style)

Reference: Linkind Smart Flame bulb — T19 form, Ø57 × 131 mm, E26, 120 V.

Same firmware/HA approach as the tea light (ESPHome, C6; mains-powered so
Wi-Fi is fine — or Thread for consistency), different body:

* **Base:** printed in **PC-FR** (or PC-CF/ABS-FR), carrying an E26 screw
  shell (buy a bulb-repair E26 base) and an **encapsulated, UL-recognised
  AC/DC module** (HLK-10M05, see Power) so the printed
  part only provides mechanics and spacing, never insulation on its own.
  Creepage ≥ 4 mm between mains and low voltage, strain relief on the
  E26 leads, and the module's own thermal limits respected (a T19 in an
  enclosed outdoor fixture gets hot; PC-FR is good to ~110–120 °C).
* **LEDs: SK6812 RGBWW, 144/m, 5 V** (RGB + warm-white die, 7 mm pitch).
  Chosen over WS2805 (RGB+CCT) because WS2805 tops out at 60/m — too coarse
  for flicker — and the dense FCOB WS2805 has one IC per 71 mm. Cool white
  isn't needed for a flame. Ten vertical columns of 10 px (the strip is 12 mm wide; a 10-sided
  mast with 12.2 mm facets leaves ~4.5 mm to the diffuser) — 100 px, XIAO
  inside the core. Body in `hardware/flame-bulb/`. Worst-case white
  ~4 A → cap brightness at ~35 % in firmware. Same reel as the tea light's
  strip option.
* **Power:** 5 V from a **Hi-Link HLK-10M05** (5 V 2 A, 47 × 28 × 22 mm,
  ordered 2026-09-26) standing vertically in the base; the XIAO runs from
  5 V directly, no buck. Design point ≤ 1.5 A continuous (the module gets
  hot near 2 A in a closed body), brightness capped in firmware. Add a 1 A
  slow-blow fuse / fusible resistor on the AC input — the module has none.
  470–1000 µF across the 5 V rail; feed the six LED columns from a common
  5 V ring at the base, not daisy-chained.
* **Diffuser:** translucent PETG tube, Ø57, or a frosted acrylic tube.
* **Effects:** ESPHome addressable_flicker per column with a vertical
  brightness gradient (bright at the bottom, dim at the top) reads as flame.

Open questions: heat (LED + PSU in a closed bulb), whether to skip the
AC/DC altogether and make a 24 V DC version for fixtures we control, and
whether it's worth it vs. the $15 Linkind + Matter.

Parts list: [`../flame-bulb-bom.md`](../flame-bulb-bom.md). Exploded assembly: `../flame-bulb-exploded.png`.
