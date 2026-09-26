# Generates perfboard.svg — component placement on a 34 mm disc cut from
# 2.54 mm-pitch double-sided perfboard. Top view, component side.
# Grid: columns A–M (x = -6..6), rows 1–13 (row 1 at top, y = +6..-6).
import math
P = 2.54; S = 15.0  # px per mm
CX, CY = 310, 335; W, H = 1120, 680
o = []
def a(s): o.append(s)
def X(ix): return CX + ix*P*S
def Y(iy): return CY - iy*P*S
def col(c): return ord(c)-ord('A')-6
def row(r): return 7-int(r)
def hole(name): return X(col(name[0])), Y(row(name[1:]))
def text(x,y,s,size=12,anchor="middle",c="#222",w="normal"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{c}" font-weight="{w}">{s}</text>')
def wire(h1,h2,c,under=True,w=3):
    x1,y1=hole(h1); x2,y2=hole(h2)
    d=' stroke-dasharray="7 4"' if under else ''
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{d} opacity="0.9"/>')
def smd(h1,h2,label,c="#8d6e63"):
    x1,y1=hole(h1); x2,y2=hole(h2); mx,my=(x1+x2)/2,(y1+y2)/2
    horiz = y1==y2
    w_,h_ = (30,14) if horiz else (14,30)
    a(f'<rect x="{mx-w_/2}" y="{my-h_/2}" width="{w_}" height="{h_}" rx="2" fill="{c}" stroke="#222"/>')
    text(mx, my+4 if horiz else my+4, label, 9, c="#fff", w="bold") if horiz else text(mx+14, my+4, label, 10, "start")

a('<rect width="100%" height="100%" fill="#fff"/>')
text(20,26,"Perfboard layout — 34 mm disc, 2.54 mm pitch (top / component side)",18,"start",w="bold")
# board
a(f'<circle cx="{CX}" cy="{CY}" r="{17*S}" fill="#2e7d32" opacity="0.85"/>')
a(f'<circle cx="{CX}" cy="{CY}" r="{9*S}" fill="none" stroke="#fff" stroke-width="1" stroke-dasharray="4 4" opacity="0.6"/>')
text(CX, CY+9*S+12, "ring centre hole Ø18", 9, c="#fff")
# XIAO body: x from -5.8 to 15.2 mm, y ±8.75
a(f'<rect x="{CX-5.8*S}" y="{CY-8.75*S}" width="{21*S}" height="{17.5*S}" rx="6" fill="#e8f0fe" stroke="#1565c0" stroke-width="2" opacity="0.92"/>')
a(f'<rect x="{CX+15.2*S-2}" y="{CY-4.5*S}" width="{9*S*0.5}" height="{9*S}" rx="3" fill="#9e9e9e" stroke="#555"/>')
text(CX+15.2*S+4.5*S*0.5, CY+4, "USB-C", 9, c="#fff")
text(CX+9.5*S, CY-6*S, "XIAO ESP32-C6", 13, c="#1565c0", w="bold")
text(CX+9.5*S, CY-6*S+14, "component side up, USB-C → right", 9, c="#1565c0")
text(CX+9.5*S, CY+5.5*S, "Kapton under it; BAT+/BAT− wires from", 9, c="#1565c0")
text(CX+9.5*S, CY+5.5*S+12, "its underside pads drop through I7 / I8", 9, c="#1565c0")
# holes
for ix in range(-6,7):
    for iy in range(-6,7):
        if math.hypot(ix,iy)*P <= 16.0:
            a(f'<circle cx="{X(ix)}" cy="{Y(iy)}" r="6" fill="#c8a24a" stroke="#222" stroke-width="0.8"/>')
            a(f'<circle cx="{X(ix)}" cy="{Y(iy)}" r="2.5" fill="#1b3a1b"/>')
# axis labels
for ix in range(-6,7): text(X(ix), CY-17*S-8, chr(ord('A')+ix+6), 11, w="bold")
for iy in range(-6,7): text(CX-17*S-12, Y(iy)+4, str(7-iy), 11, w="bold")

# XIAO pins
top = ["D6","D5","D4","D3","D2","D1","D0"]; bot=["D7","D8","D9","D10","3V3","GND","5V"]
for i,c in enumerate("FGHIJKL"):
    x,y=hole(c+"4"); a(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#1565c0" stroke="#fff"/>'); text(x,y-11,top[i],9,c="#1565c0",w="bold")
    x,y=hole(c+"10"); a(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#1565c0" stroke="#fff"/>'); text(x,y+19,bot[i],9,c="#1565c0",w="bold")
# BAT feed-through holes
for h,l,c in (("I7","BAT+","#c62828"),("I8","BAT−","#222")):
    x,y=hole(h); a(f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{c}" stroke-width="2.5"/>'); text(x+10,y+4,l,9,"start",c,"bold")

# Q1 adapter: body B..D x rows 6..9, pins row 9 (B9 D, C9 S, D9 G)
x1,y1=hole("B6"); x2,y2=hole("D9")
a(f'<rect x="{x1-12}" y="{y1-12}" width="{x2-x1+24}" height="{y2-y1+24}" rx="4" fill="#546e7a" opacity="0.85" stroke="#222"/>')
text((x1+x2)/2,(y1+y2)/2-8,"Q1",12,c="#fff",w="bold"); text((x1+x2)/2,(y1+y2)/2+6,"AO3401A",9,c="#fff"); text((x1+x2)/2,(y1+y2)/2+18,"on SOT-23 adapter",8,c="#fff")
for h,l in (("B9","D"),("C9","S"),("D9","G")):
    x,y=hole(h); a(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#ffb300" stroke="#222"/>'); text(x,y+4,l,9,w="bold")
# Q3 TO-92 at C3,C4,C5 (S,G,D) lying flat to the left
for name,pins,lbl,dx in (("Q3",("C3","C4","C5"),"2N7000",-1),("Q2",("D10","D11","D12"),"2N7000",-1)):
    xs=[hole(p) for p in pins]; x,y0=xs[0]; y2=xs[2][1]
    a(f'<rect x="{x+dx*46-14}" y="{y0-10}" width="34" height="{y2-y0+20}" rx="10" fill="#37474f" stroke="#222"/>')
    text(x+dx*46+3,(y0+y2)/2-2,name,11,c="#fff",w="bold"); text(x+dx*46+3,(y0+y2)/2+10,lbl,8,c="#fff")
    for (px,py),l in zip(xs,("S","G","D")):
        a(f'<line x1="{x+dx*46+3}" y1="{py}" x2="{px}" y2="{py}" stroke="#999" stroke-width="2"/>')
        a(f'<circle cx="{px}" cy="{py}" r="6.5" fill="#ffb300" stroke="#222"/>'); text(px,py+4,l,9,w="bold")
# LED at D4 (A) / D5 (K)
x,y=hole("D4"); x2,y2=hole("D5")
a(f'<circle cx="{x}" cy="{(y+y2)/2}" r="20" fill="#fff59d" stroke="#f9a825" stroke-width="2" opacity="0.9"/>')
text(x,(y+y2)/2-3,"warm",9,w="bold"); text(x,(y+y2)/2+8,"LED",9,w="bold")
for h,l in (("D4","A"),("D5","K")):
    px,py=hole(h); a(f'<circle cx="{px}" cy="{py}" r="6.5" fill="#f9a825" stroke="#222"/>'); text(px,py+4,l,9,w="bold")
# SMD parts bridging adjacent pads
smd("D3","D4","82Ω"); smd("B4","C4","100Ω"); smd("C3","C4","100k")
smd("H3","I3","220k"); smd("I3","J3","220k"); smd("F3","G3","330Ω")
smd("C11","D11","1k"); smd("D10","D11","100k"); smd("C9","D9","100k")
smd("G11","H11","C1 100µF",c="#6d4c41")
# wires (dashed = underside)
RED,BLK,BLU,GRN,ORG,PUR="#e53935","#111","#1e88e5","#43a047","#fb8c00","#8e24aa"
for h in ("H3","D3","C9"): wire("I7",h,RED)
for h in ("J3","C3","D10","H11"): wire("I8",h,BLK)
wire("I3","L4",BLU); wire("F3","H4",GRN); wire("B4","J4",ORG); wire("C11","I4",PUR); wire("D12","D9",PUR)
wire("B9","G11",RED); wire("C5","D5",ORG,under=False)
# off-board leads
def lead(h,dx,dy,label,c):
    x,y=hole(h); a(f'<line x1="{x}" y1="{y}" x2="{x+dx}" y2="{y+dy}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'); text(x+dx+(6 if dx>0 else -6),y+dy+4,label,10,"start" if dx>0 else "end",c,"bold")
lead("G3",0,-60,"ring DIN ↑",GRN); lead("G11",-10,70,"ring VDD ↑",RED); lead("H11",20,70,"ring GND ↑",BLK)
lead("K4",40,-70,"SW1 (button) → GND",BLU)

# legend / notes
lx=CX+17*S+50; ly=70
a(f'<rect x="{lx}" y="{ly}" width="{W-lx-20}" height="{H-ly-20}" rx="8" fill="#f5f5f5" stroke="#ccc"/>')
notes=[
 ("Legend",True),
 ("● blue = XIAO castellation soldered to that pad",False),
 ("● amber = transistor / LED lead in that hole",False),
 ("▬ brown = 0805 resistor (or 1206 cap) bridging two",False),
 ("   adjacent pads, soldered on the underside",False),
 ("- - - dashed = insulated wire on the underside",False),
 ("——— solid = bridge / wire on top",False),
 ("",False),
 ("Nets",True),
 ("BAT+  I7 → H3, D3, C9 (Q1 source)",False),
 ("GND   I8 → J3, C3, D10, H11, SW1",False),
 ("D0 (L4) ← I3   divider node (220k/220k)",False),
 ("D1 (K4) ← SW1 tact switch, other leg to GND",False),
 ("D2 (J4) → B4  100Ω → C4 Q3 gate; 100k C3–C4",False),
 ("D3 (I4) → C11  1k → D11 Q2 gate; 100k D10–D11",False),
 ("D4 (H4) → F3  330Ω → G3 → ring DIN",False),
 ("Q3 drain C5 → D5 LED cathode; D4 anode → 82Ω → D3 BAT+",False),
 ("Q2 drain D12 → D9 Q1 gate; 100k C9–D9 pulls it up",False),
 ("Q1 drain B9 → G11 = switched rail → ring VDD",False),
 ("C1 100 µF across G11 (+) / H11 (−), ring GND → H11",False),
 ("",False),
 ("Build notes",True),
 ("Cut a 34 mm disc; only holes ≤16 mm from centre are used.",False),
 ("TO-92s lie flat (toward the edge); ring sits on 4.5 mm",False),
 ("standoffs to clear the XIAO's USB-C. Verify the XIAO pin",False),
 ("order against its silkscreen before soldering.",False),
 ("B6/C6/D6 are the adapter's unused row — leave them open.",False),
]
for i,(s,b) in enumerate(notes):
    text(lx+12, ly+22+i*18, s, 11 if not b else 12, "start", w="bold" if b else "normal")
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">\n'+"\n".join(o)+"\n</svg>\n"
open("perfboard.svg","w").write(svg)
