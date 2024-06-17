from enum import Enum

from freemocap_blender_addon.models.animation.armatures.bones.body_skeleton_bone_constraints import DefaultBoneConstraints

_ARMATURE_BONE_CONSTRAINTS_TYPES = {
    "DEFAULT": DefaultBoneConstraints,
}
ArmatureBoneConstraintsTypes = Enum("ArmatureBoneConstraintsTypes", _ARMATURE_BONE_CONSTRAINTS_TYPES)
