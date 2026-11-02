"""Prepare a Blender-independent avatar input using installed public Forge APIs.

Run with a host Python that already provides skellyforge; Blender does not need
Forge or Core. Artwork is an explicit fitted input, never a sibling-path import.
Humanoid names are the VRM 0.x presentation vocabulary [@vrm0Specification].
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from skellyforge.core.skeleton.skeleton_definition import SkeletonDefinition
from skellyforge.core.skeleton.pose.rest_pose import RestPose


def humanoid_bindings() -> dict[str, str]:
    """VRM names to existing Forge segment names; not a second skeleton."""
    result = dict(hips='pelvis', spine='sacrolumbar', chest='thoracic',
                  neck='cervical_spine', head='skull')
    for side in ('left', 'right'):
        for target, source in (
            ('Shoulder', 'clavicle'), ('UpperArm', 'upper_arm'),
            ('LowerArm', 'lower_arm'), ('Hand', 'carpals'),
            ('UpperLeg', 'upper_leg'), ('LowerLeg', 'lower_leg'),
            ('Foot', 'foot'), ('Toes', 'toes'),
        ):
            result[side + target] = f'{side}_{source}'
        for digit, target in (('thumb', 'Thumb'), ('index', 'Index'),
                              ('middle', 'Middle'), ('ring', 'Ring'), ('pinky', 'Little')):
            sources = ('metacarpal', 'proximal_phalanx', 'distal_phalanx') if digit == 'thumb' else (
                'proximal_phalanx', 'middle_phalanx', 'distal_phalanx')
            for phalanx, source in zip(('Proximal', 'Intermediate', 'Distal'), sources, strict=True):
                result[side + target + phalanx] = f'{side}_{digit}_{source}'
    return result


def prepare(artwork_path: Path, height_m: float) -> dict:
    if not np.isfinite(height_m) or height_m <= 0:
        raise ValueError('Body-height scale must be positive meters')
    artwork = json.loads(artwork_path.read_text(encoding='utf-8'))
    if artwork['coordinateSystem'] != 'blender_x_right_y_forward_z_up':
        raise ValueError('Unsupported artwork coordinate system')
    skeleton = SkeletonDefinition.from_default_yaml()
    rest = RestPose.from_default_yaml(skeleton=skeleton)
    # Refuse stale fitted artwork, rather than silently fitting another model.
    for name, point in artwork['landmarks'].items():
        if not np.allclose(point, rest.landmark_positions[name].array, atol=1e-9, rtol=0):
            raise ValueError(f'Artwork/model landmark mismatch: {name}')
    for part in artwork['parts']:
        name = part['name']
        if not np.allclose(part['restOrientation'], rest.segment_orientations[name].as_array(), atol=1e-9):
            raise ValueError(f'Artwork/model rest orientation mismatch: {name}')
        if part['parent'] != rest.parents[name]:
            raise ValueError(f'Artwork/model hierarchy mismatch: {name}')
    mapping = humanoid_bindings()
    if not set(mapping.values()).issubset(skeleton.segments):
        raise ValueError('Humanoid binding references an absent Forge segment')
    bones = [dict(name=name, parent=rest.parents[name],
                  origin=rest.segment_origins[name].array.tolist(),
                  orientation=rest.segment_orientations[name].as_array().tolist(),
                  length=segment.length)
             for name, segment in skeleton.segments.items()]
    # Standard VMC local transforms address the immediate humanoid parent.
    # Keep source topology in `bones`; only the presentation rig skips unmapped
    # intermediaries for mapped joints. Metacarpal artwork bones remain present.
    avatar_parents = dict(rest.parents)
    mapped_segments = set(mapping.values())
    for name in mapped_segments:
        parent = avatar_parents[name]
        while parent is not None and parent not in mapped_segments:
            parent = rest.parents[parent]
        avatar_parents[name] = parent
    return dict(version=1, coordinateSystem=artwork['coordinateSystem'],
                authoredUnit='body_height', bodyHeightMeters=height_m,
                artworkSha256=hashlib.sha256(artwork_path.read_bytes()).hexdigest(),
                humanoid=mapping, bones=bones, avatarParents=avatar_parents, artwork=artwork)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artwork', type=Path, required=True)
    parser.add_argument('--height-m', type=float, default=1.75)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    payload = prepare(args.artwork, args.height_m)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, separators=(',', ':')), encoding='utf-8')
    print(f"Prepared {len(payload['bones'])} Forge bones and {len(payload['humanoid'])} humanoid mappings")
