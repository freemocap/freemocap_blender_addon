"""Replay decoded VMC fixtures through actual VRM skin/joint data, without Unity.

Models the published VRM0 ReverseZ/VRM1 ReverseX importers and direct local-transform
receiver [@vseeFacePreviewNodeImporter; @uniVrm1ImportAxis; @vseeFaceLocalReceiver].
This is not a live VSeeFace test or a general VRM1 retargeter.
Fixtures are explicit cross-repository inputs; this tool does not import Core.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

from validate_skelly_vrm import accessor, load_glb


def replay(path, payload, fixtures, *, apply_positions=True):
    document, binary = load_glb(path)
    nodes = document['nodes']
    parents = {child: i for i, node in enumerate(nodes) for child in node.get('children', [])}
    # Independent receiver convention: VRM0 reverses Z, VRM1 reverses X. Do not derive it from
    # the producer's sourceToFile matrix, which would conceal the original bug.
    version = payload.get('vrmVersion', '0.0')
    reverse = np.diag([1., 1., -1., 1.] if version == '0.0' else [-1., 1., 1., 1.])
    source_to_unity = np.asarray(payload['coordinateBindings']['sourceToReceiver'])
    if version == '0.0':
        bindings = {item['node']: item['bone'][0].upper() + item['bone'][1:]
                    for item in document['extensions']['VRM']['humanoid']['humanBones']}
    else:
        # File-format thumb vocabulary differs; VMC still uses Unity names.
        bindings = {}
        for name, item in document['extensions']['VRMC_vrm']['humanoid']['humanBones'].items():
            if 'ThumbMetacarpal' in name:
                name = name.replace('ThumbMetacarpal', 'ThumbProximal')
            elif 'ThumbProximal' in name:
                name = name.replace('ThumbProximal', 'ThumbIntermediate')
            bindings[item['node']] = name[0].upper() + name[1:]
    bone_by_name = {item['name']: item for item in payload['bones']}
    parts = {part['name']: part for part in payload['artwork']['parts']}
    skin = document['skins'][0]
    inverse_binds = accessor(document, binary, skin['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    inverse_binds = reverse @ inverse_binds @ reverse
    primitive_data = []
    for primitive in document['meshes'][0]['primitives']:
        attrs = primitive['attributes']
        vertices = accessor(document, binary, attrs['POSITION']) @ reverse[:3, :3]
        weights = accessor(document, binary, attrs['WEIGHTS_0'])
        joints = accessor(document, binary, attrs['JOINTS_0'])
        primitive_data.append((vertices, joints[np.arange(len(joints)), weights.argmax(axis=1)]))
    results = []
    for case in fixtures:
        locals_by_node = {}
        for index, node in enumerate(nodes):
            local = np.eye(4)
            local[:3, 3] = np.asarray(node.get('translation', [0, 0, 0])) @ reverse[:3, :3]
            if index in bindings and bindings[index] in case['bones']:
                message = case['bones'][bindings[index]]
                local[:3, :3] = Rotation.from_quat(message['local_quaternion_xyzw']).as_matrix()
                # The rotations-only diagnostic aligns the hips to isolate
                # proportional/attachment error from placement of the avatar.
                if apply_positions or bindings[index] == 'Hips':
                    local[:3, 3] = message['local_position_m']
            locals_by_node[index] = local
        world = {}

        def resolve(index):
            if index not in world:
                world[index] = resolve(parents[index]) @ locals_by_node[index] if index in parents else locals_by_node[index].copy()
                if index not in parents:
                    world[index][:3, 3] += case['root_position_m']
            return world[index]

        actual = {}
        for positions, joint_indices in primitive_data:
            for joint in np.unique(joint_indices):
                index = skin['joints'][int(joint)]
                transform = resolve(index) @ inverse_binds[int(joint)]
                posed = positions[joint_indices == joint] @ transform[:3, :3].T + transform[:3, 3]
                actual.setdefault(nodes[index]['name'], []).append(posed)
        source = {name: (np.asarray(origin) / 1000., Rotation.from_quat([q[1], q[2], q[3], q[0]]).as_matrix())
                  for name, origin, q in zip(case['source_segment_names'], case['source_origins_mm'],
                                             case['source_world_quaternions_wxyz'], strict=True)
                  if np.isfinite(np.asarray(origin, dtype=float)).all() and np.isfinite(np.asarray(q, dtype=float)).all()}
        lengths = dict(zip(case['source_segment_names'], case.get('source_segment_lengths_mm', [])))
        errors, viewport_errors = {}, {}
        for name, part in parts.items():
            if name not in source:
                continue
            origin, orientation = source[name]
            vertices = np.asarray(part['positions']).reshape(-1, 3)[np.unique(part['indices'])]
            received = np.concatenate(actual[name])
            if name in lengths:
                scale = float(np.asarray(lengths[name]).reshape(-1)[0]) / part['authoredLength'] / 1000.
                viewport = (vertices @ orientation.T * scale + origin) @ source_to_unity.T
                viewport_errors[name] = float(max(cKDTree(viewport).query(received)[0].max(), cKDTree(received).query(viewport)[0].max()))
            if name not in payload['humanoid'].values():
                # Unmapped metacarpal artwork follows Hand at avatar proportions;
                # standard VMC sends neither its separate translation nor curl.
                parent = bone_by_name[name]['parent']
                parent_origin, parent_rotation = source[parent]
                parent_rest = bone_by_name[parent]
                w, x, y, z = parent_rest['orientation']
                delta = parent_rotation @ Rotation.from_quat([x, y, z, w]).as_matrix().T
                origin = parent_origin + delta @ (np.asarray(bone_by_name[name]['fittedOriginMeters']) - parent_rest['fittedOriginMeters'])
                w, x, y, z = bone_by_name[name]['orientation']
                orientation = delta @ Rotation.from_quat([x, y, z, w]).as_matrix()
            expected = (vertices @ orientation.T * bone_by_name[name]['artworkScaleMeters'] + origin) @ source_to_unity.T
            errors[name] = float(max(cKDTree(expected).query(received)[0].max(), cKDTree(received).query(expected)[0].max()))
        results.append(dict(armElevationDegrees=case.get('arm_elevation_degrees'),
                            maximumArtworkErrorMeters=max(errors.values()),
                            partsChecked=len(errors), errorsByPart=errors,
                            viewportErrorsByPart=viewport_errors))
    return dict(file=str(path), applyPositions=apply_positions, hipsAnchoredToSource=True, cases=results,
                passed=all(item['maximumArtworkErrorMeters'] < 3e-6 for item in results))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vrm', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    report = replay(args.vrm, json.loads(args.input.read_text(encoding='utf-8')),
                    json.loads(args.fixtures.read_text(encoding='utf-8'))['fixtures'])
    args.report.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({**report, 'cases': [{key: value for key, value in item.items() if key != 'errorsByPart'} for item in report['cases']]}))
    raise SystemExit(not report['passed'])
