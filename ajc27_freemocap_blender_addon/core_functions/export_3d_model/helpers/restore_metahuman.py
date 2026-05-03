import bpy

def restore_metahuman_edit_mode(armature: bpy.types.Object):
    """
    Restore Metahuman specific bone structures in Edit Mode.
    Must be called while the armature is in Edit Mode.
    """
    # Reparent the thigh bones to the pelvis
    for bone in armature.data.edit_bones:
        if 'thigh' in bone.name:
            if 'thigh.R' in bone.name:
                bone.parent = armature.data.edit_bones.get('pelvis.R')
            elif 'thigh.L' in bone.name:
                bone.parent = armature.data.edit_bones.get('pelvis.L')
            bone.use_connect = True

        if 'shoulder' in bone.name or 'neck' in bone.name:
            bone.use_connect = True
            
    # Recreate the thumb.carpal bones
    for side in ['.L', '.R']:
        if 'thumb.carpal' + side not in armature.data.edit_bones:
            hand_bone = armature.data.edit_bones.get('hand' + side)
            thumb_01_bone = armature.data.edit_bones.get('thumb.01' + side)
            if hand_bone and thumb_01_bone:
                new_bone = armature.data.edit_bones.new(name='thumb.carpal' + side)
                new_bone.head = hand_bone.head.copy()
                new_bone.tail = thumb_01_bone.head.copy()
                new_bone.roll = 0.0
                new_bone.parent = hand_bone
                new_bone.use_connect = False


def restore_metahuman_pose_mode(armature: bpy.types.Object, data_parent_empty: bpy.types.Object):
    """
    Restore Metahuman specific constraints and settings in Pose Mode.
    """
    # Restore the hand bone constraints target markers
    for side in ['left', 'right']:
        hand_bone_name = 'hand' + '.' + side[0].upper()
        if hand_bone_name in armature.pose.bones:
            hand_bone = armature.pose.bones[hand_bone_name]

            # Get the hand_middle
            hand_middle = [
                marker for marker in data_parent_empty.children_recursive
                if side + '_hand_middle' == marker.name or side + '_hand_middle.' in marker.name
            ]
            
            # Get the hand_thumb_cmc
            hand_thumb_cmc = [
                marker for marker in data_parent_empty.children_recursive
                if side + '_hand_thumb_cmc' in marker.name
            ]

            if hand_middle and 'Damped Track' in hand_bone.constraints:
                hand_bone.constraints['Damped Track'].target = hand_middle[0]
            if hand_thumb_cmc and 'Locked Track' in hand_bone.constraints:
                hand_bone.constraints['Locked Track'].target = hand_thumb_cmc[0]

    # Remove specific correction constraints
    constraints_to_remove = {
        "spine": ["Metahuman_Spine_01_Correction"],
        "spine.001": ["Metahuman_Spine_04_Correction"],
        "neck": ["Metahuman_Neck_Location_Correction", "Metahuman_Neck_Correction"],
        "face": ["Metahuman_Head_Correction"]
    }
    
    for bone_name, constraint_names in constraints_to_remove.items():
        if bone_name in armature.pose.bones:
            bone = armature.pose.bones[bone_name]
            for c_name in constraint_names:
                if c_name in bone.constraints:
                    bone.constraints.remove(bone.constraints[c_name])
