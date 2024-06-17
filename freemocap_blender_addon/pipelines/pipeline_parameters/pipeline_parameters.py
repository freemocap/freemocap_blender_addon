from dataclasses import dataclass, field
from enum import Enum

# from freemocap_blender_addon.models.animation.armatures.armature_types import ArmatureType
from freemocap_blender_addon.models.animation.armatures.rest_pose import PoseTypes


@dataclass
class AdjustEmptiesConfig:
    vertical_align_reference: str = "left_knee"
    vertical_align_angle_offset: float = 0.0
    ground_align_reference: str = "left_foot_index"
    vertical_align_position_offset: float = 0.0
    correct_fingers_empties: bool = True
    add_hand_middle_empty: bool = True


@dataclass
class ReduceBoneLengthDispersionConfig:
    interval_variable: str = "median"
    interval_factor: float = 0.0


@dataclass
class ReduceShakiness:
    recording_fps: float = 30.0


class AddRigMethods(Enum):
    RIGIFY = "rigify"
    BY_BONE = "by_bone"


@dataclass
class AddRigConfig:
    add_rig_method: AddRigMethods = AddRigMethods.BY_BONE
    # armature_type: ArmatureType = ArmatureType.FREEMOCAP
    pose_type: PoseTypes = PoseTypes.DEFAULT_TPOSE
    add_ik_constraints: bool = False
    keep_symmetry: bool = False
    add_fingers_constraints: bool = True
    use_limit_rotation: bool = False


@dataclass
class AddBodyMeshConfig:
    body_mesh_mode: str = "custom"


@dataclass
class PipelineConfig:
    adjust_empties: AdjustEmptiesConfig = field(default_factory=AdjustEmptiesConfig)
    reduce_bone_length_dispersion: ReduceBoneLengthDispersionConfig = field(
        default_factory=ReduceBoneLengthDispersionConfig)
    reduce_shakiness: ReduceShakiness = field(default_factory=ReduceShakiness)
    add_rig: AddRigConfig = field(default_factory=AddRigConfig)
    add_body_mesh: AddBodyMeshConfig = field(default_factory=AddBodyMeshConfig)
