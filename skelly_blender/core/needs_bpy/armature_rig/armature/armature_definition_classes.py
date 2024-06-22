import pprint
from dataclasses import dataclass
from typing import Dict

from skelly_blender.core.needs_bpy.armature_rig.armature.armature_bone_classes import ArmatureBoneDefinition
from skelly_blender.core.needs_bpy.armature_rig.bone_constraints.armature_bone_constraints_types import \
    ArmatureBoneConstraintsTypes
from skelly_blender.core.needs_bpy.armature_rig.rest_pose_definitions.pose_types import RestPoseTypes
from skelly_blender.core.needs_bpy.blender_type_hints import BlenderizedName, BlenderizedSegmentDefinitions
from skelly_blender.core.needs_bpy.blenderizers.blenderized_skeleton_data import deparentify_name
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ArmatureDefinition(TypeSafeDataclass):
    armature_name: str
    bone_definitions: Dict[BlenderizedName, ArmatureBoneDefinition]

    @classmethod
    def create(cls,
               armature_name: str,
               segment_definitions: BlenderizedSegmentDefinitions,
               pose_definition: RestPoseTypes,
               bone_constraints: ArmatureBoneConstraintsTypes) -> 'ArmatureDefinition':
        bone_definitions = {}
        for segment_name, segment in segment_definitions.items():
            deparentified_name = deparentify_name(segment_name)
            bone_definitions[deparentified_name] = ArmatureBoneDefinition(
                rest_pose=pose_definition.value[deparentified_name].value,
                constraints=bone_constraints.value[deparentified_name].value,
                length=segment.length,
            )

        return cls(
            armature_name=armature_name,
            bone_definitions=bone_definitions,
        )

    def __str__(self):
        return f"ArmatureDefinition: {self.armature_name} with bones: {list(self.bone_definitions.keys())}"

