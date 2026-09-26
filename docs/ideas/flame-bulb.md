# Idea: E26 "flame" bulb (Linkind T19 style)

Reference: Linkind Smart Flame bulb — T19 form, Ø57 × 131 mm, E26, 120 V.

Same firmware/HA approach as the tea light (ESPHome, C6; mains-powered so
Wi-Fi is fine — or Thread for consistency), different body:

* **Base:** printed in **PC-FR** (or PC-CF/ABS-FR), carrying an E26 screw
  shell (buy a bulb-repair E26 base) and an **encapsulated, UL-recognised
  AC/DC module** — e.g. Mean Well IRM-10-24 (24 V, 10 W) — so the printed
  part only provides mechanics and spacing, never insulation on its own.
  Creepage ≥ 4 mm between mains and low voltage, strain relief on the
  E26 leads, and the module's own thermal limits respected (a T19 in an
  enclosed outdoor fixture gets hot; PC-FR is good to ~110–120 °C).
* **LEDs:** WS2805 is 24 V RGB + CW + WW (5-in-1, addressable) — matches the
  24 V module directly; a small buck (24 → 5 V) feeds the XIAO. Six vertical
  strip segments (~80 mm, 5 px at 60/m) around a Ø30 printed core, LEDs
  facing out; the XIAO + buck live inside the core.
* **Diffuser:** translucent PETG tube, Ø57, or a frosted acrylic tube.
* **Effects:** ESPHome addressable_flicker per column with a vertical
  brightness gradient (bright at the bottom, dim at the top) reads as flame.

Open questions: heat (LED + PSU in a closed bulb), whether to skip the
AC/DC altogether and make a 24 V DC version for fixtures we control, and
whether it's worth it vs. the $15 Linkind + Matter.
