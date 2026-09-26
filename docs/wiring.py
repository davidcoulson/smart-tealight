# Generates docs/wiring.svg (run from the docs/ directory)
W, H = 1150, 1060
o = []
def a(s): o.append(s)
RED, BLK, GRY, BLU, GRN, ORG = "#c62828", "#222", "#666", "#1565c0", "#2e7d32", "#ef6c00"
def line(pts, c=BLK, w=2):
    a(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>')
def dot(x,y,c=BLK): a(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
def text(x,y,s,size=13,anchor="start",c=BLK,weight="normal"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{c}" font-weight="{weight}">{s}</text>')
def res_v(x,y1,y2,label,c=BLK):
    m=(y1+y2)/2; line([(x,y1),(x,m-18)],c); line([(x,m+18),(x,y2)],c)
    a(f'<rect x="{x-7}" y="{m-18}" width="14" height="36" fill="#fff" stroke="{c}" stroke-width="2"/>')
    text(x+12,m+5,label,12)
def res_h(x1,x2,y,label,c=BLK):
    m=(x1+x2)/2; line([(x1,y),(m-18,y)],c); line([(m+18,y),(x2,y)],c)
    a(f'<rect x="{m-18}" y="{y-7}" width="36" height="14" fill="#fff" stroke="{c}" stroke-width="2"/>')
    text(m,y-12,label,12,"middle")
def gnd(x,y):
    line([(x,y),(x,y+10)]); 
    for i,wd in enumerate((14,9,4)): line([(x-wd,y+10+i*5),(x+wd,y+10+i*5)],BLK,2)
def batp(x,y):  # flag pointing up at (x,y) = wire end
    line([(x,y),(x,y-8)],RED); a(f'<polygon points="{x-7},{y-8} {x+7},{y-8} {x},{y-18}" fill="{RED}"/>')
    text(x,y-22,"BAT+",11,"middle",RED,"bold")
def fet(x,y,kind,name,part):
    # channel at x, gate enters from left at y; drain top (x+14,y-25), source bottom (x+14,y+25)
    a(f'<circle cx="{x+6}" cy="{y}" r="24" fill="#fff" stroke="{BLK}" stroke-width="1.5"/>')
    line([(x-18,y),(x-8,y)]); line([(x-8,y-12),(x-8,y+12)])
    line([(x-2,y-14),(x-2,y+14)])
    line([(x-2,y-10),(x+14,y-10),(x+14,y-25)]); line([(x-2,y+10),(x+14,y+10),(x+14,y+25)])
    if kind=="N": a(f'<polygon points="{x-1},{y+10} {x+7},{y+6} {x+7},{y+14}" fill="{BLK}"/>')
    else: a(f'<polygon points="{x+8},{y-10} {x},{y-14} {x},{y-6}" fill="{BLK}"/>')
    text(x+34,y-4,name,12,weight="bold"); text(x+34,y+11,part,11,c=GRY)

a('<rect width="100%" height="100%" fill="#ffffff"/>')
text(40,38,"Smart tea light — wiring (Track A: XIAO ESP32-C6)",20,weight="bold")
text(40,60,"Same wiring for XIAO nRF54L15, except the D0 battery divider (built in on the nRF54L15)",13,c=GRY)

# XIAO block
xl,xr,yt,yb=60,230,110,880
a(f'<rect x="{xl}" y="{yt}" width="{xr-xl}" height="{yb-yt}" rx="10" fill="#e8f0fe" stroke="{BLU}" stroke-width="2.5"/>')
text((xl+xr)/2,yt+30,"Seeed XIAO",16,"middle",BLU,"bold"); text((xl+xr)/2,yt+50,"ESP32-C6 / nRF54L15",12,"middle",BLU)
a(f'<rect x="{xl-12}" y="{yt+80}" width="14" height="44" rx="3" fill="#bbb" stroke="{GRY}"/>')
text(xl+10,yt+106,"USB-C",11,c=GRY); text(xl+10,yt+120,"(charge/flash)",10,c=GRY)
pins={"D0":180,"D1":300,"D2":470,"D3":720,"D4":840}
gp={"D0":"GPIO0","D1":"GPIO1","D2":"GPIO2","D3":"GPIO21","D4":"GPIO22"}
for p,y in pins.items():
    dot(xr,y,BLU); text(xr-8,y+4,p,13,"end",BLU,"bold"); text(xr-8,y+18,gp[p],10,"end",GRY)
text((xl+xr)/2,yb-30,"battery pads",11,"middle",GRY); text((xl+xr)/2,yb-17,"(underside)",11,"middle",GRY)
for lbl,x in (("BAT+",110),("BAT−",190)):
    dot(x,yb,RED if "+" in lbl else BLK); text(x,yb-3-2,"",1)
text(104,yb+18,"BAT+",11,"end",RED,"bold"); text(196,yb+18,"BAT−",11,"start",BLK,"bold")

# battery
line([(110,yb),(110,940)],RED); line([(190,yb),(190,940)])
a(f'<rect x="80" y="940" width="140" height="55" rx="6" fill="#fff8e1" stroke="{ORG}" stroke-width="2"/>')
text(150,962,"LiPo 3.7 V ~400 mAh",12,"middle",weight="bold"); text(150,980,"802030, protected, JST",11,"middle",GRY)
text(96,935,"+",15,"middle",RED,"bold"); text(204,935,"−",15,"middle",BLK,"bold")
dot(110,915,RED)
gnd(190,905); dot(190,905)

# D0: battery divider
y=pins["D0"]; x=340
line([(xr,y),(x,y)]); dot(x,y)
res_v(x,90,y,"R1 220k"); batp(x,90)
res_v(x,y,y+80,"R2 220k"); gnd(x,y+80)
a(f'<line x1="{x+60}" y1="{y}" x2="{x+60}" y2="{y}" />')
text(x+75,y-30,"Battery sense (C6 only)",13,weight="bold")
text(x+75,y-14,"halves 4.2 V → 2.1 V for the ADC",12,c=GRY)
text(x+75,y+2,"optional 100 nF across R2",12,c=GRY)

# D1: button
y=pins["D1"]; line([(xr,y),(320,y)])
a(f'<circle cx="320" cy="{y}" r="3" fill="#fff" stroke="{BLK}" stroke-width="2"/><circle cx="370" cy="{y}" r="3" fill="#fff" stroke="{BLK}" stroke-width="2"/>')
line([(322,y-4),(366,y-16)]); line([(344,y-10),(344,y-24)]); line([(334,y-24),(354,y-24)])
line([(373,y),(400,y)]); gnd(400,y)
text(430,y-6,"SW1 6×6 tact switch → GND",13,weight="bold")
text(430,y+10,"internal pull-up; tap = candle on/off, hold 2 s = ship mode, wakes from deep sleep",12,c=GRY)

# D2: warm LED low-side
y=pins["D2"]; gx=440; fx=520
res_h(xr,gx,y,"100 Ω")
dot(gx,y); res_v(gx,y,y+70,""); text(gx-50,y+45,"100k",12); gnd(gx,y+70)
line([(gx,y),(fx-18,y)]); fet(fx,y,"N","Q3","AO3400 (N)")
dx=fx+14
line([(dx,y+25),(dx,y+45)]); gnd(dx,y+45)
# LED chain: drain -> up -> right -> LED -> 82R -> BAT+
ty=y-45
line([(dx,y-25),(dx,ty),(dx+60,ty)])
lx=dx+75
a(f'<polygon points="{lx-3},{ty-10} {lx-3},{ty+10} {lx+12},{ty}" fill="#fff59d" stroke="{BLK}" stroke-width="2"/>')
line([(lx+12,ty-10),(lx+12,ty+10)]); line([(lx+12,ty),(lx+30,ty)])
line([(lx+2,ty-14),(lx+10,ty-24)],ORG); line([(lx+10,ty-12),(lx+18,ty-22)],ORG)
res_h(lx+30,lx+110,ty,"82 Ω"); line([(lx+110,ty),(lx+130,ty)],RED); batp(lx+130,ty)
text(dx+120,ty+30,"Warm-white candle LED (low-power mode)",13,weight="bold")
text(dx+120,ty+46,"2200–2700 K, ~10 mA at 3.7 V; PWM on D2",12,c=GRY)
text(dx+120,ty+62,"sits in the ring's centre hole",12,c=GRY)

# D3: rail switch
y=pins["D3"]; gx=440; q2=520
res_h(xr,gx,y,"1k")
dot(gx,y); res_v(gx,y,y+60,""); text(gx-50,y+35,"100k",12); gnd(gx,y+60)
line([(gx,y),(q2-18,y)]); fet(q2,y,"N","Q2","2N7002 (N)")
d2=q2+14; line([(d2,y+25),(d2,y+40)]); gnd(d2,y+40)
q1y=y-75; q1=d2+60+18  # gate node at d2
line([(d2,y-25),(d2,q1y)]); dot(d2,q1y)
res_v(d2,q1y-65,q1y,""); text(d2-50,q1y-28,"100k",12); batp(d2,q1y-65)
line([(d2,q1y),(q1-18,q1y)])
fet(q1,q1y,"P","Q1","AO3401A (P)")
s1=q1+14
line([(s1,q1y-25),(s1,q1y-45)]); batp(s1,q1y-45)
# drain -> ring VDD
vdd_y=q1y+45
line([(s1,q1y+25),(s1,vdd_y),(800,vdd_y)],RED)
text(s1+10,vdd_y-8,"switched LED rail",11,c=RED)
cx=720; dot(cx,vdd_y,RED); line([(cx,vdd_y),(cx,vdd_y+22)])
line([(cx-14,vdd_y+22),(cx+14,vdd_y+22)],BLK,3); line([(cx-14,vdd_y+30),(cx+14,vdd_y+30)],BLK,3)
line([(cx,vdd_y+30),(cx,vdd_y+42)]); gnd(cx,vdd_y+42); text(cx+18,vdd_y+32,"100 µF",12)

# D4: data
y=pins["D4"]; res_h(xr,560,y,"330 Ω"); line([(560,y),(800,y)],GRN)
text(580,y+18,"data (hold LOW when rail is off)",11,c=GRN)

# LED ring
rx,ry=960,800
a(f'<circle cx="{rx}" cy="{ry}" r="95" fill="#fafafa" stroke="{BLK}" stroke-width="2"/><circle cx="{rx}" cy="{ry}" r="45" fill="#fff" stroke="{GRY}" stroke-width="1.5"/>')
import math
cols=["#e53935","#fb8c00","#fdd835","#43a047","#1e88e5","#8e24aa","#e53935","#fb8c00"]
for i in range(8):
    t=math.radians(i*45-90); px,py=rx+70*math.cos(t),ry+70*math.sin(t)
    a(f'<rect x="{px-9}" y="{py-9}" width="18" height="18" rx="2" fill="{cols[i]}" opacity="0.85" stroke="{BLK}"/>')
text(rx,ry-4,"8× WS2812B",12,"middle",weight="bold"); text(rx,ry+12,"32 mm ring",11,"middle",GRY)
text(rx,ry+115,"(or SK6812 RGBW/RGBWW)",11,"middle",GRY)
# pads
for lbl,py,c in (("VDD",vdd_y,RED),("GND",ry+5,BLK),("DIN",700,GRN)):
    pass
# connect pads: lines to ring edge
line([(800,vdd_y),(840,vdd_y),(850,ry-55)],RED); text(806,vdd_y-8,"VDD",12,c=RED,weight="bold")
line([(800,840),(840,840),(848,ry+50)],GRN); text(806,832,"DIN",12,c=GRN,weight="bold")
line([(826,ry+5),(790,ry+5)]); text(800,ry,"GND",12,weight="bold"); gnd(790,ry+5)

# notes box
nx,ny=620,90
a(f'<rect x="{nx}" y="{ny}" width="510" height="95" rx="8" fill="#f5f5f5" stroke="#ccc"/>')
notes=["Every ⏚ is one common GND (XIAO GND = battery −).",
       "BAT+ is the cell’s positive terminal (3.0–4.2 V); it’s live while charging too.",
       "D3 HIGH → Q2 on → Q1 gate pulled low → LED rail on. 100k pull-downs keep",
       "the ring and warm LED off while the XIAO boots or sleeps."]
for i,s in enumerate(notes): text(nx+14,ny+24+i*20,s,12.5)

a(f'<text x="1120" y="1045" font-size="11" text-anchor="end" fill="{GRY}">docs/wiring.svg — generated by docs/wiring.py</text>')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">\n'+"\n".join(o)+"\n</svg>\n"
open("wiring.svg","w").write(svg)
