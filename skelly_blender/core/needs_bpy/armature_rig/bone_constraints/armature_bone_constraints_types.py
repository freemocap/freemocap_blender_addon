from enum import Enum

from skelly_blender.core.needs_bpy.armature_rig.bone_constraints.body_skeleton_bone_constraint_definitions import \
    DefaultBoneConstraints

_ARMATURE_BONE_CONSTRAINTS_TYPES = {
    "DEFAULT_SKELETON": DefaultBoneConstraints,
}
ArmatureBoneConstraintsTypes = Enum("ArmatureBoneConstraintsTypes", _ARMATURE_BONE_CONSTRAINTS_TYPES)
