import bpy
import math

from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.bone_rotation_limits import BONE_ROTATION_LIMITS


class FREEMOCAP_OT_set_bone_rotation_limits(bpy.types.Operator):
    bl_idname = 'freemocap._set_bone_rotation_limits'
    bl_label = 'Set Bone Rotation Limits'
    bl_description = "Set Bone Rotation Limits"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Setting bone rotation limits.......")
       
        data_parent_empty = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]

        # Go to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        armature = None

        # Get the reference to the armature object
        for child in data_parent_empty.children_recursive:
            if child.type == 'ARMATURE':
                armature = child
                break

        if armature is None:
            print("No armature found for the data parent: " + data_parent_empty.name)
            return {'FINISHED'}

        # Set the limit rotation constraints on the pose bones
        for bone in BONE_ROTATION_LIMITS.keys():
            if bone in armature.pose.bones:
                bone_constraint = armature.pose.bones[bone].constraints.new(
                    'LIMIT_ROTATION'
                )
                bone_constraint.owner_space = 'LOCAL'
                bone_constraint.use_limit_x = True
                bone_constraint.use_limit_y = True
                bone_constraint.use_limit_z = True
                bone_constraint.min_x = math.radians(BONE_ROTATION_LIMITS[bone]['x'][0])
                bone_constraint.max_x = math.radians(BONE_ROTATION_LIMITS[bone]['x'][1])
                bone_constraint.min_y = math.radians(BONE_ROTATION_LIMITS[bone]['y'][0])
                bone_constraint.max_y = math.radians(BONE_ROTATION_LIMITS[bone]['y'][1])
                bone_constraint.min_z = math.radians(BONE_ROTATION_LIMITS[bone]['z'][0])
                bone_constraint.max_z = math.radians(BONE_ROTATION_LIMITS[bone]['z'][1])
        
        return {'FINISHED'}
