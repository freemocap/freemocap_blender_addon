"""Run in a Blender that can read the source asset to create a portable copy.

blender --background --python tools/extract_skelly_asset.py -- OUTPUT.json.gz
The original .blend remains the editable source. The portable representation
preserves topology, coordinates and all vertex groups (including helper points).
"""
import gzip
import json
from pathlib import Path
import sys

import bpy

source = Path(__file__).resolve().parents[1] / 'freemocap_blender_addon/assets/skelly_full_mesh_20k_faces.blend'
with bpy.data.libraries.load(str(source), link=False) as (_, target):
    target.objects = ['skelly_mesh']
obj = target.objects[0]
groups = {g.name: [] for g in obj.vertex_groups}
for vertex in obj.data.vertices:
    for membership in vertex.groups:
        groups[obj.vertex_groups[membership.group].name].append([vertex.index, membership.weight])
payload = dict(schema_version=1, source=source.name,
               vertices=[v.co[:] for v in obj.data.vertices],
               faces=[list(p.vertices) for p in obj.data.polygons],
               groups=groups)
output = Path(sys.argv[sys.argv.index('--') + 1])
with output.open('wb') as stream:
    with gzip.GzipFile(filename='', fileobj=stream, mode='wb', mtime=0) as compressed:
        compressed.write(json.dumps(payload, separators=(',', ':')).encode())
print('PORTABLE_SKELLY', len(payload['vertices']), len(payload['faces']), len(groups), str(output))
