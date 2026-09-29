# Generates ppk2-wiring.svg — how to wire the Nordic PPK2, the XIAO nRF54L15 and
# the 802030 cell for the tea light's current measurement. Two panels:
#   A. Source meter  — PPK2 *is* the battery (do this first; cleanest numbers)
#   B. Ampere meter  — PPK2 in series with the real cell
W, H = 1240, 960
o = []
def a(s): o.append(s)
RED, BLK, GRN, BLU, ORG, PUR, GRY = "#c62828", "#222", "#2e7d32", "#1565c0", "#ef6c00", "#6a1b9a", "#666"
def text(x, y, s, size=12, anchor="start", c=BLK, w="normal"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{c}" font-weight="{w}">{s}</text>')
def line(pts, c=BLK, w=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    a(f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{d}/>')
def box(x, y, w, h, fill, stroke=BLK, rx=6, sw=2):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def dot(x, y, c=BLK): a(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
def pin(x, y, label, side="r", c=BLK):
    dot(x, y, c); text(x + (8 if side == "r" else -8), y + 4, label, 11, "start" if side == "r" else "end", c, "bold")

a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
text(20, 34, "Tea light current measurement — PPK2 + XIAO nRF54L15 + 802030 cell", 20, "start", BLK, "bold")
text(20, 56, "XIAO USB-C must be UNPLUGGED in both setups: it powers the onboard debugger and runs the charger, which swamps the reading.", 12, "start", RED, "bold")

def ppk2(x, y, vin_left=False):
    box(x, y, 210, 150, "#e8f0fe")
    text(x + 105, y + 22, "Nordic PPK2", 14, "middle", BLK, "bold")
    text(x + 105, y + 40, "micro-USB → laptop (Power Profiler app)", 10, "middle", GRY)
    if vin_left: pin(x, y + 100, "VIN", "l", ORG); vin = (x, y + 100)
    else:        pin(x + 210, y + 70, "VIN", "r", ORG); vin = (x + 210, y + 70)
    pin(x + 210, y + 100, "VOUT", "r", RED); pin(x + 210, y + 130, "GND", "r", BLK)
    return vin, (x + 210, y + 100), (x + 210, y + 130)

def xiao(x, y, usb_note=True):
    box(x, y, 200, 150, "#e3f2fd")
    text(x + 100, y + 22, "XIAO nRF54L15", 14, "middle", BLK, "bold")
    text(x + 100, y + 40, "battery pads on the underside", 10, "middle", GRY)
    pin(x, y + 100, "BAT+", "l", RED); pin(x, y + 130, "BAT−", "l", BLK)
    box(x + 70, y + 118, 60, 22, "#fff", GRY, 4, 1.5); text(x + 100, y + 112, "USB-C", 10, "middle", GRY)
    if usb_note:
        line([(x + 74, y + 120), (x + 126, y + 138)], RED, 3); line([(x + 74, y + 138), (x + 126, y + 120)], RED, 3)
        text(x + 100, y + 68, "USB unplugged", 11, "middle", RED, "bold")
    return (x, y + 100), (x, y + 130)

def cell(x, y):
    box(x, y, 130, 70, "#fff3e0")
    text(x + 65, y + 20, "802030 LiPo", 13, "middle", BLK, "bold"); text(x + 65, y + 35, "3.7 V 400 mAh, PCM", 10, "middle", GRY)
    text(x + 122, y + 60, "+ red", 10, "end", RED, "bold"); text(x + 8, y + 60, "− blk", 10, "start", BLK, "bold")
    dot(x + 130, y + 50, RED); dot(x, y + 50, BLK)
    return (x + 130, y + 50), (x, y + 50)

# ---------------- Panel A: source meter ----------------
ay = 90
box(20, ay, W - 40, 300, "#fafafa", GRY, 8, 1.5)
text(36, ay + 26, "A.  Source-meter mode — PPK2 replaces the battery  (do this first)", 15, "start", BLK, "bold")
vin, vout, gnd = ppk2(120, ay + 70)
bp, bm = xiao(760, ay + 70)
line([vout, (520, vout[1]), (520, bp[1]), bp], RED, 3); text(520, bp[1] - 10, "VOUT → BAT+", 11, "middle", RED, "bold")
line([gnd, (560, gnd[1]), (560, bm[1]), bm], BLK, 3); text(560, bm[1] + 18, "GND → BAT−", 11, "middle", BLK, "bold")
text(vin[0] + 60, vin[1] + 4, "(VIN unused)", 10, "start", GRY)
sa = ["App: Source meter · Supply 3700 mV · Enable power",
      "Sampling 100 kHz · record ≥ 5 min idle, then ≥ 5 min with the light on",
      "Read the AVERAGE over the window — the spikes are the 1 s polls"]
for i, s in enumerate(sa): text(36, ay + 230 + i * 20, s, 12, "start", BLU)

# ---------------- Panel B: ampere meter ----------------
by = 410
box(20, by, W - 40, 380, "#fafafa", GRY, 8, 1.5)
text(36, by + 26, "B.  Ampere-meter mode — PPK2 in series with the real cell", 15, "start", BLK, "bold")
cp, cm = cell(60, by + 120)                     # cell on the left; + pin lands on VIN's y
vin, vout, gnd = ppk2(300, by + 70, vin_left=True)
bp, bm = xiao(800, by + 70)
# cell + → VIN (straight across)
line([cp, vin], ORG, 3); text((cp[0] + vin[0]) / 2, vin[1] - 10, "cell + → VIN", 11, "middle", ORG, "bold")
# VOUT → BAT+
line([vout, (650, vout[1]), (650, bp[1]), bp], RED, 3); text(650, bp[1] - 10, "VOUT → BAT+", 11, "middle", RED, "bold")
# common ground bus along the bottom of the panel
gy = by + 300
line([cm, (36, cm[1]), (36, gy), (800, gy)], BLK, 3)          # cell − → bus → XIAO BAT−
line([(800, gy), bm], BLK, 3)
line([gnd, (690, gnd[1]), (690, gy)], BLK, 3); dot(690, gy)    # PPK2 GND → bus
text(420, gy - 8, "cell −  →  PPK2 GND  →  XIAO BAT−   (one common ground)", 11, "middle", BLK, "bold")
sb = ["App: Ampere meter · Enable power   (PPK2 passes the cell straight through and only measures)",
      "Same recording as A. Any difference from A is the cell's own ESR/leakage — expect it to be tiny."]
for i, s_ in enumerate(sb): text(36, by + 330 + i * 20, s_, 12, "start", BLU)

# ---------------- notes ----------------
ny = 812
notes = [("Before you start", True),
 ("• Polarity: the JST-PH on Chinese pouch cells is NOT standardised — verify red = + with a meter before touching the XIAO's pads. Reversed = dead board.", False),
 ("• Solder the cell's leads to the BAT+ / BAT− pads (or a 2-pin header on them); the XIAO's charger then handles it over USB when you are not measuring.", False),
 ("• Keep the debug probe's USB out for the whole recording. If you need the serial console, take it BEFORE, then unplug and let it settle 2 min.", False),
 ("• What to expect: a flat floor in the tens of µA with a ~10 mA spike every second (the ICD poll). The floor × time is your standby life.", False)]
for i, (s, b) in enumerate(notes): text(36, ny + 8 + i * 22, s, 13 if b else 11, "start", BLK, "bold" if b else "normal")

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">' + "".join(o) + "</svg>"
open("ppk2-wiring.svg", "w").write(svg); print("svg ok")
