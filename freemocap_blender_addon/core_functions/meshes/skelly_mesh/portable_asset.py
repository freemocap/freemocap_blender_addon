"""Load the same Skelly geometry on Blender 3.0 and newer."""
import gzip
import json
from pathlib import Path

import bpy

from .skelly_mesh_paths import SKELLY_FULL_MESH_PATH


def load_skelly_mesh(*, canonical=False):
    path = Path(SKELLY_FULL_MESH_PATH).with_name('skelly_mesh.json.gz')
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        data = json.load(stream)
    if (data['schema_version'] != 2 or
            data['coordinate_system'] != 'blender_x_right_y_forward_z_up'):
        raise ValueError('Unsupported Skelly mesh asset version')
    # The legacy attachment helpers still consume the historical asset basis.
    # Native consumers receive canonical geometry without any pose conversion.
    vertices = data['vertices'] if canonical else [(-x, -y, z) for x, y, z in data['vertices']]
    mesh = bpy.data.meshes.new('skelly_mesh')
    mesh.from_pydata(vertices, [], data['faces'])
    mesh.update()
    obj = bpy.data.objects.new('skelly_mesh', mesh)
    bpy.context.collection.objects.link(obj)
    obj['attachment_frames'] = json.dumps(data['attachment_frames'])
    for name, memberships in data['groups'].items():
        group = obj.vertex_groups.new(name=name)
        # Preserve non-unit weights too; helper groups must retain all members.
        weights = {}
        for index, weight in memberships:
            weights.setdefault(weight, []).append(index)
        for weight, indices in weights.items():
            group.add(indices, weight, 'REPLACE')
    for definition in data['materials']:
        material = bpy.data.materials.new('Skelly ' + definition['name'])
        material.diffuse_color = definition['diffuse_color']
        material.use_nodes = True
        shader = material.node_tree.nodes.get('Principled BSDF')
        for name, value in definition['inputs'].items():
            # Principled renamed these sockets in Blender 4.0.
            socket = {'Specular IOR Level': 'Specular', 'Emission Color': 'Emission'}.get(name, name) if bpy.app.version < (4, 0) else name
            shader.inputs[socket].default_value = value
        mesh.materials.append(material)
    for polygon, index, smooth in zip(mesh.polygons, data['face_materials'], data['face_smooth']):
        polygon.material_index = index
        polygon.use_smooth = smooth
    return obj
