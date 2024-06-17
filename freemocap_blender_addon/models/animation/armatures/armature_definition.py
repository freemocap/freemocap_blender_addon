from collections import defaultdict, deque
from dataclasses import dataclass
import pprint
from typing import Dict, Tuple, List

from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import BoneRestPoseDefinition, \
    ROOT_BONE_NAME
from freemocap_blender_addon.models.animation.armatures.rest_pose.pose_types import PoseTypes
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name, BlenderizedName
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ArmatureBoneDefinition:
    rest_pose: BoneRestPoseDefinition
    length: float

    @property
    def is_root(self):
        return self.rest_pose.parent_bone_name == ROOT_BONE_NAME

    @property
    def parent(self):
        return self.rest_pose.parent_bone_name

    def __str__(self):
        return f"ArmatureBoneDefinition: {self.rest_pose} with length {self.length}"




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

    def __str__(self):
        return f"ArmatureDefinition: {self.armature_name} with bones: {pprint.pformat(self.bone_definitions, indent=4)}"



if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_test_recording
    from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
        calculate_rigid_body_trajectories
    from freemocap_blender_addon.models.skeleton_model import SkeletonTypes

    recording_data = load_freemocap_test_recording()
    keypoint_trajectories_outer, segment_definitions_outer = calculate_rigid_body_trajectories(
        keypoint_trajectories=recording_data.body.map_to_keypoints(),
        skeleton_definition=SkeletonTypes.BODY_ONLY)

    armature_definition=ArmatureDefinition.create(
        rig_name="rig",
        segment_definitions=segment_definitions_outer,
        pose_definition=PoseTypes.DEFAULT_TPOSE,
    )
    print(armature_definition)
