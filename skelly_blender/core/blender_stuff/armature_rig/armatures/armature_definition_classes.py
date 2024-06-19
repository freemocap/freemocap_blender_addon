import pprint
from dataclasses import dataclass
from typing import Dict

from skelly_blender.core.blender_stuff.armature_rig.bone_constraints.armature_bone_constraints_types import ArmatureBoneConstraintsTypes
from skelly_blender.core.blender_stuff.armature_rig.armatures.armature_bone_classes import ArmatureBoneDefinition
from skelly_blender.core.blender_stuff.armature_rig.rest_pose_definitions.pose_types import RestPoseTypes
from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedName
from skelly_blender.core.pure_python.generic_type_hints import RigidSegmentDefinitions
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ArmatureDefinition(TypeSafeDataclass):
    armature_name: str
    bone_definitions: Dict[BlenderizedName, ArmatureBoneDefinition]

    @classmethod
    def create(cls,
               armature_name: str,
               segment_definitions: RigidSegmentDefinitions,
               pose_definition: RestPoseTypes,
               bone_constraints: ArmatureBoneConstraintsTypes) -> 'ArmatureDefinition':
        bone_definitions = {}
        for segment_name, segment in segment_definitions.items():
            bone_definitions[blenderize_name(segment_name)] = ArmatureBoneDefinition(
                rest_pose=pose_definition.value[blenderize_name(segment_name)].value,
                constraints=bone_constraints.value[blenderize_name(segment_name)].value,
                length=segment.length,
            )

        return cls(
            armature_name=armature_name,
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

    armature_definition = ArmatureDefinition.create(
        armature_name="rig",
        segment_definitions=segment_definitions_outer,
        pose_definition=RestPoseTypes.DEFAULT_TPOSE,
        bone_constraints=ArmatureBoneConstraintsTypes.DEFAULT_SKELETON
    )
    print(armature_definition)
