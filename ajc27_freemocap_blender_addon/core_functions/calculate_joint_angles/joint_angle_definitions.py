from dataclasses import dataclass
from typing import Dict, Union

@dataclass
class ProjectionPlaneDefinition:
    axis1: Dict
    axis2: Dict

@dataclass
class ProjectedVectorDefinition:
    origin: str
    end: str
    projection_plane: ProjectionPlaneDefinition

@dataclass
class RotationVectorDefinition:
    origin: str
    end: Union[str, ProjectedVectorDefinition]

@dataclass
class JointAngleDefinition:
    joint_center: str
    reference_vector: Dict
    rotation_vector: RotationVectorDefinition
    zero_offset: float = 0.0 # value in degrees to offset the angle calculation in some cases like ankle angles

joint_angles_definitions = {
    'left_elbow_extension_flexion': JointAngleDefinition(
        joint_center='left_elbow',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'left_shoulder',
            'reference_vector_end': 'left_elbow',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_elbow',
            end='left_wrist'
        )
    ),
    'left_shoulder_extension_flexion': JointAngleDefinition(
        joint_center='left_shoulder',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'neck_center',
            'reference_vector_end': 'trunk_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_shoulder',
            end=ProjectedVectorDefinition(
                origin='left_shoulder',
                end='left_elbow',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'neck_center',
                        'plane_axis_end': 'trunk_center',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'neck_center',
                        'plane_axis_cross_1_end': 'trunk_center',
                        'plane_axis_cross_2_origin': 'neck_center',
                        'plane_axis_cross_2_end': 'left_shoulder',
                    },
                )
            )
        )
    ),
    'left_shoulder_abduction_adduction': JointAngleDefinition(
        joint_center='left_shoulder',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'neck_center',
            'reference_vector_end': 'trunk_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_shoulder',
            end=ProjectedVectorDefinition(
                origin='left_shoulder',
                end='left_elbow',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'neck_center',
                        'plane_axis_end': 'trunk_center',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'neck_center',
                        'plane_axis_end': 'left_shoulder',
                    },
                )
            )
        )
    ),
    'right_elbow_extension_flexion': JointAngleDefinition(
        joint_center='right_elbow',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'right_shoulder',
            'reference_vector_end': 'right_elbow',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_elbow',
            end='right_wrist'
        )
    ),
    'right_shoulder_extension_flexion': JointAngleDefinition(
        joint_center='right_shoulder',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'neck_center',
            'reference_vector_end': 'trunk_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_shoulder',
            end=ProjectedVectorDefinition(
                origin='right_shoulder',
                end='right_elbow',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'neck_center',
                        'plane_axis_end': 'trunk_center',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'neck_center',
                        'plane_axis_cross_1_end': 'right_shoulder',
                        'plane_axis_cross_2_origin': 'neck_center',
                        'plane_axis_cross_2_end': 'trunk_center',
                    },
                )
            )
        )
    ),
    'right_shoulder_abduction_adduction': JointAngleDefinition(
        joint_center='right_shoulder',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'neck_center',
            'reference_vector_end': 'trunk_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_shoulder',
            end=ProjectedVectorDefinition(
                origin='right_shoulder',
                end='right_elbow',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'neck_center',
                        'plane_axis_end': 'trunk_center',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'neck_center',
                        'plane_axis_end': 'right_shoulder',
                    },
                )
            )
        )
    ),
    'left_knee_extension_flexion': JointAngleDefinition(
        joint_center='left_knee',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'left_hip',
            'reference_vector_end': 'left_knee',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_knee',
            end='left_ankle'
        )
    ),
    'left_hip_extension_flexion': JointAngleDefinition(
        joint_center='left_hip',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_hip',
            end=ProjectedVectorDefinition(
                origin='left_hip',
                end='left_knee',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'trunk_center',
                        'plane_axis_end': 'hips_center',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'trunk_center',
                        'plane_axis_cross_1_end': 'hips_center',
                        'plane_axis_cross_2_origin': 'hips_center',
                        'plane_axis_cross_2_end': 'left_hip',
                    },
                )
            )
        )
    ),
    'left_hip_abduction_adduction': JointAngleDefinition(
        joint_center='left_hip',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_hip',
            end=ProjectedVectorDefinition(
                origin='left_hip',
                end='left_knee',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'trunk_center',
                        'plane_axis_end': 'hips_center',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'hips_center',
                        'plane_axis_end': 'left_hip',
                    },
                )
            )
        )
    ),
    'right_knee_extension_flexion': JointAngleDefinition(
        joint_center='right_knee',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'right_hip',
            'reference_vector_end': 'right_knee',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_knee',
            end='right_ankle'
        )
    ),
    'right_hip_extension_flexion': JointAngleDefinition(
        joint_center='right_hip',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_hip',
            end=ProjectedVectorDefinition(
                origin='right_hip',
                end='right_knee',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'trunk_center',
                        'plane_axis_end': 'hips_center',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'hips_center',
                        'plane_axis_cross_1_end': 'right_hip',
                        'plane_axis_cross_2_origin': 'trunk_center',
                        'plane_axis_cross_2_end': 'hips_center',
                    },
                )
            )
        )
    ),
    'right_hip_abduction_adduction': JointAngleDefinition(
        joint_center='right_hip',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'hips_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_hip',
            end=ProjectedVectorDefinition(
                origin='right_hip',
                end='right_knee',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'trunk_center',
                        'plane_axis_end': 'hips_center',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'hips_center',
                        'plane_axis_end': 'right_hip',
                    },
                )
            )
        )
    ),
    'neck_extension_flexion': JointAngleDefinition(
        joint_center='neck_center',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'neck_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='neck_center',
            end=ProjectedVectorDefinition(
                origin='neck_center',
                end='head_center',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'trunk_center',
                        'plane_axis_end': 'neck_center',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'trunk_center',
                        'plane_axis_cross_1_end': 'neck_center',
                        'plane_axis_cross_2_origin': 'neck_center',
                        'plane_axis_cross_2_end': 'right_shoulder',
                    },
                )
            )
        )
    ),
    'neck_lateral_flexion': JointAngleDefinition(
        joint_center='neck_center',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'trunk_center',
            'reference_vector_end': 'neck_center',
        },
        rotation_vector=RotationVectorDefinition(
            origin='neck_center',
            end=ProjectedVectorDefinition(
                origin='neck_center',
                end='head_center',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'trunk_center',
                        'plane_axis_end': 'neck_center',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'neck_center',
                        'plane_axis_end': 'left_shoulder',
                    },
                )
            )
        )
    ),
    'neck_rotation': JointAngleDefinition(
        joint_center='neck_center',
        reference_vector={
            'type': 'crossproduct',
            'reference_cross_1_origin': 'neck_center',
            'reference_cross_1_end': 'head_center',
            'reference_cross_2_origin': 'neck_center',
            'reference_cross_2_end': 'right_shoulder',
        },
        rotation_vector=RotationVectorDefinition(
            origin='neck_center',
            end=ProjectedVectorDefinition(
                origin='neck_center',
                end='nose',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'doublecrossproduct',
                        'plane_axis_cross_1_origin': 'neck_center',
                        'plane_axis_cross_1_end': 'head_center',
                        'plane_axis_cross_2_origin': 'neck_center',
                        'plane_axis_cross_2_end': 'right_shoulder',
                        'plane_axis_cross_3_origin': 'neck_center',
                        'plane_axis_cross_3_end': 'head_center',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'neck_center',
                        'plane_axis_cross_1_end': 'right_shoulder',
                        'plane_axis_cross_2_origin': 'neck_center',
                        'plane_axis_cross_2_end': 'head_center',
                    },
                )
            )
        )
    ),
    'left_ankle_dorsiflexion_plantarflexion': JointAngleDefinition(
        joint_center='left_ankle',
        reference_vector={
            'type': 'doublecrossproduct',
            'reference_cross_1_origin': 'left_knee',
            'reference_cross_1_end': 'left_ankle',
            'reference_cross_2_origin': 'left_ankle',
            'reference_cross_2_end': 'left_foot_index',
            'reference_cross_3_origin': 'left_knee',
            'reference_cross_3_end': 'left_ankle',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_ankle',
            end=ProjectedVectorDefinition(
                origin='left_ankle',
                end='left_foot_index',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'left_knee',
                        'plane_axis_end': 'left_ankle',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'left_knee',
                        'plane_axis_end': 'left_foot_index',
                    },
                )
            )
        ),
        zero_offset=18.0  # Offset to make the zero value when standing still
    ),
    'left_ankle_inversion_eversion': JointAngleDefinition(
        joint_center='left_ankle',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'left_knee',
            'reference_vector_end': 'left_ankle',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_ankle',
            end=ProjectedVectorDefinition(
                origin='left_ankle',
                end='left_heel',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'left_hip',
                        'plane_axis_cross_1_end': 'left_knee',
                        'plane_axis_cross_2_origin': 'left_knee',
                        'plane_axis_cross_2_end': 'left_ankle',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'left_knee',
                        'plane_axis_end': 'left_ankle',
                    },
                )
            )
        )
    ),
    'right_ankle_dorsiflexion_plantarflexion': JointAngleDefinition(
        joint_center='right_ankle',
        reference_vector={
            'type': 'doublecrossproduct',
            'reference_cross_1_origin': 'right_knee',
            'reference_cross_1_end': 'right_ankle',
            'reference_cross_2_origin': 'right_ankle',
            'reference_cross_2_end': 'right_foot_index',
            'reference_cross_3_origin': 'right_knee',
            'reference_cross_3_end': 'right_ankle',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_ankle',
            end=ProjectedVectorDefinition(
                origin='right_ankle',
                end='right_foot_index',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'right_knee',
                        'plane_axis_end': 'right_ankle',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'right_knee',
                        'plane_axis_end': 'right_foot_index',
                    },
                )
            )
        ),
        zero_offset=18.0  # Offset to make the zero value when standing still
    ),
    'right_ankle_inversion_eversion': JointAngleDefinition(
        joint_center='right_ankle',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'right_knee',
            'reference_vector_end': 'right_ankle',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_ankle',
            end=ProjectedVectorDefinition(
                origin='right_ankle',
                end='right_heel',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'right_knee',
                        'plane_axis_end': 'right_ankle',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'right_hip',
                        'plane_axis_cross_1_end': 'right_knee',
                        'plane_axis_cross_2_origin': 'right_knee',
                        'plane_axis_cross_2_end': 'right_ankle',
                    },
                )
            )
        )
    ),
    'spine_extension_flexion': JointAngleDefinition(
        joint_center='hips_center',
        reference_vector={
            'type': 'average',
            'reference_average_1_origin': 'left_knee',
            'reference_average_1_end': 'left_hip',
            'reference_average_2_origin': 'right_knee',
            'reference_average_2_end': 'right_hip',
        },
        rotation_vector=RotationVectorDefinition(
            origin='hips_center',
            end=ProjectedVectorDefinition(
                origin='hips_center',
                end='trunk_center',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'average',
                        'plane_axis_average_1_origin': 'left_knee',
                        'plane_axis_average_1_end': 'left_hip',
                        'plane_axis_average_2_origin': 'right_knee',
                        'plane_axis_average_2_end': 'right_hip',
                    },
                    axis2={
                        'type': 'average_crossproduct',
                        'plane_axis_average_1_origin': 'left_knee',
                        'plane_axis_average_1_end': 'left_hip',
                        'plane_axis_average_2_origin': 'right_knee',
                        'plane_axis_average_2_end': 'right_hip',
                        'plane_axis_cross_1_origin': 'hips_center',
                        'plane_axis_cross_1_end': 'right_hip',
                    },
                )
            )
        )
    ),
    'spine_lateral_flexion': JointAngleDefinition(
        joint_center='hips_center',
        reference_vector={
            'type': 'average',
            'reference_average_1_origin': 'left_knee',
            'reference_average_1_end': 'left_hip',
            'reference_average_2_origin': 'right_knee',
            'reference_average_2_end': 'right_hip',
        },
        rotation_vector=RotationVectorDefinition(
            origin='hips_center',
            end=ProjectedVectorDefinition(
                origin='hips_center',
                end='trunk_center',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'hips_center',
                        'plane_axis_end': 'left_hip',
                    },
                    axis2={
                        'type': 'average',
                        'plane_axis_average_1_origin': 'left_knee',
                        'plane_axis_average_1_end': 'left_hip',
                        'plane_axis_average_2_origin': 'right_knee',
                        'plane_axis_average_2_end': 'right_hip',
                    },
                )
            )
        )
    ),
    'left_hand_extension_flexion': JointAngleDefinition(
        joint_center='left_wrist',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'left_elbow',
            'reference_vector_end': 'left_wrist',
        },
        rotation_vector=RotationVectorDefinition(
            origin='left_wrist',
            end=ProjectedVectorDefinition(
                origin='left_wrist',
                end='left_hand_middle',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'vector',
                        'plane_axis_origin': 'left_elbow',
                        'plane_axis_end': 'left_wrist',
                    },
                    axis2={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'left_elbow',
                        'plane_axis_cross_1_end': 'left_wrist',
                        'plane_axis_cross_2_origin': 'left_wrist',
                        'plane_axis_cross_2_end': 'left_hand_thumb_cmc',
                    },
                )
            )
        )
    ),
    'right_hand_extension_flexion': JointAngleDefinition(
        joint_center='right_wrist',
        reference_vector={
            'type': 'vector',
            'reference_vector_origin': 'right_elbow',
            'reference_vector_end': 'right_wrist',
        },
        rotation_vector=RotationVectorDefinition(
            origin='right_wrist',
            end=ProjectedVectorDefinition(
                origin='right_wrist',
                end='right_hand_middle',
                projection_plane=ProjectionPlaneDefinition(
                    axis1={
                        'type': 'crossproduct',
                        'plane_axis_cross_1_origin': 'right_elbow',
                        'plane_axis_cross_1_end': 'right_wrist',
                        'plane_axis_cross_2_origin': 'right_wrist',
                        'plane_axis_cross_2_end': 'right_hand_thumb_cmc',
                    },
                    axis2={
                        'type': 'vector',
                        'plane_axis_origin': 'right_elbow',
                        'plane_axis_end': 'right_wrist',
                    },
                )
            )
        )
    ),
}
