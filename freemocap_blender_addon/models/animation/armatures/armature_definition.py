from dataclasses import dataclass
from typing import Dict

from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import ROOT_BONE_NAME, \
    BonePoseDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose.pose_types import PoseTypes
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name, BlenderizedName
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ArmatureBoneDefinition:
    rest_pose: BonePoseDefinition
    length: float

    @property
    def is_root(self):
        return self.rest_pose.parent_bone_name == ROOT_BONE_NAME

    @property
    def parent(self):
        return self.rest_pose.parent_bone_name

@dataclass
class ArmatureDefinition(TypeSafeDataclass):
    armature_name: str
    bone_definitions: Dict[BlenderizedName, ArmatureBoneDefinition]

    @classmethod
    def create(cls,
               rig_name: str,
               segment_definitions: RigidSegmentDefinitions,
               pose_definition: PoseTypes):
        bone_definitions = {}
        for segment_name, segment in segment_definitions.items():
            bone_definitions[blenderize_name(segment_name)] = ArmatureBoneDefinition(
                rest_pose=pose_definition.value[blenderize_name(segment_name)].value,
                length=segment.length,
            )

        return cls(
            armature_name=rig_name,
            bone_definitions=bone_definitions,
        )
