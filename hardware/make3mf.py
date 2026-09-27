#!/usr/bin/env python3
"""Pack binary STLs into one 3MF, print-oriented and laid out on the plate.
Usage: make3mf.py out.3mf "Title" name:file.stl[:flipX][@x,y] ..."""
import struct, zipfile, sys

def read_stl(p):
    d = open(p, 'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    verts, tris, idx, off = [], [], {}, 84
    for _ in range(n):
        v = struct.unpack('<12fH', d[off:off+50]); off += 50
        t = []
        for k in (3, 6, 9):
            key = (round(v[k], 5), round(v[k+1], 5), round(v[k+2], 5))
            if key not in idx:
                idx[key] = len(verts); verts.append(key)
            t.append(idx[key])
        tris.append(t)
    return verts, tris

out, title, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
objs, items = [], []
for i, spec in enumerate(specs, start=1):
    place = (0.0, 0.0)
    if "@" in spec:
        spec, pos = spec.split("@"); place = tuple(float(x) for x in pos.split(","))
    bits = spec.split(":")
    name, path = bits[0], bits[1]
    flip = "flipX" in bits[2:]
    v, t = read_stl(path)
    if flip:                                   # 180 deg about X: proper rotation,
        v = [(x, -y, -z) for (x, y, z) in v]   # winding and normals stay valid
    minz = min(z for _, _, z in v)
    v = [(x, y, z - minz) for (x, y, z) in v]  # sit on the bed
    vx = "".join(f'<vertex x="{x:.5f}" y="{y:.5f}" z="{z:.5f}"/>' for x, y, z in v)
    tx = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
    objs.append(f'<object id="{i}" type="model" name="{name}">'
                f'<mesh><vertices>{vx}</vertices><triangles>{tx}</triangles></mesh></object>')
    items.append(f'<item objectid="{i}" transform="1 0 0 0 1 0 0 0 1 '
                 f'{place[0]} {place[1]} 0"/>')
    print(f"  {name:28s} {len(v):6d} verts  {'flipped' if flip else ''}")

model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
         'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         f'<metadata name="Title">{title}</metadata>'
         '<metadata name="Designer">davidcoulson/smart-tealight</metadata>'
         f'<resources>{"".join(objs)}</resources><build>{"".join(items)}</build></model>')
ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", ct); z.writestr("_rels/.rels", rels)
    z.writestr("3D/3dmodel.model", model)
print("wrote", out)
