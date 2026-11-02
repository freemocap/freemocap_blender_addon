"""Prepare a Blender-independent avatar input using installed public Forge APIs.

Run with a host Python that already provides skellyforge; Blender does not need
Forge or Core. Artwork is an explicit fitted input, never a sibling-path import.
Humanoid names follow the selected VRM version [@vrm0Specification; @vrmAddon4103].
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from skellyforge.core.skeleton.skeleton_definition import SkeletonDefinition
from skellyforge.core.skeleton.pose.rest_pose import RestPose, build_rest_pose
from skellyforge.core.math.geometry.coordinate_systems import (
    AnatomicalDirection, CoordinateSystemConvention, CoordinateSystemRegistry,
    CoordinateSystemTransform,
)


def coordinate_bindings(vrm_version: str = '0.0') -> dict:
    """Versioned file/receiver boundary, using Forge's existing conversion API.

    Registry `vrm` is VRM1, not VRM0. UniVRM0 reverses Z on import, whereas
    UniVRM1 reverses X [@uniVrmCoordinateSystems]. The official Blender exporter
    consumes its own authoring-facing convention; adapt that input, not VMC.
    """
    registry = CoordinateSystemRegistry.from_default_yaml()
    vrm0 = CoordinateSystemConvention(
        name='vrm0', description='VRM0 file: +X right, +Y up, +Z backward',
        x_direction=AnatomicalDirection.RIGHT, y_direction=AnatomicalDirection.UP,
        z_direction=AnatomicalDirection.BACKWARD,
    )
    if vrm_version not in ('0.0', '1.0'):
        raise ValueError('Unsupported VRM version')
    target = vrm0 if vrm_version == '0.0' else registry.get(name='vrm')
    source = registry.get(name='blender')
    source_to_file = CoordinateSystemTransform(from_convention=source, to_convention=target).matrix
    # VRM0 uses the addon's (-X,Z,Y) converter. VRM1 delegates to Blender's
    # glTF exporter, whose Y-up conversion is (X,Z,-Y) [@blenderGltfJointExport].
    exporter_axes = registry.get(name='vrm') if vrm_version == '0.0' else vrm0
    exporter_to_source = CoordinateSystemTransform(from_convention=exporter_axes, to_convention=source).matrix
    return dict(fileConvention='vrm0' if vrm_version == '0.0' else 'vrm1',
                sourceToFile=source_to_file.tolist(),
                exporterOutputFromInput=exporter_to_source.T.tolist(),
                sourceToReceiver=CoordinateSystemTransform(from_convention=source,
                    to_convention=registry.get(name='unity')).matrix.tolist(),
                fileToReceiver=CoordinateSystemTransform(from_convention=target,
                    to_convention=registry.get(name='unity')).matrix.tolist(),
                exporterInputFromSource=(exporter_to_source @ source_to_file).tolist())


def humanoid_bindings(vrm_version: str = '0.0') -> dict[str, str]:
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
    if vrm_version == '1.0':
        for side in ('left', 'right'):
            metacarpal = result.pop(side + 'ThumbProximal')
            proximal = result.pop(side + 'ThumbIntermediate')
            result[side + 'ThumbMetacarpal'] = metacarpal
            result[side + 'ThumbProximal'] = proximal
    return result


def prepare(artwork_path: Path, height_m: float, vrm_version: str = '0.0',
            segment_scales_mm: dict[str, float] | None = None) -> dict:
    if not np.isfinite(height_m) or height_m <= 0:
        raise ValueError('Body-height scale must be positive meters')
    artwork = json.loads(artwork_path.read_text(encoding='utf-8'))
    if artwork['coordinateSystem'] != 'blender_x_right_y_forward_z_up':
        raise ValueError('Unsupported artwork coordinate system')
    skeleton = SkeletonDefinition.from_default_yaml()
    rest = RestPose.from_default_yaml(skeleton=skeleton)
    # This is the existing ModelScaleFit.segment_scales field, not a new fit.
    # Fit in source units first; convert the resulting presentation geometry to m.
    if segment_scales_mm is not None:
        if set(segment_scales_mm) != set(skeleton.segments):
            raise ValueError('Segment scales must cover exactly the authored skeleton')
        if any(not np.isfinite(value) or value <= 0 for value in segment_scales_mm.values()):
            raise ValueError('Segment scales must be finite positive millimeters')
        scales_m = {name: value / 1000. for name, value in segment_scales_mm.items()}
    else:
        scales_m = {name: height_m for name in skeleton.segments}
    _, fitted_origins, _ = build_rest_pose(
        skeleton=skeleton, parents=rest.parents, connect_ats=rest.connect_ats,
        orientations=rest.relative_orientations, segment_scales=scales_m)
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
    mapping = humanoid_bindings(vrm_version)
    if not set(mapping.values()).issubset(skeleton.segments):
        raise ValueError('Humanoid binding references an absent Forge segment')
    bones = [dict(name=name, parent=rest.parents[name],
                  origin=rest.segment_origins[name].array.tolist(),
                  orientation=rest.segment_orientations[name].as_array().tolist(),
                  length=segment.length,
                  fittedOriginMeters=fitted_origins[name].array.tolist(),
                  fittedLengthMeters=segment.length * scales_m[name],
                  artworkScaleMeters=scales_m[name])
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
    return dict(version=3, coordinateSystem=artwork['coordinateSystem'],
                vrmVersion=vrm_version, coordinateBindings=coordinate_bindings(vrm_version),
                authoredUnit='body_height', bodyHeightMeters=height_m,
                fitMode='recorded_segment_scales' if segment_scales_mm is not None else 'uniform_height',
                artworkSha256=hashlib.sha256(artwork_path.read_bytes()).hexdigest(),
                humanoid=mapping, bones=bones, avatarParents=avatar_parents, artwork=artwork)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artwork', type=Path, required=True)
    parser.add_argument('--height-m', type=float, default=1.75)
    parser.add_argument('--vrm-version', choices=('0.0', '1.0'), default='0.0')
    parser.add_argument('--segment-scales-mm', type=Path,
                        help='JSON mapping from existing ModelScaleFit.segment_scales in mm; overrides uniform height fitting')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    scales = json.loads(args.segment_scales_mm.read_text(encoding='utf-8')) if args.segment_scales_mm else None
    payload = prepare(args.artwork, args.height_m, args.vrm_version, scales)
    if args.segment_scales_mm:
        payload['fitSourceSha256'] = hashlib.sha256(args.segment_scales_mm.read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, separators=(',', ':')), encoding='utf-8')
    print(f"Prepared {len(payload['bones'])} Forge bones and {len(payload['humanoid'])} humanoid mappings")
