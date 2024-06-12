import math as m
from typing import Dict

import bpy

from freemocap_blender_addon.models.animation.armatures import bone_name_map
from freemocap_blender_addon.models.animation.armatures.armature_bone_info import ArmatureBoneInfo
from freemocap_blender_addon.models.animation.armatures.armature_types import ArmatureType
from freemocap_blender_addon.models.animation.bones.ik_control_bones import ik_control_bones
from freemocap_blender_addon.models.animation.bones.ik_pole_bones import ik_pole_bones
from freemocap_blender_addon.models.animation.poses.pose_element import PoseElement
from freemocap_blender_addon.system.constants import UE_METAHUMAN_SIMPLE_ARMATURE, FREEMOCAP_ARMATURE


def add_rig_by_bone(
        bone_data: Dict[str, Dict[str, float]],
        armature: Dict[str, ArmatureBoneInfo],
        pose: Dict[str, PoseElement],
        add_ik_constraints: bool,
) -> bpy.types.Object:
    print("Adding rig to scene bone by bone...")
    if armature == ArmatureType.UE_METAHUMAN_SIMPLE:
        armature_name = UE_METAHUMAN_SIMPLE_ARMATURE
    elif armature == ArmatureType.FREEMOCAP:
        armature_name = FREEMOCAP_ARMATURE
    else:
        raise ValueError("Invalid armature name")

    # Get rig height as the sum of the major bones length in a standing position. Assume foot declination angle of 23º
    avg_ankle_projection_length = (m.sin(m.radians(23)) * bone_data["foot.R"]["median"]
                                   + m.sin(m.radians(23)) * bone_data["foot.L"]["median"]) / 2
    avg_shin_length = (bone_data["shin.R"]["median"] + bone_data["shin.L"]["median"]) / 2
    avg_thigh_length = (bone_data["thigh.R"]["median"] + bone_data["thigh.L"]["median"]) / 2

    # Add the armature
    bpy.ops.object.armature_add(
        enter_editmode=False,
        align="WORLD",
        location=(0, 0, 0),
    )

    # Rename the armature
    bpy.data.armatures[0].name = "root"
    # Get reference to armature
    rig = bpy.data.objects["Armature"]
    # Rename the rig object to pelvis
    rig.name = "root"
    # Get reference to the renamed armature
    rig = bpy.data.objects["root"]

    # Change to edit mode
    bpy.ops.object.mode_set(mode="EDIT")

    # Remove the default bone
    rig.data.edit_bones.remove(rig.data.edit_bones["Bone"])

    # Get the inverse bone_map_dict
    inv_bone_name_map = {
        value: key for key, value in bone_name_map[armature_name].items()
    }

    # Iterate over the armature dictionary
    for bone in armature:

        # Get the reference to the parent of the bone if its not root
        parent_name = armature[bone].parent_bone
        if parent_name != "root":
            parent_bone = rig.data.edit_bones[parent_name]

        # Add the new bone
        rig_bone = rig.data.edit_bones.new(bone)

        # Set the bone head position
        if bone in ("pelvis"):
            rig_bone.head = mathutils.Vector(
                [
                    0,
                    0,
                    avg_ankle_projection_length + avg_shin_length + avg_thigh_length,
                ]
            )
        else:
            # Set the bone position relative to its parent
            if armature[bone].parent_position == "head":
                rig_bone.head = parent_bone.head
            elif armature[bone].parent_position == "tail":
                rig_bone.head = parent_bone.tail

        # Get the bone vector
        if inv_bone_name_map[bone] not in bone_data:
            bone_vector = mathutils.Vector(
                [0, 0, armature[bone].default_length]
            )
        else:
            bone_vector = mathutils.Vector(
                [0, 0, bone_data[inv_bone_name_map[bone]]["median"]]
            )

        # Get the rotation matrix
        rotation_matrix = mathutils.Euler(
            mathutils.Vector(pose[bone].rotation),
            "XYZ",
        ).to_matrix()

        # Rotate the bone vector
        rig_bone.tail = rig_bone.head + rotation_matrix @ bone_vector

        # Assign the roll to the bone
        rig_bone.roll = pose[bone].roll

        # Parent the bone if its parent exists
        if parent_name != "root":
            rig_bone.parent = parent_bone
            rig_bone.use_connect = armature[bone].connected

    # Special armature conditions
    if armature_name == UE_METAHUMAN_SIMPLE_ARMATURE:
        # Change parents of thigh bones
        rig.data.edit_bones["thigh_r"].use_connect = False
        rig.data.edit_bones["thigh_l"].use_connect = False
        rig.data.edit_bones["thigh_r"].parent = rig.data.edit_bones["pelvis"]
        rig.data.edit_bones["thigh_l"].parent = rig.data.edit_bones["pelvis"]

    # Add the ik bones if specified
    if add_ik_constraints:
        for ik_control in ik_control_bones:
            ik_bone = rig.data.edit_bones.new(ik_control)
            ik_bone.head = rig.data.edit_bones[
                bone_name_map[armature_name][
                    ik_control_bones[ik_control].controlled_bone
                ]
            ].head
            ik_bone.tail = ik_bone.head + mathutils.Vector(
                ik_control_bones[ik_control].tail_relative_position
            )
        for ik_pole in ik_pole_bones:
            ik_bone = rig.data.edit_bones.new(ik_pole)
            ik_bone.head = ik_pole_bones[ik_pole].head_position
            ik_bone.tail = ik_pole_bones[ik_pole].tail_position

    return rig
