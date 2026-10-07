"""Editable Blender animation targets, separate from recorded trajectories."""
import numpy as np
from .scene_objects import descendants
from .get_fcurves_from_object_action import get_fcurves_from_object_action


def animation_targets(root, start_frame, end_frame):
    route = root.get('import_route', 'legacy_npy')
    if route == 'parquet_segments':
        raise ValueError('Animation cleanup requires a constraint-driven Blender skeleton. Load the Parquet constraints route; saved segment poses are preserved.')
    if route == 'parquet_constraints':
        targets = {o['legacy_target_name']: o for o in descendants(root) if 'legacy_target_name' in o}
    else:
        targets = {o.name: o for p in descendants(root) if p.type == 'EMPTY' and 'empties_parent' in p.name
                   for o in p.children if o.type == 'EMPTY'}
    result = {}
    for name, obj in targets.items():
        curves = get_fcurves_from_object_action(obj)
        if curves is None:
            continue
        location = [curves.find('location', index=i) for i in range(3)]
        if any(c is None for c in location):
            continue
        frames = [[k.co[0] for k in c.keyframe_points] for c in location]
        expected = list(range(len(frames[0])))
        if any(f != expected for f in frames):
            raise ValueError('Legacy animation cleanup currently requires dense zero-based keyframes; source frame numbers will not be rewritten')
        if start_frame != 0 or end_frame != len(expected) - 1:
            raise ValueError('Animation cleanup requires the full imported frame range')
        result[name] = dict(object=obj, fcurves=np.array([[k.co[1] for k in c.keyframe_points] for c in location]))
    if not result:
        raise ValueError('No editable constraint targets found in the selected recording')
    return result
