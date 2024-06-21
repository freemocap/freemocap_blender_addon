import pprint
from dataclasses import dataclass
from typing import Dict

from skelly_blender.core.blender_stuff.armature_rig.armature.armature_bone_classes import ArmatureBoneDefinition
from skelly_blender.core.blender_stuff.armature_rig.bone_constraints.armature_bone_constraints_types import \
    ArmatureBoneConstraintsTypes
from skelly_blender.core.blender_stuff.armature_rig.rest_pose_definitions.pose_types import RestPoseTypes
from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedName, BlenderizedSegmentDefinitions
from skelly_blender.core.blender_stuff.blenderizers.blenderize_name import blenderize_name
from skelly_blender.core.utility_classes import TypeSafeDataclass


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

