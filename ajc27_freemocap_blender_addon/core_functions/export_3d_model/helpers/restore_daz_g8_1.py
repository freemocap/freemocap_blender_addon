import bpy

def restore_daz_g8_1_edit_mode(armature: bpy.types.Object):
    """
    Restore DAZ G8.1 specific bone structures in Edit Mode.
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
                
    # Remove the forearm twist bones if they were created
    for side in ['.L', '.R']:
        twist_bone_name = 'forearm_twist' + side
        if twist_bone_name in armature.data.edit_bones:
            bone = armature.data.edit_bones[twist_bone_name]
            armature.data.edit_bones.remove(bone)


def restore_daz_g8_1_pose_mode(armature: bpy.types.Object):
    """
    Restore DAZ G8.1 specific constraints and settings in Pose Mode.
    """
    # Remove specific correction constraints
    constraints_to_remove = {
        "face": ["DazG8.1_Face_Correction"],
        "pelvis": ["DazG8.1_Pelvis_Correction"],
        "spine": ["DazG8.1_Spine_Correction"],
    }
    
    for bone_name, constraint_names in constraints_to_remove.items():
        if bone_name in armature.pose.bones:
            bone = armature.pose.bones[bone_name]
            for c_name in constraint_names:
                if c_name in bone.constraints:
                    bone.constraints.remove(bone.constraints[c_name])
                    
    # Forearm constraints
    for side in ['.L', '.R']:
        forearm_bone_name = 'forearm' + side
        if forearm_bone_name in armature.pose.bones:
            forearm_bone = armature.pose.bones[forearm_bone_name]
            if "DazG8.1_Forearm_Bend_Correction" in forearm_bone.constraints:
                constraint = forearm_bone.constraints["DazG8.1_Forearm_Bend_Correction"]
                forearm_bone.constraints.remove(constraint)
