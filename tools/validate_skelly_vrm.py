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
    vrm = document['extensions']['VRM']
    if vrm['specVersion'] != '0.0':
        raise ValueError('VSeeFace deliverable must use VRM0')
    nodes = document['nodes']
    indices = {node['name']: i for i, node in enumerate(nodes)}
    bindings = {bone['bone']: nodes[bone['node']]['name'] for bone in vrm['humanoid']['humanBones']}
    if bindings != payload['humanoid']:
        raise ValueError('Exported humanoid bindings differ from the build input')
    parents = {child: i for i, node in enumerate(nodes) for child in node.get('children', [])}
    for node in nodes:
        if 'matrix' in node or not np.allclose(node.get('rotation', [0, 0, 0, 1]), [0, 0, 0, 1]) or not np.allclose(node.get('scale', [1, 1, 1]), 1):
            raise ValueError('Expected VRM0 normalized nodes')

    def world(index):
        value = np.asarray(nodes[index].get('translation', [0, 0, 0]), dtype=float)
        return value + world(parents[index]) if index in parents else value

    def vrm0_position(points):
        # Official VRM0 exporter boundary, distinct from the Unity wire basis.
        return np.asarray(points)[..., [0, 2, 1]] * [-1, 1, 1]

    height = payload['bodyHeightMeters']
    shift = np.array([0, 0, build['floorOffsetMeters']])
    maximum_origin_error = 0.
    for bone in payload['bones']:
        index = indices[bone['name']]
        actual_parent = nodes[parents[index]]['name'] if index in parents else None
        if actual_parent != payload['avatarParents'][bone['name']]:
            raise ValueError(f"Hierarchy changed at {bone['name']}")
        expected = vrm0_position(np.asarray(bone['origin']) * height + shift)
        maximum_origin_error = max(maximum_origin_error, float(np.linalg.norm(world(index) - expected)))
    if maximum_origin_error > 2e-6:
        raise ValueError(f'Bone origins changed: {maximum_origin_error} m')
    if len(document['meshes']) != 1 or len(document['materials']) != len(payload['artwork']['materials']):
        raise ValueError('Unexpected mesh or material count')
    for actual, source in zip(document['materials'], payload['artwork']['materials'], strict=True):
        if actual['name'] != source['name'] or not np.allclose(actual['pbrMetallicRoughness']['baseColorFactor'], source['inputs']['Base Color'], atol=2e-6):
            raise ValueError(f"Material changed: {source['name']}")
    mesh_node = next(node for node in nodes if 'mesh' in node)
    skin = document['skins'][mesh_node['skin']]
    inverse_binds = accessor(document, binary, skin['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    for index, inverse in zip(skin['joints'], inverse_binds, strict=True):
        matrix = np.eye(4)
        matrix[:3, 3] = world(index)
        if not np.allclose(matrix @ inverse, np.eye(4), atol=2e-6):
            raise ValueError(f"Inverse bind mismatch: {nodes[index]['name']}")
    actual_groups = {}
    triangle_count = 0
    for primitive in document['meshes'][0]['primitives']:
        attributes = primitive['attributes']
        positions = accessor(document, binary, attributes['POSITION'])
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
    if triangle_count != expected_triangles:
        raise ValueError('Triangle count changed')
    bones = {bone['name']: bone for bone in payload['bones']}
    maximum_vertex_error = 0.
    for part in payload['artwork']['parts']:
        name = part['name']
        bone = bones[name]
        w, x, y, z = bone['orientation']
        rotation = Rotation.from_quat([x, y, z, w])
        positions = np.asarray(part['positions']).reshape(-1, 3)[np.unique(part['indices'])]
        expected = vrm0_position((rotation.apply(positions) + bone['origin']) * height + shift)
        actual = np.concatenate(actual_groups.pop(name))
        # Both directions: catch omitted surface vertices as well as new ones.
        error = max(cKDTree(expected).query(actual)[0].max(), cKDTree(actual).query(expected)[0].max())
        maximum_vertex_error = max(maximum_vertex_error, float(error))
    if actual_groups or maximum_vertex_error > 2e-6:
        raise ValueError(f'Articulated artwork changed: {maximum_vertex_error} m')
    return dict(vrmSha256=hashlib.sha256(vrm_path.read_bytes()).hexdigest(),
                specVersion='0.0', humanoidMappings=len(bindings), forgeBones=len(bones),
                triangles=triangle_count, materials=len(document['materials']),
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
