"""Run in a Blender that can read the source asset to create a portable copy.

blender --background --python tools/extract_skelly_asset.py -- OUTPUT.json.gz
The original .blend remains the editable source. The portable representation
preserves topology and vertex groups (including helpers), normalizes coordinates
to +X right/+Y forward/+Z up, and declares complete attachment-frame roll hints.
"""
import gzip
import json
from pathlib import Path
import sys
import runpy

import bpy
canonical_asset = runpy.run_path(str(Path(__file__).with_name('skelly_asset_format.py')))['canonical_asset']

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
payload['materials'] = []
for material in obj.data.materials:
    shader = next(n for n in material.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    if len(material.node_tree.nodes) != 2:
        raise ValueError('Portable Skelly supports the authored Principled/output materials only')
    inputs = {}
    for name in ('Base Color', 'Metallic', 'Roughness', 'IOR', 'Alpha',
                 'Specular IOR Level', 'Emission Color', 'Emission Strength'):
        value = shader.inputs[name].default_value
        inputs[name] = list(value) if hasattr(value, '__len__') else value
    payload['materials'].append(dict(name=material.name, diffuse_color=list(material.diffuse_color), inputs=inputs))
payload['face_materials'] = [p.material_index for p in obj.data.polygons]
payload['face_smooth'] = [p.use_smooth for p in obj.data.polygons]
payload = canonical_asset(payload)
output = Path(sys.argv[sys.argv.index('--') + 1])
with output.open('wb') as stream:
    with gzip.GzipFile(filename='', fileobj=stream, mode='wb', mtime=0) as compressed:
        compressed.write(json.dumps(payload, separators=(',', ':')).encode())
print('PORTABLE_SKELLY', len(payload['vertices']), len(payload['faces']), len(groups), str(output))
