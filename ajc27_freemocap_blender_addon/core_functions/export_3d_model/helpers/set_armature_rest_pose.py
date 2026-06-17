import math as m

import bpy
from mathutils import Euler, Vector

from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.rest_pose_types import (
    rest_pose_type_rotations,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import (
    get_bone_info,
)


def _get_marker(parent_empty: bpy.types.Object, substring: str) -> bpy.types.Object:
    """Helper to find a marker by name substring."""
    return next(
        (marker for marker in parent_empty.children_recursive if substring in marker.name),
        None
    )


def _add_damped_track(pose_bone, target, name, track_axis, influence):
    """Helper to add a DAMPED_TRACK constraint."""
    constraint = pose_bone.constraints.new('DAMPED_TRACK')
    constraint.name = name
    constraint.target = target
    constraint.track_axis = track_axis
    constraint.influence = influence
    return constraint


def _apply_base_rotations(
    armature: bpy.types.Armature, bone_info: dict, rest_pose_rotations: dict
):
    for bone in armature.data.edit_bones:
        if bone.name in rest_pose_rotations:
            # If the bone is part of the palm, move its head to its parent
            # as it is not connected and didn't move with its parent rotation
            if 'palm' in bone.name or 'thumb.carpal' in bone.name:
                bone.head = bone.parent.head

            bone_vector = Vector([0, 0, bone_info[bone.name]['length']])

            # Get the rotation matrix
            rotation_matrix = Euler(
                Vector(rest_pose_rotations[bone.name]['rotation']),
                'XYZ',
            ).to_matrix()

            # Rotate the bone vector
            bone.tail = bone.head + rotation_matrix @ bone_vector

            # Assign the roll to the bone
            bone.roll = rest_pose_rotations[bone.name]['roll']


def _apply_metahuman_edit_mode(
    armature: bpy.types.Armature, bone_info: dict, rest_pose_rotations: dict
):
    for bone in armature.data.edit_bones:
        if 'thigh' in bone.name:
            bone.use_connect = False
            bone.parent = armature.data.edit_bones['pelvis']

        if 'thumb.01' in bone.name:
            thumb_side = 'left' if '.L' in bone.name else 'right'
            bone.use_connect = False
            # Set the new parent to the hand using uppercase first letter
            bone.parent = armature.data.edit_bones[f'hand.{thumb_side[0].upper()}']

            # Remove the thumb.carpal bone
            thumb_carpal_name = f'thumb.carpal.{thumb_side[0].upper()}'
            if thumb_carpal_name in armature.data.edit_bones:
                armature.data.edit_bones.remove(
                    armature.data.edit_bones[thumb_carpal_name]
                )

        # Disconnect the shoulder and neck bones from parent
        # so spine.001 can have custom rotation
        if 'shoulder' in bone.name or 'neck' in bone.name:
            bone.use_connect = False

    # Change the length of Spine.001 (spine_04) to compensate for new parent
    spine_rotation = rest_pose_rotations['spine']['rotation'][0]
    spine_len = bone_info['spine']['length']
    spine_001_len = bone_info['spine.001']['length']
    
    # Law of cosines
    spine_001_new_length = m.sqrt(
        spine_len**2
        + (spine_len + spine_001_len)**2
        - 2 * spine_len * (spine_len + spine_001_len) * m.cos(spine_rotation)
    )

    armature.data.edit_bones['spine.001'].length = spine_001_new_length


def _apply_metahuman_pose_mode(
    armature: bpy.types.Armature, data_parent_empty: bpy.types.Object
):
    for pose_bone in armature.pose.bones:
        if 'thumb.01' in pose_bone.name:
            thumb_side = 'left' if '.L' in pose_bone.name else 'right'
            thumb_cmc = _get_marker(
                data_parent_empty, f"{thumb_side}_hand_thumb_cmc"
            )
            if thumb_cmc:
                location_constraint = pose_bone.constraints.new('COPY_LOCATION')
                location_constraint.target = thumb_cmc
                pose_bone.constraints.move(1, 0)

    # Change the targets of the hand constraints
    # TODO: Delete this if default target markers change to these in the future
    for side in ['left', 'right']:
        hand_bone = armature.pose.bones[f'hand.{side[0].upper()}']

        hand_middle_finger_mcp = _get_marker(data_parent_empty, f"{side}_hand_middle_finger_mcp")
        hand_index_finger_mcp = _get_marker(data_parent_empty, f"{side}_hand_index_finger_mcp")

        if hand_middle_finger_mcp and 'Damped Track' in hand_bone.constraints:
            hand_bone.constraints['Damped Track'].target = hand_middle_finger_mcp
        if hand_index_finger_mcp and 'Locked Track' in hand_bone.constraints:
            hand_bone.constraints['Locked Track'].target = hand_index_finger_mcp

    trunk_center_marker = _get_marker(data_parent_empty, 'trunk_center')
    _add_damped_track(
        armature.pose.bones["spine"],
        trunk_center_marker,
        "Metahuman_Spine_01_Correction",
        'TRACK_NEGATIVE_Z',
        0.055,
    )

    neck_center_marker = _get_marker(data_parent_empty, 'neck_center')
    _add_damped_track(
        armature.pose.bones["spine.001"],
        neck_center_marker,
        "Metahuman_Spine_04_Correction",
        'TRACK_Z',
        0.035,
    )

    # Create a new copy_location constraint to the neck bone to set its location to the neck_center marker
    neck_location_constraint = armature.pose.bones["neck"].constraints.new('COPY_LOCATION')
    neck_location_constraint.name = "Metahuman_Neck_Location_Correction"
    neck_location_constraint.target = neck_center_marker

    # Move the new constraint to the top of the stack
    neck_constraints = armature.pose.bones["neck"].constraints
    neck_constraints.move(len(neck_constraints) - 1, 0)

    head_center_marker = _get_marker(data_parent_empty, 'head_center')
    _add_damped_track(
        armature.pose.bones["neck"],
        head_center_marker,
        "Metahuman_Neck_Correction",
        'TRACK_Z',
        0.11,
    )

    nose_marker = _get_marker(data_parent_empty, 'nose')
    _add_damped_track(
        armature.pose.bones["face"],
        nose_marker,
        "Metahuman_Head_Correction",
        'TRACK_Z',
        0.1,
    )


def _apply_daz_g8_1_edit_mode(armature: bpy.types.Armature, bone_info: dict):
    # Parent the thigh bones to the pelvis
    for bone in armature.data.edit_bones:
        if 'thigh' in bone.name:
            bone.use_connect = False
            bone.parent = armature.data.edit_bones['pelvis']

        if 'thumb.01' in bone.name:
            thumb_side = 'left' if '.L' in bone.name else 'right'
            bone.use_connect = False
            # Set the new parent to the hand using uppercase first letter
            bone.parent = armature.data.edit_bones[f'hand.{thumb_side[0].upper()}']

            # Remove the thumb.carpal bone
            thumb_carpal_name = f'thumb.carpal.{thumb_side[0].upper()}'
            if thumb_carpal_name in armature.data.edit_bones:
                armature.data.edit_bones.remove(
                    armature.data.edit_bones[thumb_carpal_name]
                )

    # Change length of Spine.001 (chestLower) to compensate for new parent position
    # 18 results from the 0.2 influence of the trunk_center marker above
    spine_rotation = m.radians(18)
    spine_length = bone_info['spine']['length']
    spine_001_length = bone_info['spine.001']['length']
    
    spine_001_new_length = m.sqrt(
        spine_length**2
        + (spine_length + spine_001_length)**2
        - 2 * spine_length * (spine_length + spine_001_length) * m.cos(spine_rotation)
    )

    armature.data.edit_bones['spine.001'].length = spine_001_new_length

    print("New spine.001 length:", armature.data.edit_bones['spine.001'].length)

    # Create the ForearmTwist bones and parent them to the forearm bones
    for side in ['left', 'right']:
        forearm_name = f'forearm.{side[0].upper()}'
        if forearm_name not in armature.data.edit_bones:
            continue

        bone = armature.data.edit_bones[forearm_name]

        # Duplicate bone
        forearm_twist_bone = armature.data.edit_bones.new(
            f'forearm_twist.{side[0].upper()}'
        )
        forearm_twist_bone.head = bone.head.copy()
        forearm_twist_bone.tail = bone.tail.copy()
        forearm_twist_bone.roll = bone.roll
        forearm_twist_bone.use_connect = False

        # Parent duplicate to source
        forearm_twist_bone.parent = bone


def _apply_daz_g8_1_pose_mode(
    armature: bpy.types.Armature, data_parent_empty: bpy.types.Object
):
    for pose_bone in armature.pose.bones:
        if 'thumb.01' in pose_bone.name:
            thumb_side = 'left' if '.L' in pose_bone.name else 'right'
            thumb_cmc = _get_marker(
                data_parent_empty, f"{thumb_side}_hand_thumb_cmc"
            )
            if thumb_cmc:
                bone_location_constraint = pose_bone.constraints.new('COPY_LOCATION')
                bone_location_constraint.target = thumb_cmc
                pose_bone.constraints.move(1, 0)

    nose_marker = _get_marker(data_parent_empty, 'nose')
    _add_damped_track(
        armature.pose.bones["face"],
        nose_marker,
        "DazG8.1_Face_Correction",
        'TRACK_Z',
        0.6,
    )

    trunk_center_marker = _get_marker(data_parent_empty, 'trunk_center')

    pelvis_constraint = armature.pose.bones["pelvis"].constraints.new('LOCKED_TRACK')
    pelvis_constraint.name = "DazG8.1_Pelvis_Correction"
    pelvis_constraint.target = trunk_center_marker
    pelvis_constraint.track_axis = 'TRACK_Y'
    pelvis_constraint.lock_axis = 'LOCK_X'
    pelvis_constraint.influence = 0.87

    _add_damped_track(
        armature.pose.bones["spine"],
        trunk_center_marker,
        "DazG8.1_Spine_Correction",
        'TRACK_NEGATIVE_Z',
        0.2,
    )

    for side in ['left', 'right']:
        twist_bone_name = f'forearm_twist.{side[0].upper()}'
        hand_bone_name = f'hand.{side[0].upper()}'
        forearm_bone_name = f'forearm.{side[0].upper()}'

        if (
            twist_bone_name in armature.pose.bones
            and hand_bone_name in armature.pose.bones
        ):
            forearm_twist_bone = armature.pose.bones[twist_bone_name]
            hand_bone = armature.pose.bones[hand_bone_name]

            copy_rotation_constraint = forearm_twist_bone.constraints.new('COPY_ROTATION')
            copy_rotation_constraint.target = armature
            copy_rotation_constraint.subtarget = hand_bone.name
            copy_rotation_constraint.influence = 0.5
            copy_rotation_constraint.use_x = False
            copy_rotation_constraint.use_z = False
            copy_rotation_constraint.target_space = 'LOCAL'
            copy_rotation_constraint.owner_space = 'LOCAL'

        if forearm_bone_name in armature.pose.bones:
            forearm_bone = armature.pose.bones[forearm_bone_name]
            thumb_cmc = _get_marker(data_parent_empty, f"{side}_hand_thumb_cmc")

            bend_bone_constraint = forearm_bone.constraints.new('LOCKED_TRACK')
            bend_bone_constraint.name = 'DazG8.1_Forearm_Bend_Correction'
            bend_bone_constraint.target = thumb_cmc
            bend_bone_constraint.track_axis = 'TRACK_Z'
            bend_bone_constraint.lock_axis = 'LOCK_Y'
            bend_bone_constraint.influence = 0.35


def set_armature_rest_pose(
    data_parent_empty: bpy.types.Object,
    armature: bpy.types.Armature,
    rest_pose_type: str,
):
    print("Setting armature rest pose...")
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the armature
    armature.select_set(True)

    # Get the bone info (positions and lengths)
    bone_info = get_bone_info(armature)

    rest_pose_rotations = rest_pose_type_rotations[rest_pose_type]

    # Enter Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Apply base rest pose rotations
    _apply_base_rotations(armature, bone_info, rest_pose_rotations)

    if rest_pose_type == 'metahuman':
        _apply_metahuman_edit_mode(armature, bone_info, rest_pose_rotations)
    elif rest_pose_type == 'daz_g8.1':
        _apply_daz_g8_1_edit_mode(armature, bone_info)

    # Enter Pose Mode
    bpy.ops.object.mode_set(mode='POSE')

    if rest_pose_type == 'metahuman':
        _apply_metahuman_pose_mode(armature, data_parent_empty)
    elif rest_pose_type == 'daz_g8.1':
        _apply_daz_g8_1_pose_mode(armature, data_parent_empty)

    # Go back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
