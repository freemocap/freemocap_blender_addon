import bpy
import mathutils

from freemocap_blender_addon.models.animation.bones.ik_control_bones import ik_control_bones
from freemocap_blender_addon.models.animation.bones.ik_pole_bones import ik_pole_bones


def add_ik_constraints_to_rig(armature=bpy.types.Object) -> bpy.types.Object:
    for ik_control in ik_control_bones:
        ik_bone = armature.data.edit_bones.new(ik_control)
        ik_bone.head = armature.data.edit_bones[ik_control.controlled_bone].head
        ik_bone.tail = ik_bone.head + mathutils.Vector(
            ik_control.tail_relative_position
        )
    for ik_pole in ik_pole_bones:
        ik_bone = armature.data.edit_bones.new(ik_pole)
        ik_bone.head = ik_pole_bones[ik_pole].head_position
        ik_bone.tail = ik_pole_bones[ik_pole].tail_position

    return armature
