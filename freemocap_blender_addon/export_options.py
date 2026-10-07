"""Route capabilities and validation, usable outside Blender."""
CAPABILITIES = {
    'legacy_npy': dict(formats=['fbx', 'bvh'], rest_poses=['tpose', 'apose'], animation_cleanup=True),
    'parquet_constraints': dict(formats=['fbx'], rest_poses=['tpose', 'apose'], animation_cleanup=True),
    'parquet_segments': dict(formats=['fbx'], rest_poses=['tpose'], animation_cleanup=False),
}


def parquet_options(route, config):
    if not isinstance(config, dict):
        raise ValueError('Parquet export options must be a dictionary')
    allowed = {'export_3d_model': {'formats'}, 'add_rig': {'rest_pose'},
               'motion_cleanup': {'apply_foot_locking', 'limit_hand_markers_range_of_motion'}}
    for section, values in config.items():
        if section not in allowed or not isinstance(values, dict) or set(values) - allowed[section]:
            raise ValueError('Unsupported Parquet export configuration section/options: ' + section)
    formats = config.get('export_3d_model', {}).get('formats', [])
    pose = config.get('add_rig', {}).get('rest_pose', 'tpose')
    cleanup = config.get('motion_cleanup', {})
    capability = CAPABILITIES[route]
    if not isinstance(formats, list) or any(f not in capability['formats'] for f in formats):
        raise ValueError(route + ' supports model formats: ' + repr(capability['formats']))
    if pose not in capability['rest_poses']:
        raise ValueError(route + ' supports rest poses: ' + repr(capability['rest_poses']))
    if any(type(v) is not bool for v in cleanup.values()):
        raise ValueError('Animation cleanup options must be booleans')
    if any(cleanup.values()) and not capability['animation_cleanup']:
        raise ValueError('Saved segment poses do not support trajectory cleanup; use parquet_constraints')
    return dict(formats=formats, rest_pose=pose,
                foot_locking=cleanup.get('apply_foot_locking', False),
                hand_limits=cleanup.get('limit_hand_markers_range_of_motion', False))
