# Body — 3D-printed parts

`tealight.scad` is the source (parametric; every dimension at the top).
Three parts:

| Part | Material | Notes |
|---|---|---|
| `cup.stl` | opaque PETG | battery, perfboard ledge tabs, XIAO, USB-C notch (+x), Ø4 button hole in the floor |
| `carrier.stl` | opaque PETG | 4.5 mm spacer on the perfboard that carries the 32 mm LED ring; cut away over the XIAO |
| `cap.stl` | translucent PETG | diffuser, 2 mm plug skirt into the cup, notched for the USB-C |

Total height 23.0 mm, Ø38. Stack: floor 1 · cell 8.5 · perf 1.6 · XIAO 4 ·
ring 3.5 · headroom 2.9 · top 1.

Render: `openscad -D 'part="cup"' -o cup.stl tealight.scad` (same for
`carrier`, `cap`; `part="all"` with `exploded=true` for a preview).
`preview.py` is a manifold3d port used to produce the STLs and
`preview.png` where OpenSCAD isn't available; keep it in sync with the .scad.

**Untested — first print is a fit test.** Things to check on it: the 802030
cell's corners against the Ø36 bore, the USB-C notch height (12–15.5 mm)
against the real XIAO on the perfboard, and the cap's plug fit (0.2 mm
clearance; PETG usually wants 0.2–0.3).
