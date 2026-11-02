"""Validate the generated VRM against its explicit Forge/artwork build input.

This checks our export contract, not every possible glTF or VRM feature.
VRM0 normalization and humanoid metadata: [@vrm0Specification].
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation


def load_glb(path: Path):
    data = path.read_bytes()
    magic, version, length = struct.unpack_from('<4sII', data)
    if magic != b'glTF' or version != 2 or length != len(data):
        raise ValueError('Invalid GLB header')
    json_size, json_kind = struct.unpack_from('<I4s', data, 12)
    if json_kind != b'JSON':
        raise ValueError('Missing GLB JSON')
    document = json.loads(data[20:20 + json_size])
    offset = 20 + json_size
    binary_size, binary_kind = struct.unpack_from('<I4s', data, offset)
    if binary_kind != b'BIN\0' or offset + 8 + binary_size != len(data):
        raise ValueError('Invalid GLB binary buffer')
    return document, data[offset + 8:]


def accessor(document, binary, index):
    item = document['accessors'][index]
    if 'sparse' in item:
        raise ValueError('Unexpected sparse accessor in this rigid export')
    view = document['bufferViews'][item['bufferView']]
    dtype = np.dtype({5121: 'u1', 5123: '<u2', 5125: '<u4', 5126: '<f4'}[item['componentType']])
    width = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}[item['type']]
    return np.ndarray((item['count'], width), dtype=dtype, buffer=binary,
                      offset=view.get('byteOffset', 0) + item.get('byteOffset', 0),
                      strides=(view.get('byteStride', width * dtype.itemsize), dtype.itemsize)).copy()


def validate(vrm_path: Path, payload: dict, build: dict) -> dict:
    document, binary = load_glb(vrm_path)
    version = payload.get('vrmVersion', '0.0')
    vrm = document['extensions']['VRM' if version == '0.0' else 'VRMC_vrm']
    if vrm['specVersion'] != version:
        raise ValueError('Exported VRM version differs from requested target')
    nodes = document['nodes']
    indices = {node['name']: i for i, node in enumerate(nodes)}
    bindings = ({bone['bone']: nodes[bone['node']]['name'] for bone in vrm['humanoid']['humanBones']}
                if version == '0.0' else
                {name: nodes[bone['node']]['name'] for name, bone in vrm['humanoid']['humanBones'].items()})
    if bindings != payload['humanoid']:
        raise ValueError('Exported humanoid bindings differ from the build input')
    parents = {child: i for i, node in enumerate(nodes) for child in node.get('children', [])}
    for node in nodes:
        if 'matrix' in node or not np.allclose(node.get('rotation', [0, 0, 0, 1]), [0, 0, 0, 1], atol=2e-7) or not np.allclose(node.get('scale', [1, 1, 1]), 1):
            raise ValueError('Expected normalized avatar nodes')

    matrices = {}

    def world_matrix(index):
        if index not in matrices:
            node = nodes[index]
            if 'matrix' in node:
                local = np.asarray(node['matrix']).reshape(4, 4).T
            else:
                local = np.eye(4)
                local[:3, :3] = Rotation.from_quat(node.get('rotation', [0, 0, 0, 1])).as_matrix() @ np.diag(node.get('scale', [1, 1, 1]))
                local[:3, 3] = node.get('translation', [0, 0, 0])
            matrices[index] = world_matrix(parents[index]) @ local if index in parents else local
        return matrices[index]

    def world(index):
        return world_matrix(index)[:3, 3]

    def vrm0_position(points):
        # Versioned VRM0 file convention, not Forge registry's VRM1 convention.
        return np.asarray(points) @ np.asarray(payload['coordinateBindings']['sourceToFile']).T

    shift = np.array([0, 0, build['floorOffsetMeters']])
    maximum_origin_error = 0.
    for bone in payload['bones']:
        index = indices[bone['name']]
        parent_index = parents.get(index)
        # VRM1 may preserve the armature object as a non-bone root container.
        actual_parent = nodes[parent_index]['name'] if parent_index is not None and nodes[parent_index]['name'] in payload['avatarParents'] else None
        if actual_parent != payload['avatarParents'][bone['name']]:
            raise ValueError(f"Hierarchy changed at {bone['name']}")
        expected = vrm0_position(np.asarray(bone['fittedOriginMeters']) + shift)
        maximum_origin_error = max(maximum_origin_error, float(np.linalg.norm(world(index) - expected)))
    if maximum_origin_error > 2e-6:
        raise ValueError(f'Bone origins changed: {maximum_origin_error} m')
    if len(document['meshes']) != 1 or len(document['materials']) != len(payload['artwork']['materials']):
        raise ValueError('Unexpected mesh or material count')
    for actual, source in zip(document['materials'], payload['artwork']['materials'], strict=True):
        if actual['name'] != source['name'] or not np.allclose(actual['pbrMetallicRoughness']['baseColorFactor'], source['inputs']['Base Color'], atol=2e-6):
            raise ValueError(f"Material changed: {source['name']}")
    mesh_index = next(i for i, node in enumerate(nodes) if 'mesh' in node)
    mesh_node = nodes[mesh_index]
    mesh_world = world_matrix(mesh_index)
    skin = document['skins'][mesh_node['skin']]
    inverse_binds = accessor(document, binary, skin['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    for index, inverse in zip(skin['joints'], inverse_binds, strict=True):
        if not np.allclose(world_matrix(index) @ inverse, mesh_world, atol=2e-6):
            raise ValueError(f"Inverse bind mismatch: {nodes[index]['name']}")
    actual_groups = {}
    triangle_count = 0
    for primitive in document['meshes'][0]['primitives']:
        attributes = primitive['attributes']
        positions = accessor(document, binary, attributes['POSITION'])
        positions = positions @ mesh_world[:3, :3].T + mesh_world[:3, 3]
        weights = accessor(document, binary, attributes['WEIGHTS_0'])
        joints = accessor(document, binary, attributes['JOINTS_0'])
        if not np.allclose(np.sort(weights, axis=1), [0, 0, 0, 1]):
            raise ValueError('Artwork lost rigid single-bone weights')
        selected = joints[np.arange(len(joints)), weights.argmax(axis=1)]
        for joint in np.unique(selected):
            name = nodes[skin['joints'][int(joint)]]['name']
            actual_groups.setdefault(name, []).append(positions[selected == joint])
        triangle_count += accessor(document, binary, primitive['indices']).size // 3
    expected_triangles = sum(len(part['indices']) // 3 for part in payload['artwork']['parts'])
    unique_triangles = 0
    for part in payload['artwork']['parts']:
        _, canonical = np.unique(np.asarray(part['positions']).reshape(-1, 3), axis=0, return_inverse=True)
        faces = np.sort(canonical[np.asarray(part['indices']).reshape(-1, 3)], axis=1)
        unique_triangles += len(np.unique(faces, axis=0))
    # Blender's VRM1/glTF path removes an existing duplicate skull triangle.
    # Allow duplicate elimination only; surface coordinates are still compared.
    if triangle_count not in (expected_triangles, unique_triangles):
        raise ValueError('Triangle count changed')
    bones = {bone['name']: bone for bone in payload['bones']}
    maximum_vertex_error = 0.
    for part in payload['artwork']['parts']:
        name = part['name']
        bone = bones[name]
        w, x, y, z = bone['orientation']
        rotation = Rotation.from_quat([x, y, z, w])
        positions = np.asarray(part['positions']).reshape(-1, 3)[np.unique(part['indices'])]
        expected = vrm0_position(rotation.apply(positions) * bone['artworkScaleMeters'] + bone['fittedOriginMeters'] + shift)
        actual = np.concatenate(actual_groups.pop(name))
        # Both directions: catch omitted surface vertices as well as new ones.
        error = max(cKDTree(expected).query(actual)[0].max(), cKDTree(actual).query(expected)[0].max())
        maximum_vertex_error = max(maximum_vertex_error, float(error))
    if actual_groups or maximum_vertex_error > 2e-6:
        raise ValueError(f'Articulated artwork changed: {maximum_vertex_error} m')
    return dict(vrmSha256=hashlib.sha256(vrm_path.read_bytes()).hexdigest(),
                specVersion=version, humanoidMappings=len(bindings), forgeBones=len(bones),
                triangles=triangle_count, materials=len(document['materials']),
                duplicateTrianglesElided=expected_triangles-triangle_count,
                normalizedNodeTransforms=True, rigidWeightsAndInverseBinds=True,
                maximumOriginErrorMeters=maximum_origin_error,
                maximumArtworkErrorMeters=maximum_vertex_error, userReceiverAcceptance=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vrm', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--build-report', type=Path, required=True)
    args = parser.parse_args()
    report = validate(args.vrm, json.loads(args.input.read_text(encoding='utf-8')),
                      json.loads(args.build_report.read_text(encoding='utf-8')))
    args.vrm.with_suffix('.validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))
