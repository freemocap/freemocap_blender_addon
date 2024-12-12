import math as m
from typing import Dict

import bpy

from ajc27_freemocap_blender_addon.core_functions.create_rig.rig_utilities import get_appended_number
from ajc27_freemocap_blender_addon.data_models.armatures.armature_bone_info import ArmatureBoneInfo
from ajc27_freemocap_blender_addon.data_models.armatures.bone_name_map import bone_name_map
from ajc27_freemocap_blender_addon.data_models.bones.bone_constraints import ConstraintType, \
    LimitRotationConstraint, CopyLocationConstraint, LockedTrackConstraint, DampedTrackConstraint, IKConstraint, \
    Constraint
from ajc27_freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType
from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement
from ajc27_freemocap_blender_addon.system.constants import UE_METAHUMAN_SIMPLE_ARMATURE, FREEMOCAP_ARMATURE, FREEMOCAP_TPOSE, \
    FREEMOCAP_APOSE, UE_METAHUMAN_DEFAULT, UE_METAHUMAN_TPOSE


def apply_bone_constraints(
    rig: bpy.types.Object,
    add_fingers_constraints: bool,
    parent_object: bpy.types.Object,
        bone_constraint_definitions=Dict[str, Constraint],
    armature_definition: Dict[str, ArmatureBoneInfo] = ArmatureType.FREEMOCAP,
    pose_definition: Dict[str, PoseElement] = PoseType.FREEMOCAP_TPOSE,

    use_limit_rotation: bool = False,
) -> None:
    if armature_definition == ArmatureType.UE_METAHUMAN_SIMPLE:
        armature_name = UE_METAHUMAN_SIMPLE_ARMATURE
    elif armature_definition == ArmatureType.FREEMOCAP:
        armature_name = FREEMOCAP_ARMATURE
    else:
        raise ValueError("Invalid armature name")

    if pose_definition == PoseType.FREEMOCAP_TPOSE:
        pose_name = FREEMOCAP_TPOSE
    elif pose_definition == PoseType.FREEMOCAP_APOSE:
        pose_name = FREEMOCAP_APOSE
    elif pose_definition == PoseType.UE_METAHUMAN_DEFAULT:
        pose_name = UE_METAHUMAN_DEFAULT
    elif pose_definition == PoseType.UE_METAHUMAN_TPOSE:
        pose_name = UE_METAHUMAN_TPOSE
    else:
        raise ValueError("Invalid pose name")

    print("Adding bone constraints...")
    # TODO: getting key error in this function with Failed to add rig: 'bpy_prop_collection[key]: key "pelvis.R" not found'
    # Change to pose mode
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    #
    # # Define the hand bones damped track target as the hand middle empty if they were already added
    # try:
    #     right_hand_middle_name = bpy.data.objects['right_hand_middle'].name
    #     # Right Hand Middle Empty exists. Use hand middle as target
    #     hand_damped_track_target = 'hand_middle'
    # except:
    #     # Hand middle empties do not exist. Use hand_index as target
    #     hand_damped_track_target = 'index'

    # Create each constraint
    for (
        bone_name,
        constraint_definitions,
    ) in bone_constraint_definitions.items():
        # If pose bone does not exist, skip it
        if bone_name not in rig.pose.bones:
            continue

        if not isinstance(constraint_definitions, list):
            raise Exception(f"Constraint definitions for {bone_name} must be a list")

        # If it is a finger bone amd add_fingers_constraints is False continue with the next bone
        if (
            not add_fingers_constraints
            and len(
                [
                    finger_part
                    for finger_part in [
                        "palm",
                        "thumb",
                        "index",
                        "middle",
                        "ring",
                        "pinky",
                    ]
                    if finger_part
                    in constraint_definitions
                ]
            )
            > 0
        ):
            continue

        for constraint in constraint_definitions:
            # if "target" in constraint.keys():
            #     base_target_name = constraint["target"]
            #     actual_target_name = get_actual_empty_target_name(empty_names = empty_names,
            #                                                       base_target_name = base_target_name)
            #     constraint["target"] = actual_target_name
            appended_number_string = get_appended_number(parent_object.name)
            if appended_number_string is not None:
                if hasattr(constraint, "target"):
                    constraint.target = constraint.target + appended_number_string
            # Add new constraint determined by type
            if not use_limit_rotation and constraint.type == ConstraintType.LIMIT_ROTATION:
                continue
            else:
                try:
                    bone_constraint = rig.pose.bones[bone_name_map[armature_name][bone_name]].constraints.new(
                        constraint.type.value
                    )
                except:
                    print(f"Failed to add rig: {bone_name} constraint {constraint.type}")
                    continue

                # Define aditional parameters based on the type of constraint
            if isinstance(constraint, LimitRotationConstraint):
                bone_constraint.use_limit_x = constraint.use_limit_x
                bone_constraint.min_x = m.radians(constraint.min_x)
                bone_constraint.max_x = m.radians(constraint.max_x)
                bone_constraint.use_limit_y = constraint.use_limit_y
                bone_constraint.min_y = m.radians(constraint.min_y)
                bone_constraint.max_y = m.radians(constraint.max_y)
                bone_constraint.use_limit_z = constraint.use_limit_z
                bone_constraint.min_z = m.radians(constraint.min_z)
                bone_constraint.max_z = m.radians(constraint.max_z)
                bone_constraint.owner_space = constraint.owner_space.value
            elif isinstance(constraint, CopyLocationConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
            elif isinstance(constraint, LockedTrackConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
                bone_constraint.track_axis = constraint.track_axis[pose_name].value
                bone_constraint.lock_axis = constraint.lock_axis[pose_name].value
                bone_constraint.influence = constraint.influence
            elif isinstance(constraint, DampedTrackConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
                bone_constraint.track_axis = constraint.track_axis.value
            elif isinstance(constraint, IKConstraint):
                bone_constraint.target = bpy.data.objects[constraint.target]
                bone_constraint.pole_target = bpy.data.objects[
                    constraint.pole_target
                ]
                bone_constraint.chain_count = constraint.chain_count
                bone_constraint.pole_angle = constraint.pole_angle
