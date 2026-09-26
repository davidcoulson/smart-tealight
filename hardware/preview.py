# Python port of hardware/tealight.scad for preview/STL (manifold3d). Same numbers.
import math, numpy as np, trimesh
from manifold3d import Manifold, CrossSection
od,wall=38,1.0; id_=od-2*wall; floor_t=1.0; cell_h=8.5; perf_t=1.6; perf_d=34
ledge_z=floor_t+cell_h; cup_h=15.5; cap_h=7.5; skirt_h=2.0; clr=0.2
ring_od,ring_id,ring_t=32,18,1.6; carrier_od,carrier_id,carrier_h=34,29,4.5; xiao_cut_x=11
usb_w,usb_z0=10,12.0; btn_d,btn_x=4,-14; N=120
def cyl(d,h,z=0): return Manifold.cylinder(h,d/2,d/2,N).translate([0,0,z])
def box(x,y,z,sx,sy,sz): return Manifold.cube([sx,sy,sz]).translate([x,y,z])
def cup():
    c=cyl(od,cup_h)-cyl(id_,cup_h,floor_t)-box(id_/2-1,-usb_w/2,usb_z0,wall+2,usb_w,cup_h)-cyl(btn_d,floor_t+2,-1).translate([btn_x,0,0])
    for a in (90,210,330):
        c=c+box(id_/2-1.5,-1.5,ledge_z-1,1.5,3,1).rotate([0,0,a])
    return c
def carrier():
    return cyl(carrier_od,carrier_h)-cyl(carrier_id,carrier_h+2,-1)-box(xiao_cut_x,-od/2,-1,od,od,carrier_h+2)
def cap():
    # rounded top approximated: stack of cylinders following a r=2 fillet
    shell=cyl(od,cap_h-2)
    for i in range(1,9):
        t=i/8*math.pi/2; shell=shell+cyl(od-4+4*math.cos(t),0.3,cap_h-2+2*math.sin(t)-0.15)
    shell=shell-cyl(id_,cap_h-wall+1,-1)
    skirt=cyl(id_-2*clr,skirt_h)-cyl(id_-2*clr-2*wall,skirt_h+2,-1)-box(id_/2-3,-(usb_w+2)/2,-1,5,usb_w+2,skirt_h+2)
    return shell+skirt.translate([0,0,-skirt_h])
def tm(m,color):
    mesh=m.to_mesh(); t=trimesh.Trimesh(np.array(mesh.vert_properties)[:,:3],np.array(mesh.tri_verts)); t.visual.face_colors=color; return t
parts={"cup":cup(),"carrier":carrier(),"cap":cap()}
for k,v in parts.items():
    t=tm(v,[120,120,120,255]); t.export(f"./{k}.stl"); print(k,"watertight",t.is_watertight,"volume mm3 %.0f"%t.volume, "bbox", np.round(t.bounds,1).tolist())
# exploded preview
scene=[tm(parts["cup"],[90,90,90,255]),
       tm(parts["carrier"].translate([0,0,ledge_z+perf_t+12]),[90,90,90,255]),
       tm(parts["cap"].translate([0,0,cup_h+24]),[255,240,160,200]),
       tm(box(-10,-15,floor_t,20,30,8),[255,150,50,255]),
       tm(cyl(perf_d,perf_t,ledge_z),[40,140,40,255]),
       tm(box(-5.8,-8.75,ledge_z+perf_t,21,17.5,4),[70,130,180,255]),
       tm((cyl(ring_od,ring_t)-cyl(ring_id,ring_t+2,-1)).translate([0,0,ledge_z+perf_t+carrier_h+12]),[240,240,240,255])]
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(11,7)); 
for i,(el,az,title) in enumerate(((25,-50,"exploded, iso"),(0,0,"exploded, side"))):
    ax=fig.add_subplot(1,2,i+1,projection="3d")
    for t in scene:
        pc=Poly3DCollection(t.vertices[t.faces],alpha=t.visual.face_colors[0][3]/255,facecolor=np.array(t.visual.face_colors[0][:3])/255,edgecolor="none"); ax.add_collection3d(pc)
    ax.set_xlim(-22,22); ax.set_ylim(-22,22); ax.set_zlim(0,55); ax.set_box_aspect((1,1,1.25)); ax.view_init(el,az); ax.set_title(title); ax.set_axis_off()
plt.tight_layout(); plt.savefig("./preview.png",dpi=110); print("preview ok")
