# Generates flame-bulb-exploded.svg: side-view exploded assembly with the
# electronics, drawn to scale (S px/mm) with exploded gaps between parts.
S = 2.75                     # px per mm
CX = 480                    # part centreline x
GAP = 22                     # exploded gap, mm
W, H = 1180, 1040
o = []
def a(s): o.append(s)
def X(mm): return CX + mm*S
def rect(cx_mm, w_mm, y_mm, h_mm, fill, stroke="#222", dash="", op=1.0, rx=2):
    x = X(cx_mm - w_mm/2); y = Y(y_mm + h_mm)
    a(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_mm*S:.1f}" height="{h_mm*S:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{f" stroke-dasharray=\"{dash}\"" if dash else ""} opacity="{op}"/>')
def text(x, y, s, size=13, anchor="start", c="#222", w="normal"):
    a(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}" font-weight="{w}">{s}</text>')
def leader(from_mm_x, y_mm, label, sub="", side="r"):
    x0 = X(from_mm_x); y0 = Y(y_mm)
    x1 = 760 if side == "r" else 330
    a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1}" y2="{y0:.1f}" stroke="#888" stroke-width="1" stroke-dasharray="3 3"/>')
    a(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="3" fill="#888"/>')
    text(x1 + (8 if side=="r" else -8), y0 + 4, label, 13, "start" if side=="r" else "end", "#111", "bold")
    if sub: text(x1 + (8 if side=="r" else -8), y0 + 20, sub, 11, "start" if side=="r" else "end", "#555")

# vertical layout (mm, bottom-up), with exploded gaps
BOT = 8
def Y(mm): return H - 30 - mm*S       # mm above the page bottom -> px

y = BOT
# ---- E26 shell ----
e26_y = y
rect(0, 26, y, 22, "#c9c9c9", rx=3)                   # screw shell
for i in range(4): a(f'<line x1="{X(-13):.1f}" y1="{Y(y+4+i*5):.1f}" x2="{X(13):.1f}" y2="{Y(y+4+i*5):.1f}" stroke="#888" stroke-width="1"/>')
rect(0, 26, y+22, 8, "#3a2a1a", rx=2)                  # bakelite body above the threads
rect(0, 8, y-6, 6, "#777", rx=3)                      # centre contact
leader(13, y+11, "E26 male pigtail plug", "threaded shell + bakelite body, two leads; epoxied into the cup")
y += 30 + GAP
# ---- cap ----
cap_y = y
rect(0, 31.5, y, 12, "#555")                         # cup for the plug
rect(0, 26.5, y+2, 10.5, "#777", "#555", "4 2")        # plug body sits in here
rect(0, 57, y+12, 2, "#555")                         # flange
rect(0, 53, y+14, 3.4, "#555")                       # press-in plug
leader(16, y+6, "cap  (PC-FR)", "cup captures the E26 plug; leads pass through the floor")
leader(-28.5, y+13, "fuse 1 A slow-blow, in the E26 lead", "heat-shrunk, tucked in the cap", side="l")
y += 17.4 + GAP
# ---- base with PSU ----
base_y = y
rect(0, 57, y, 37.4, "#4a4a4a")                      # body (base_h 41.4 minus spigot)
rect(0, 54, y+37.4, 4, "#4a4a4a")                    # spigot
rect(0, 47, y+4, 28, "#2b6cb0", "#8fc1ff", "5 3", 0.9)   # HLK-10M05 on its side (dashed = inside)
text(X(0), Y(y+20)+4, "HLK-10M05", 11, "middle", "#fff", "bold")
text(X(0), Y(y+13)+4, "AC → 5 V 2 A, on its side", 10, "middle", "#dbeafe")
leader(28.5, y+22, "base  (PC-FR), 41 mm", "open bottom: PSU drops in, cap closes it")
leader(-14, y+38, "10-facet socket + wire hole in the top plate", "5 V / GND / data up into the core", side="l")
y += 41.4 + GAP
# ---- core with XIAO, shifter, strips ----
core_y = y
rect(0, 39.5, y, 70, "#e0932a")                      # mast (10 facets)
for i in range(1, 10): a(f'<line x1="{X(-19.75+i*3.95):.1f}" y1="{Y(y+70):.1f}" x2="{X(-19.75+i*3.95):.1f}" y2="{Y(y):.1f}" stroke="#b8741a" stroke-width="0.8"/>')
# strips on two visible facets
for fx in (-14, 12):
    rect(fx, 6, y+1, 68, "#f5f5f5", "#999")
    for k in range(10): a(f'<rect x="{X(fx)-4:.1f}" y="{Y(y+4+k*6.94)-4:.1f}" width="8" height="8" rx="1" fill="#ffd27a" stroke="#c9a24a"/>')
# XIAO inside bore (dashed)
rect(0, 18, y+20, 21, "#1565c0", "#9ecbff", "5 3", 0.9)
text(X(0), Y(y+30)+4, "XIAO C6", 10, "middle", "#fff", "bold")
rect(0, 12, y+8, 8, "#6a1b9a", "#d1a3ff", "5 3", 0.9)
text(X(0), Y(y+12)+3.5, "74AHCT125", 8, "middle", "#fff", "bold")
rect(0, 8, y+46, 12, "#333", "#bbb", "5 3", 0.9)
text(X(0), Y(y+52)+3.5, "1000µF", 8, "middle", "#fff")
leader(19.75, y+60, "core  (PETG), 10 facets", "XIAO, level shifter and cap live in the bore")
leader(-17, y+35, "SK6812 RGBWW 144/m, 12 mm strip", "10 columns × 10 px, data-in at the bottom of each", side="l")
leader(-19.75, y+3, "5 V ring at the base of the mast (22 AWG)", "star-feeds all 10 columns", side="l")
y += 70 + GAP
# ---- shade ----
sh_y = y
rect(0, 57, y, 76, "#fff3c4", "#c9b76a", "", 0.85)
rect(0, 53, y+76, 2, "#fff3c4", "#c9b76a", "", 0.85, rx=6)
leader(28.5, y+40, "shade  (translucent PETG)", "one piece; slides down over the core onto the base spigot")

# title / scale
text(30, 34, "Flame bulb — exploded assembly (side view, to scale)", 20, "start", "#111", "bold")
text(30, 56, "Ø57 mm, ~140 mm tall including the E26 plug. Dashed = inside a printed part.", 12, "start", "#555")
# assembly order strip
steps = ["1 mains: shell → fuse → HLK-10M05", "2 PSU into base, cap closes bottom", "3 XIAO + shifter + cap into core", "4 strips on facets, ring-feed 5 V", "5 core into base socket", "6 shade over the top"]
text(760, 76, "Assembly order", 12, "start", "#111", "bold")
for i, s in enumerate(steps): text(760, 96 + i*17, s, 11, "start", "#333")
a(f'<line x1="{X(0):.1f}" y1="{Y(BOT-8):.1f}" x2="{X(0):.1f}" y2="{Y(sh_y+80):.1f}" stroke="#bbb" stroke-width="1" stroke-dasharray="2 6"/>')  # centreline
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif"><rect width="100%" height="100%" fill="#fff"/>' + "".join(o) + "</svg>"
open("flame-bulb-exploded.svg", "w").write(svg)
print("svg ok")
