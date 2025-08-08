joint_angles = {
    'left_elbow_extension_flexion' : {
        'joint_center': 'left_elbow',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'left_shoulder',
            'reference_vector_end': 'left_elbow',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_elbow',
            'rotation_vector_end': 'left_wrist',
        },
    },
    'left_shoulder_extension_flexion' : {
        'joint_center': 'left_shoulder',
        'reference_vector': {
            'type': 'vector',
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
    'left_shoulder_abduction_adduction': {
        'joint_center': 'left_shoulder',
        'reference_vector': {
            'type': 'vector',
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
                        'type': 'vector',
                        'plane_axis_2_origin': 'neck_center',
                        'plane_axis_2_end': 'left_shoulder',
                    },
                }
            }
        },
    },
    'right_elbow_extension_flexion' : {
        'joint_center': 'right_elbow',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'right_shoulder',
            'reference_vector_end': 'right_elbow',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_elbow',
            'rotation_vector_end': 'right_wrist',
        },
    },
    'right_shoulder_extension_flexion' : {
        'joint_center': 'right_shoulder',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'neck_center',
            'reference_vector_end': 'trunk_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_shoulder',
            'rotation_vector_end': {
                'projected_vector_origin': 'right_shoulder',
                'projected_vector_end': 'right_elbow',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'neck_center',
                        'plane_axis_1_end': 'trunk_center',
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'neck_center',
                        'plane_axis_2_cross_1_end': 'right_shoulder',
                        'plane_axis_2_cross_2_origin': 'neck_center',
                        'plane_axis_2_cross_2_end': 'trunk_center',
                    },
                }
            }
        },
    },
    'right_shoulder_abduction_adduction': {
        'joint_center': 'right_shoulder',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'neck_center',
            'reference_vector_end': 'trunk_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_shoulder',
            'rotation_vector_end': {
                'projected_vector_origin': 'right_shoulder',
                'projected_vector_end': 'right_elbow',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'neck_center',
                        'plane_axis_1_end': 'trunk_center',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'neck_center',
                        'plane_axis_2_end': 'right_shoulder',
                    },
                }
            }
        },
    },
    'left_knee_extension_flexion' : {
        'joint_center': 'left_knee',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'left_hip',
            'reference_vector_end': 'left_knee',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_knee',
            'rotation_vector_end': 'left_ankle',
        },
    },
    'left_hip_extension_flexion' : {
        'joint_center': 'left_hip',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_hip',
            'rotation_vector_end': {
                'projected_vector_origin': 'left_hip',
                'projected_vector_end': 'left_knee',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'trunk_center',
                        'plane_axis_1_end': 'hips_center',
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'trunk_center',
                        'plane_axis_2_cross_1_end': 'hips_center',
                        'plane_axis_2_cross_2_origin': 'hips_center',
                        'plane_axis_2_cross_2_end': 'left_hip',
                    },
                }
            }
        },
    },
    'left_hip_abduction_adduction': {
        'joint_center': 'left_hip',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_hip',
            'rotation_vector_end': {
                'projected_vector_origin': 'left_hip',
                'projected_vector_end': 'left_knee',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'trunk_center',
                        'plane_axis_1_end': 'hips_center',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'hips_center',
                        'plane_axis_2_end': 'left_hip',
                    },
                }
            }
        },
    },
    # 'left_hip_rotation': {
    #     'joint_center': 'left_hip',
    #     'reference_vector': {
    #         'type': 'crossproduct',
    #         'reference_cross_1_origin': 'left_hip',
    #         'reference_cross_1_end': 'left_knee',
    #         'reference_cross_2_origin': 'hips_center',
    #         'reference_cross_2_end': 'left_hip',
    #     },
    #     'rotation_vector': {
    #         'rotation_vector_origin': 'left_hip',
    #         'rotation_vector_end': {
                  ## TODO: Improve the projection logic so it can work
                  ##       with a projected vector that it doesn't have
                  ##       the same origin as the rotion vector. Like
                  ##       the ankle-foot_index vector in this case
    #             'projected_vector_origin': 'left_hip',
    #             'projected_vector_end': 'left_foot_index',
    #             'projection_plane': {
    #                 'plane_axis_1': {
    #                     'type': 'vector',
    #                     'plane_axis_1_origin': 'hips_center',
    #                     'plane_axis_1_end': 'left_hip',
    #                 },
    #                 'plane_axis_2': {
    #                     'type': 'crossproduct',
    #                     'plane_axis_2_cross_1_origin': 'left_hip',
    #                     'plane_axis_2_cross_1_end': 'left_knee',
    #                     'plane_axis_2_cross_2_origin': 'hips_center',
    #                     'plane_axis_2_cross_2_end': 'left_hip',
    #                 },
    #             }
    #         }
    #     },
    # },
    'right_knee_extension_flexion' : {
        'joint_center': 'right_knee',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'right_hip',
            'reference_vector_end': 'right_knee',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_knee',
            'rotation_vector_end': 'right_ankle',
        },
    },
    'right_hip_extension_flexion' : {
        'joint_center': 'right_hip',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_hip',
            'rotation_vector_end': {
                'projected_vector_origin': 'right_hip',
                'projected_vector_end': 'right_knee',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'trunk_center',
                        'plane_axis_1_end': 'hips_center',
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'hips_center',
                        'plane_axis_2_cross_1_end': 'right_hip',
                        'plane_axis_2_cross_2_origin': 'trunk_center',
                        'plane_axis_2_cross_2_end': 'hips_center',
                    },
                }
            }
        },
    },
    'right_hip_abduction_adduction': {
        'joint_center': 'right_hip',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_hip',
            'rotation_vector_end': {
                'projected_vector_origin': 'right_hip',
                'projected_vector_end': 'right_knee',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'trunk_center',
                        'plane_axis_1_end': 'hips_center',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'hips_center',
                        'plane_axis_2_end': 'right_hip',
                    },
                }
            }
        },
    },
    'neck_extension_flexion' : {
        'joint_center': 'neck_center',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'neck_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'neck_center',
            'rotation_vector_end': {
                'projected_vector_origin': 'neck_center',
                'projected_vector_end': 'head_center',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'trunk_center',
                        'plane_axis_1_end': 'neck_center',
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'trunk_center',
                        'plane_axis_2_cross_1_end': 'neck_center',
                        'plane_axis_2_cross_2_origin': 'neck_center',
                        'plane_axis_2_cross_2_end': 'right_shoulder',
                    },
                }
            }
        },
    },
    'neck_lateral_flexion': {
        'joint_center': 'neck_center',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'neck_center',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'neck_center',
            'rotation_vector_end': {
                'projected_vector_origin': 'neck_center',
                'projected_vector_end': 'head_center',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'trunk_center',
                        'plane_axis_1_end': 'neck_center',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'neck_center',
                        'plane_axis_2_end': 'left_shoulder',
                    },
                }
            }
        },
    },
    'neck_rotation': {
        'joint_center': 'neck_center',
        'reference_vector': {
            'type': 'crossproduct',
            'reference_cross_1_origin': 'neck_center',
            'reference_cross_1_end': 'head_center',
            'reference_cross_2_origin': 'neck_center',
            'reference_cross_2_end': 'right_shoulder',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'neck_center',
            'rotation_vector_end': {
                'projected_vector_origin': 'neck_center',
                'projected_vector_end': 'nose',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'doublecrossproduct',
                        'plane_axis_1_cross_1_origin': 'neck_center',
                        'plane_axis_1_cross_1_end': 'head_center',
                        'plane_axis_1_cross_2_origin': 'neck_center',
                        'plane_axis_1_cross_2_end': 'right_shoulder',
                        'plane_axis_1_cross_3_origin': 'neck_center',
                        'plane_axis_1_cross_3_end': 'head_center',
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'neck_center',
                        'plane_axis_2_cross_1_end': 'right_shoulder',
                        'plane_axis_2_cross_2_origin': 'neck_center',
                        'plane_axis_2_cross_2_end': 'head_center',
                    },
                }
            }
        },
    },
    # TODO: Define a better reference vector and rotation plane because
    # when the leg is fully extended the thigh and shin bones might form
    # unwanted angles. The most obvious choice is to just use knee-ankle
    # and ankle-foot_index, but that ommits the other ankle rotations
    # TODO: Add an offset to the angle so it is 0º when it is on the a 
    # standing straight pose
    'left_ankle_dorsiflexion_plantarflexion' : {
        'joint_center': 'left_ankle',
        'reference_vector': {
            'type': 'doublecrossproduct',
                'reference_cross_1_origin': 'left_knee',
                'reference_cross_1_end': 'left_ankle',
                'reference_cross_2_origin': 'left_ankle',
                'reference_cross_2_end': 'left_foot_index',
                'reference_cross_3_origin': 'left_knee',
                'reference_cross_3_end': 'left_ankle',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_ankle',
            'rotation_vector_end': {
                'projected_vector_origin': 'left_ankle',
                'projected_vector_end': 'left_foot_index',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'left_knee',
                        'plane_axis_1_end': 'left_ankle',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'left_knee',
                        'plane_axis_2_end': 'left_foot_index',
                    },
                }
            }
        },
    },
    'left_ankle_inversion_eversion' : {
        'joint_center': 'left_ankle',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'left_knee',
            'reference_vector_end': 'left_ankle',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_ankle',
            'rotation_vector_end': {
                'projected_vector_origin': 'left_ankle',
                'projected_vector_end': 'left_heel',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'crossproduct',
                        'plane_axis_1_cross_1_origin': 'left_hip',
                        'plane_axis_1_cross_1_end': 'left_knee',
                        'plane_axis_1_cross_2_origin': 'left_knee',
                        'plane_axis_1_cross_2_end': 'left_ankle',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'left_knee',
                        'plane_axis_2_end': 'left_ankle',
                    },
                }
            }
        },
    },
    'right_ankle_dorsiflexion_plantarflexion' : {
        'joint_center': 'right_ankle',
        'reference_vector': {
            'type': 'doublecrossproduct',
                'reference_cross_1_origin': 'right_knee',
                'reference_cross_1_end': 'right_ankle',
                'reference_cross_2_origin': 'right_ankle',
                'reference_cross_2_end': 'right_foot_index',
                'reference_cross_3_origin': 'right_knee',
                'reference_cross_3_end': 'right_ankle',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_ankle',
            'rotation_vector_end': {
                'projected_vector_origin': 'right_ankle',
                'projected_vector_end': 'right_foot_index',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'right_knee',
                        'plane_axis_1_end': 'right_ankle',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'right_knee',
                        'plane_axis_2_end': 'right_foot_index',
                    },
                }
            }
        },
    },
    'right_ankle_inversion_eversion' : {
        'joint_center': 'right_ankle',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'right_knee',
            'reference_vector_end': 'right_ankle',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_ankle',
            'rotation_vector_end': {
                'projected_vector_origin': 'right_ankle',
                'projected_vector_end': 'right_heel',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'right_knee',
                        'plane_axis_1_end': 'right_ankle',
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'right_hip',
                        'plane_axis_2_cross_1_end': 'right_knee',
                        'plane_axis_2_cross_2_origin': 'right_knee',
                        'plane_axis_2_cross_2_end': 'right_ankle',
                    },
                }
            }
        },
    },
    # TODO: Find a better way to define the reference vector. As the pelvis
    # is only defined by two markers, it can be determined what is its
    # rotation in the Sagittal plane. The approach to use the average of the 
    # two thighs is an approximation when both legs are rotated equally
    # like when standing still.
    'spine_extension_flexion' : {
        'joint_center': 'hips_center',
        'reference_vector': {
            'type': 'average',
            'reference_average_1_origin': 'left_knee',
            'reference_average_1_end': 'left_hip',
            'reference_average_2_origin': 'right_knee',
            'reference_average_2_end': 'right_hip',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'hips_center',
            'rotation_vector_end': {
                'projected_vector_origin': 'hips_center',
                'projected_vector_end': 'trunk_center',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'average',
                        'plane_axis_1_average_1_origin': 'left_knee',
                        'plane_axis_1_average_1_end': 'left_hip',
                        'plane_axis_1_average_2_origin': 'right_knee',
                        'plane_axis_1_average_2_end': 'right_hip',
                    },
                    'plane_axis_2': {
                        'type': 'average_crossproduct',
                        'plane_axis_2_average_1_origin': 'left_knee',
                        'plane_axis_2_average_1_end': 'left_hip',
                        'plane_axis_2_average_2_origin': 'right_knee',
                        'plane_axis_2_average_2_end': 'right_hip',
                        'plane_axis_2_cross_1_origin': 'hips_center',
                        'plane_axis_2_cross_1_end': 'right_hip',                        
                    },
                }
            }
        },
    },
    # TODO: Same thing as spine flexion extension reference vector
    'spine_lateral_flexion' : {
        'joint_center': 'hips_center',
        'reference_vector': {
            'type': 'average',
            'reference_average_1_origin': 'left_knee',
            'reference_average_1_end': 'left_hip',
            'reference_average_2_origin': 'right_knee',
            'reference_average_2_end': 'right_hip',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'hips_center',
            'rotation_vector_end': {
                'projected_vector_origin': 'hips_center',
                'projected_vector_end': 'trunk_center',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'hips_center',
                        'plane_axis_1_end': 'left_hip',   
                    },
                    'plane_axis_2': {
                        'type': 'average',
                        'plane_axis_2_average_1_origin': 'left_knee',
                        'plane_axis_2_average_1_end': 'left_hip',
                        'plane_axis_2_average_2_origin': 'right_knee',
                        'plane_axis_2_average_2_end': 'right_hip',
                    },
                }
            }
        },
    },
    # TODO: Check the constraints of the hand. Mediapipe body hand markers
    # and hand markers are not aligned. Probably placed them at average position?
    'left_hand_extension_flexion' : {
        'joint_center': 'left_wrist',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'left_elbow',
            'reference_vector_end': 'left_wrist',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'left_wrist',
            'rotation_vector_end': {
                'projected_vector_origin': 'left_wrist',
                'projected_vector_end': 'left_hand_middle',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'vector',
                        'plane_axis_1_origin': 'left_elbow',
                        'plane_axis_1_end': 'left_wrist',   
                    },
                    'plane_axis_2': {
                        'type': 'crossproduct',
                        'plane_axis_2_cross_1_origin': 'left_elbow',
                        'plane_axis_2_cross_1_end': 'left_wrist',
                        'plane_axis_2_cross_2_origin': 'left_wrist',
                        'plane_axis_2_cross_2_end': 'left_hand_thumb_cmc',
                    },
                }
            }
        },
    },
    'right_hand_extension_flexion' : {
        'joint_center': 'right_wrist',
        'reference_vector': {
            'type': 'vector',
            'reference_vector_origin': 'right_elbow',
            'reference_vector_end': 'right_wrist',
        },
        'rotation_vector': {
            'rotation_vector_origin': 'right_wrist',
            'rotation_vector_end': {
                'projected_vector_origin': 'right_wrist',
                'projected_vector_end': 'right_hand_middle',
                'projection_plane': {
                    'plane_axis_1': {
                        'type': 'crossproduct',
                        'plane_axis_1_cross_1_origin': 'right_elbow',
                        'plane_axis_1_cross_1_end': 'right_wrist',
                        'plane_axis_1_cross_2_origin': 'right_wrist',
                        'plane_axis_1_cross_2_end': 'right_hand_thumb_cmc',
                    },
                    'plane_axis_2': {
                        'type': 'vector',
                        'plane_axis_2_origin': 'right_elbow',
                        'plane_axis_2_end': 'right_wrist',
                    },
                }
            }
        },
    },
}