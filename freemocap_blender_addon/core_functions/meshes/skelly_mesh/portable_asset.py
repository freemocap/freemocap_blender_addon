"""Load the same Skelly geometry on Blender 3.0 and newer."""
import gzip
import json
from pathlib import Path

import bpy

from .skelly_mesh_paths import SKELLY_FULL_MESH_PATH


def load_skelly_mesh():
    path = Path(SKELLY_FULL_MESH_PATH).with_name('skelly_mesh.json.gz')
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        data = json.load(stream)
    if data['schema_version'] != 1:
        raise ValueError('Unsupported Skelly mesh asset version')
    mesh = bpy.data.meshes.new('skelly_mesh')
    mesh.from_pydata(data['vertices'], [], data['faces'])
    mesh.update()
    obj = bpy.data.objects.new('skelly_mesh', mesh)
    bpy.context.collection.objects.link(obj)
    for name, memberships in data['groups'].items():
        group = obj.vertex_groups.new(name=name)
        # Preserve non-unit weights too; helper groups must retain all members.
        weights = {}
        for index, weight in memberships:
            weights.setdefault(weight, []).append(index)
        for weight, indices in weights.items():
            group.add(indices, weight, 'REPLACE')
    material = bpy.data.materials.get('Skelly bone') or bpy.data.materials.new('Skelly bone')
    material.diffuse_color = (.72, .86, .88, 1.)
    material.use_nodes = True
    shader = material.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = material.diffuse_color
    shader.inputs['Roughness'].default_value = .5
    mesh.materials.append(material)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    return obj
