"""Portable asset convention, independent of Blender and the reconstruction stack."""


def canonical_asset(payload):
    """Convert the authored legacy asset (+X left, -Y forward) once at export.

    Roll hints are directions in the canonical asset/rest world, not segment
    axes. They complete the attachment frame where endpoints alone cannot.
    """
    if payload['schema_version'] != 1:
        raise ValueError('Expected original legacy asset')
    payload['vertices'] = [[-x, -y, z] for x, y, z in payload['vertices']]
    payload['schema_version'] = 2
    payload['coordinate_system'] = 'blender_x_right_y_forward_z_up'
    payload['attachment_frames'] = {
        name: dict(roll_reference=[0, 1, 0] if name in ('spine', 'spine.001', 'neck')
                   or name.startswith(('thigh.', 'shin.')) else [0, 0, 1])
        for name in payload['groups'] if name + '_origin' in payload['groups']
    }
    for part, landmark in {'face': 'head_vertex', 'pelvis': 'left_iliac_crest',
                           'spine.001': 'xiphoid_process'}.items():
        payload['attachment_frames'][part]['model_secondary_landmark'] = landmark
    return payload
