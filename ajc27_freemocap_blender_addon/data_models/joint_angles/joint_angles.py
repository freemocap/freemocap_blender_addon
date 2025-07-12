joint_angles = {
    'left_elbow_extension_flexion' : {
        'segment': 'left_arm',
        'joint_center': 'left_elbow',
        'reference_vector': {
            'reference_vector_origin': 'left_elbow',
            'reference_vector_end': 'left_shoulder',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_elbow',
            'rotation_vector_end': 'left_wrist',
        },
    },
    'left_shoulder_extension_flexion' : {
        'segment': 'left_arm',
        'joint_center': 'left_shoulder',
        'reference_vector': {
            'reference_vector_origin': 'neck_center',
            'reference_vector_end': 'trunk_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_shoulder',
            'rotation_vector_end': {
                'projected_vector_origin': 'left_shoulder',
                'projected_vector_end': 'left_elbow',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'neck_center',
                        'plane_axis_1_end': 'trunk_center',
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'neck_center',
                        'plane_axis_2_cross_1_end': 'trunk_center',
                        'plane_axis_2_cross_2_origin': 'neck_center',
                        'plane_axis_2_cross_2_end': 'left_shoulder',
                    },
                }
            }
            
        },
    },
    # 'spine_extension_flexion' : {
    #     'segment': 'spine',
    #     'spine_extension': 0.0,
    #     'spine_flexion': 0.0
    # },
    # 'spine_lateral_flexion' : {
    #     'segment': 'spine',
    #     'spine_lateral_flexion': 0.0
    # },
    # 'neck_extension_flexion' : {
    #     'segment': 'neck',
    #     'neck_extension': 0.0,
    #     'neck_flexion': 0.0
    # },
    # 'neck_lateral_flexion' : {
    #     'segment': 'neck',
    #     'neck_lateral_flexion': 0.0
    # },
    # 'neck_rotation' : {
    #     'segment': 'neck',
    #     'neck_rotation': 0.0
    # },
}