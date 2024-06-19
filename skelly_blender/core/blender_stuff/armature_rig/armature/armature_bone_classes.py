import math as m
from dataclasses import dataclass
from typing import Tuple, Optional

import mathutils

from skelly_blender.core.blender_stuff.armature_rig.bone_constraints.armature_bone_constraints_types import \
    ArmatureBoneConstraintsTypes

ROOT_BONE_NAME = "ROOT"


@dataclass
class BoneRestPoseDefinition:
    parent_bone_name: Optional[str]
    world_rotation_degrees: Tuple[float, float, float] = (0, 0, 0)  # rotation defined relative to parent bone
    offset: Tuple[float, float, float] = (0, 0, 0)
    roll: float = 0
    is_connected: bool = True

    def __str__(self):
        rotation_str = ", ".join([f"{r:.3f}" for r in self.world_rotation_degrees])
        return f"PoseElement(local_rotation_degrees={rotation_str}) [degrees]: parent_bone_name: {self.parent_bone_name}, is_connected={self.is_connected}"

    @property
    def rotation_as_radians(self) -> mathutils.Vector:
        return mathutils.Vector((m.radians(self.world_rotation_degrees[0]),
                                 m.radians(self.world_rotation_degrees[1]),
                                 m.radians(self.world_rotation_degrees[2])))

    @property
    def rotation_matrix(self) -> mathutils.Matrix:
        return mathutils.Euler(
            mathutils.Vector(self.rotation_as_radians),
            "XYZ",
        ).to_matrix()


@dataclass
class ArmatureBoneDefinition:
    length: float
    rest_pose: BoneRestPoseDefinition
    constraints: ArmatureBoneConstraintsTypes

    @property
    def is_root(self):
        return self.rest_pose.parent_bone_name == ROOT_BONE_NAME

    @property
    def parent(self):
        return self.rest_pose.parent_bone_name

    def __str__(self):
        return f"ArmatureBoneDefinition: {self.rest_pose} with length {self.length}"
