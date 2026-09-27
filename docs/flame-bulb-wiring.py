# Generates flame-bulb-wiring.svg — full electrical diagram of the flame bulb.
W, H = 1240, 860
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

a('<rect width="100%" height="100%" fill="#fff"/>')
text(30, 36, "Flame bulb — wiring", 20, "start", BLK, "bold")
text(30, 58, "E26 → fuse → HLK-10M05 → 5 V rail. XIAO C6 drives D4 through a 74AHCT125 into 10 serpentine columns. 5 V ring at the bottom, GND ring at the top.", 12, "start", GRY)

# ---- mains side ----
box(40, 100, 110, 70, "#eee"); text(95, 128, "E26 plug", 12, "middle", BLK, "bold"); text(95, 146, "pigtail leads", 10, "middle", GRY)
pin(150, 118, "L", "r", RED); pin(150, 152, "N", "r", BLK)
# fuse on L
line([(150, 118), (200, 118)], RED); box(200, 108, 60, 20, "#fff", RED, 4); text(230, 122, "F1 1 A T", 10, "middle", RED, "bold"); line([(260, 118), (330, 118)], RED)
line([(150, 152), (330, 152)], BLK)
text(230, 100, "slow-blow, heat-shrunk", 9, "middle", GRY)
# PSU
box(330, 90, 150, 90, "#2b6cb0", BLK); text(405, 120, "HLK-10M05", 13, "middle", "#fff", "bold"); text(405, 138, "AC 100–240 V → 5 V 2 A", 10, "middle", "#dbeafe"); text(405, 156, "encapsulated, inside the mast", 9, "middle", "#dbeafe")
pin(330, 118, "AC", "l", "#fff"); pin(330, 152, "AC", "l", "#fff")
pin(480, 118, "+Vo", "r", "#fff"); pin(480, 152, "−Vo", "r", "#fff")
a(f'<rect x="30" y="80" width="470" height="110" rx="10" fill="none" stroke="{RED}" stroke-width="1.5" stroke-dasharray="6 4"/>')
text(40, 205, "MAINS — everything in this box lives inside the PC-FR mast/cap. Insulate every joint.", 10, "start", RED, "bold")

# ---- 5 V rail ----
RAIL_Y, GND_Y = 118, 152
line([(480, RAIL_Y), (560, RAIL_Y)], RED, 3); line([(480, GND_Y), (560, GND_Y)], BLK, 3)
# bulk cap
box(560, 100, 26, 70, "#fff", BLK, 3); text(573, 140, "C1", 10, "middle", BLK, "bold"); text(600, 128, "1000 µF", 10, "start"); text(600, 142, "6.3–10 V", 10, "start", GRY)
line([(573, 100), (573, RAIL_Y)], RED, 3); line([(573, 170), (573, GND_Y)], BLK, 3)
text(586, 96, "+", 12, "start", RED, "bold")
# rail continues to the right (to XIAO, shifter, and the ring)
line([(586, RAIL_Y), (700, RAIL_Y), (700, 250)], RED, 3); line([(586, GND_Y), (720, GND_Y), (720, 250)], BLK, 3)
text(640, 110, "5 V rail (22 AWG)", 10, "middle", RED, "bold")

# ---- XIAO ----
box(60, 260, 200, 150, "#e8f0fe", BLU); text(160, 285, "XIAO ESP32-C6", 14, "middle", BLU, "bold"); text(160, 302, "inside the mast bore, above the PSU", 9, "middle", BLU)
pin(260, 330, "5V", "r", RED); pin(260, 360, "GND", "r", BLK); pin(260, 390, "D4 (GPIO22)", "r", GRN)
text(70, 395, "Wi-Fi to HA (mains powered)", 9, "start", GRY)
# ---- level shifter ----
box(400, 300, 170, 110, "#f3e5f5", PUR); text(485, 322, "74AHCT125", 13, "middle", PUR, "bold"); text(485, 338, "one gate of the quad", 9, "middle", PUR)
pin(400, 360, "A1", "l", GRN); pin(400, 390, "/OE1", "l", GRY); pin(570, 360, "Y1", "r", GRN); pin(485, 300, "VCC 5 V", "r", RED); pin(485, 410, "GND", "r", BLK)
text(492, 424, "/OE1 → GND", 9, "start", GRY)
# wires XIAO -> shifter
line([(260, 390), (330, 390), (330, 360), (400, 360)], GRN); line([(400, 390), (380, 390), (380, 440), (485, 440), (485, 410)], GRY)
# power to XIAO & shifter
line([(260, 330), (300, 330), (300, 250), (700, 250)], RED, 2); line([(260, 360), (290, 360), (290, 236), (720, 236), (720, 250)], BLK, 2)
line([(485, 300), (485, 250)], RED, 2); line([(485, 440), (720, 440), (720, 250)], BLK, 2)
# series resistor
line([(570, 360), (600, 360)], GRN); box(600, 352, 40, 16, "#fff", BLK, 3); text(620, 364, "330 Ω", 9, "middle", BLK, "bold"); line([(640, 360), (700, 360), (700, 520)], GRN, 2)
text(650, 348, "data →", 9, "start", GRN, "bold")

# ---- columns ----
CX0, CW, CGAP, CY, CH = 760, 30, 44, 520, 210
n = 10
cols = []
for i in range(n):
    x = CX0 + i * CGAP; cols.append(x)
    box(x, CY, CW, CH, "#fafafa", "#999", 3, 1.5)
    for k in range(15): a(f'<rect x="{x+9}" y="{CY+8+k*13.8}" width="12" height="9" rx="1.5" fill="#ffd27a" stroke="#c9a24a" stroke-width="0.8"/>')
    up = (i % 2 == 0)      # even columns run bottom->top, odd columns top->bottom
    text(x + CW/2, CY - 8, str(i + 1), 10, "middle", BLK, "bold")
    a(f'<text x="{x+CW/2}" y="{CY+CH/2}" font-size="9" text-anchor="middle" fill="#888" transform="rotate(-90 {x+CW/2} {CY+CH/2})">{"▲ DIN at bottom" if up else "▼ DIN at top"}</text>')
# serpentine data chain
y_top, y_bot = CY - 2, CY + CH + 2
line([(700, 520), (700, y_bot + 22), (cols[0] + CW/2, y_bot + 22), (cols[0] + CW/2, y_bot)], GRN, 2)
for i in range(n - 1):
    xa, xb = cols[i] + CW/2, cols[i+1] + CW/2
    y = y_top - 12 if i % 2 == 0 else y_bot + 12
    line([(xa, y_top if i % 2 == 0 else y_bot), (xa, y), (xb, y), (xb, y_top if i % 2 == 0 else y_bot)], GRN, 2)
text(cols[0], y_top - 24, "DOUT → next DIN, alternating top / bottom (serpentine)", 10, "start", GRN, "bold")
# 5 V ring under the columns, GND ring above them
ry = y_bot + 40; gy = y_top - 40
line([(cols[0] - 12, ry), (cols[-1] + CW + 12, ry)], RED, 4)
line([(cols[0] - 12, gy), (cols[-1] + CW + 12, gy)], BLK, 4)
for x in cols:
    line([(x + 6, y_bot), (x + 6, ry)], RED, 1.5); dot(x + 6, ry, RED)       # 5 V in at the bottom pad
    line([(x + CW - 6, y_top), (x + CW - 6, gy)], BLK, 1.5); dot(x + CW - 6, gy, BLK)  # GND out at the top pad
text(cols[0] - 12, ry + 30, "5 V ring at the bottom of the mast (22 AWG) — feeds every column's bottom 5 V pad", 10, "start", RED, "bold")
text(cols[0] - 12, gy - 12, "GND ring at the top (22 AWG) — every column's top GND pad; one 22 AWG lead back down the bore", 10, "start", BLK, "bold")
text(cols[0] - 12, ry + 46, "Current enters each column at the bottom and leaves at the top: equal copper for every pixel, even brightness.", 9, "start", GRY)
# tie the rings to the rail
line([(700, 250), (700, 300), (735, 300), (735, ry), (cols[0] - 12, ry)], RED, 3)
line([(720, 250), (720, 290), (745, 290), (745, gy), (cols[0] - 12, gy)], BLK, 3)
# notes
nx, ny = 40, 470
box(nx, ny, 640, 300, "#f7f7f7", "#ccc", 8, 1)
notes = [("Notes", True),
 ("• 10 columns × 15 px = 150 × SK6812 RGBWW (144/m, 12 mm). Cut at the marks; ~104 mm each.", False),
 ("• Odd columns (1,3,5…) mount DIN-down, even columns DIN-up, so DOUT→DIN jumpers are a few mm.", False),
 ("  Firmware must reverse every second column (ESPHome: partition with reversed segments).", False),
 ("• Level shifter is REQUIRED: strip at 5 V wants ≥3.5 V on DIN; the C6 gives 3.3 V.", False),
 ("• Brightness cap in firmware ≈ 15–20 %: 150 px all-white at 100 % would be ~12 A. A flame", False),
 ("  effect at that cap averages ~1.5 A on the 2 A supply.", False),
 ("• 22 AWG for both rings and the PSU output; 30 AWG is fine for data and the shifter.", False),
 ("• XIAO is powered through its 5V pin (VBUS); nothing on its 3V3 pin. Do not plug USB in", False),
 ("  while on mains unless you are sure the meter/host is isolated.", False),
 ("• Mains: L → fuse → PSU; heat-shrink every joint; ≥4 mm creepage to anything low-voltage.", False)]
for i, (s, b) in enumerate(notes): text(nx + 12, ny + 24 + i * 24, s, 12 if b else 11, "start", BLK, "bold" if b else "normal")

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">' + "".join(o) + "</svg>"
open("flame-bulb-wiring.svg", "w").write(svg); print("svg ok")
