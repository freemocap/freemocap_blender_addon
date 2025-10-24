import bpy
from mathutils import Vector, Euler
import math as m

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import get_bone_info
from ajc27_freemocap_blender_addon.core_functions.export_3d_model.helpers.rest_pose_types import rest_pose_type_rotations

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

    # Get the bone info (postions and lengths)
    bone_info = get_bone_info(armature)

    rest_pose_rotations = rest_pose_type_rotations[rest_pose_type]

    # Enter Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Set the rest pose rotations
    for bone in armature.data.edit_bones:
        if bone.name in rest_pose_rotations:

            # If the bone is part of the palm, move its head to its parent
            # as it is not connected and didn't move with its parent rotation
            if 'palm' in bone.name or 'thumb.carpal' in bone.name:
                bone.head = bone.parent.head

            # TODO: Check again the metahuman metacarpal offset values
            # TODO: Generalize this for other rest pose types if needed
            # If the armature is a metahuman, move the metacarpals using the offset info
            # if rest_pose_type == 'metahuman':
            #     if bone.name in ['palm.01.L', 'palm.02.L', 'palm.03.L', 'palm.04.L'] and 'position_offset' in rest_pose_rotations[bone.name].keys():
            #         print("Bone head position:", bone.head)
            #         print("Bone tail position:", bone_info[bone.name]['tail_position'])
            #         print("Bone length:", bone_info[bone.name]['length'])
            #         # Get the offset distance from the hand bone head
            #         offset_distance = rest_pose_rotations[bone.name]['position_offset']['wrist_newbonehead_to_wrist_mcp_ratio'] * bone_info[bone.name]['length']
            #         # Create the offset vector
            #         offset_vector = Vector([0, 0, offset_distance])
            #         # Get the rotation matrix
            #         rotation_matrix = Euler(
            #             Vector(rest_pose_rotations[bone.name]['position_offset']['rotation']),
            #                 'XYZ',
            #             ).to_matrix()
            #         # Rotate the offset vector
            #         bone.head = (
            #             bone.parent.head
            #             + rotation_matrix @ offset_vector
            #         )
            #         # Update the bone length
            #         bone_info[bone.name]['length'] = rest_pose_rotations[bone.name]['position_offset']['newbonehead_mcp_to_wrist_mcp_ratio'] * bone_info[bone.name]['length']
            #         print("Bone head position:", bone.head)
            #         print("Bone tail position:", bone_info[bone.name]['tail_position'])
            #         print("Bone length:", bone_info[bone.name]['length'])

            bone_vector = Vector(
                [0, 0, bone_info[bone.name]['length']]
            )

            # Get the rotation matrix
            rotation_matrix = Euler(
                Vector(rest_pose_rotations[bone.name]['rotation']),
                'XYZ',
            ).to_matrix()

            # Rotate the bone vector
            bone.tail = (
                bone.head
                + rotation_matrix @ bone_vector
            )

            # Assign the roll to the bone
            bone.roll = rest_pose_rotations[bone.name]['roll']

    # In case the rest pose type is metahuman, parent the thigh bones to the pelvis
    # and parent the thumb.01 bones to the hand
    if rest_pose_type == 'metahuman':
        for bone in armature.data.edit_bones:
            if 'thigh' in bone.name:
                bone.use_connect = False
                bone.parent = armature.data.edit_bones['pelvis']

            if 'thumb.01' in bone.name:
                thumb_side = 'left' if '.L' in bone.name else 'right'

                bone.use_connect = False
                # Set the new parent to the hand using the uppercase first letter of side
                bone.parent = armature.data.edit_bones[f'hand.{thumb_side[0].upper()}']

                # Get the thumb cmc marker
                thumb_cmc = [
                    marker for marker in data_parent_empty.children_recursive
                    if thumb_side + '_hand_thumb_cmc' in marker.name
                ][0]

                bone_location_constraint = armature.pose.bones[bone.name].constraints.new('COPY_LOCATION')
                bone_location_constraint.target = thumb_cmc
                armature.pose.bones[bone.name].constraints.move(1, 0)

                # Remove the thumb.carpal bone
                if 'thumb.carpal.' + thumb_side[0].upper() in armature.data.edit_bones:
                    armature.data.edit_bones.remove(armature.data.edit_bones['thumb.carpal.' + thumb_side[0].upper()])

        # Change the targets of the hand constraints
        # TODO: Delete this code if the default target markers change to these ones in the future
        for side in ['left', 'right']:
            hand_bone = armature.pose.bones['hand' + '.' + side[0].upper()]

            # Get the hand_middle_finger_mcp
            hand_middle_finger_mcp = [
                marker for marker in data_parent_empty.children_recursive
                if side + '_hand_middle_finger_mcp' in marker.name
            ][0]

            # Get the hand_index_finger_mcp
            hand_index_finger_mcp = [
                marker for marker in data_parent_empty.children_recursive
                if side + '_hand_index_finger_mcp' in marker.name
            ][0]

            hand_bone.constraints['Damped Track'].target = hand_middle_finger_mcp
            hand_bone.constraints['Locked Track'].target = hand_index_finger_mcp

    if rest_pose_type == 'daz_g8.1':
        # Parent the thigh bones to the pelvis
        for bone in armature.data.edit_bones:
            if 'thigh' in bone.name:
                bone.use_connect = False
                bone.parent = armature.data.edit_bones['pelvis']

            if 'thumb.01' in bone.name:
                thumb_side = 'left' if '.L' in bone.name else 'right'

                bone.use_connect = False
                # Set the new parent to the hand using the uppercase first letter of side
                bone.parent = armature.data.edit_bones[f'hand.{thumb_side[0].upper()}']

                # Get the thumb cmc marker
                thumb_cmc = [
                    marker for marker in data_parent_empty.children_recursive
                    if thumb_side + '_hand_thumb_cmc' in marker.name
                ][0]

                bone_location_constraint = armature.pose.bones[bone.name].constraints.new('COPY_LOCATION')
                bone_location_constraint.target = thumb_cmc
                armature.pose.bones[bone.name].constraints.move(1, 0)

                # Remove the thumb.carpal bone
                if 'thumb.carpal.' + thumb_side[0].upper() in armature.data.edit_bones:
                    armature.data.edit_bones.remove(armature.data.edit_bones['thumb.carpal.' + thumb_side[0].upper()])


        # Create a new damped_tracked constraint for the face and set it to the z-axis with 0.6 influence
        new_constraint = armature.pose.bones["face"].constraints.new('DAMPED_TRACK')
        new_constraint.name = "DazG8.1_Face_Correction"

        # Get the nose marker
        nose_marker = [
            marker for marker in data_parent_empty.children_recursive
            if 'nose' in marker.name
        ][0]
        new_constraint.target = nose_marker
        new_constraint.track_axis = 'TRACK_Z'
        new_constraint.influence = 0.6

        # Create a new locked_tracked constraint for the pelvis and set it to the y-axis with 0.87 influence
        new_constraint = armature.pose.bones["pelvis"].constraints.new('LOCKED_TRACK')
        new_constraint.name = "DazG8.1_Pelvis_Correction"

        # Get the trunk_center marker
        trunk_center_marker = [
            marker for marker in data_parent_empty.children_recursive
            if 'trunk_center' in marker.name
        ][0]
        new_constraint.target = trunk_center_marker
        new_constraint.track_axis = 'TRACK_Y'
        new_constraint.lock_axis = 'LOCK_X'
        new_constraint.influence = 0.87

        # Create a new damped_tracked constraint for the spine (abdomenLower) and set it to the -z-axis with 0.2 influence
        new_constraint = armature.pose.bones["spine"].constraints.new('DAMPED_TRACK')
        new_constraint.name = "DazG8.1_Spine_Correction"
        
        # Reuse the trunk_center marker
        new_constraint.target = trunk_center_marker
        new_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        new_constraint.influence = 0.2

        # Change the length of Spine.001 (chestLower) to compensate for the new parent position
        spine_rotation = m.radians(18) # 18 results from the 0.2 influence of the trunk_center marker above
        spine_length = bone_info['spine']['length']
        spine_001_length = bone_info['spine.001']['length']
        spine_001_new_length = m.sqrt(spine_length**2 + (spine_length+spine_001_length)**2 - 2*spine_length*(spine_length+spine_001_length)*m.cos(spine_rotation))

        armature.data.edit_bones['spine.001'].length = spine_001_new_length

        print("New spine.001 length:", armature.data.edit_bones['spine.001'].length)

        # Create the ForearmTwist bones and parent them to the forearm bones
        for side in ['left', 'right']:
            if not 'forearm.' + side[0].upper() in armature.data.edit_bones:
                continue

            bone = armature.data.edit_bones['forearm.' + side[0].upper()]

            # Duplicate bone
            forearm_twist_bone = armature.data.edit_bones.new('forearm_twist' + '.' + side[0].upper())
            
            forearm_twist_bone.head = bone.head.copy()
            forearm_twist_bone.tail = bone.tail.copy()
            forearm_twist_bone.roll = bone.roll
            forearm_twist_bone.use_connect = False

            # Parent duplicate to source
            forearm_twist_bone.parent = bone

        # Add a copy rotation constraint to the forearm_twist bones to copy the hand bone rotation
        # Also add a locked tracked constraint to the forearm_bend bones to the thumb cmc marker
        # Enter Pose Mode
        bpy.ops.object.mode_set(mode='POSE')

        for side in ['left', 'right']:
            forearm_twist_bone = armature.pose.bones['forearm_twist' + '.' + side[0].upper()]

            hand_bone = armature.pose.bones['hand' + '.' + side[0].upper()]

            copy_rotation_constraint = forearm_twist_bone.constraints.new('COPY_ROTATION')
            copy_rotation_constraint.target = armature
            copy_rotation_constraint.subtarget = hand_bone.name
            copy_rotation_constraint.influence = 0.5
            copy_rotation_constraint.use_x = False
            copy_rotation_constraint.use_z = False
            copy_rotation_constraint.target_space = 'LOCAL'
            copy_rotation_constraint.owner_space = 'LOCAL'
            
            forearm_bone = armature.pose.bones['forearm' + '.' + side[0].upper()]
            # Get the thumb cmc marker
            thumb_cmc = [
                marker for marker in data_parent_empty.children_recursive
                if side + '_hand_thumb_cmc' in marker.name
            ][0]

            # Add a locked track constraint to the forearm bone to point to the thumb cmc marker
            bend_bone_constraint = forearm_bone.constraints.new('LOCKED_TRACK')
            bend_bone_constraint.name = 'DazG8.1_Forearm_Bend_Correction'
            bend_bone_constraint.target = thumb_cmc
            bend_bone_constraint.track_axis = 'TRACK_Z'
            bend_bone_constraint.lock_axis = 'LOCK_Y'
            bend_bone_constraint.influence = 0.35


    # Go back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')        
