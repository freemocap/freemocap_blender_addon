import bpy

from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.ui_utilities import find_matching_bone_in_target_list

class FREEMOCAP_OT_detect_bone_mapping(bpy.types.Operator):
    bl_idname = 'freemocap._detect_bone_mapping'
    bl_label = 'Detect Bone Mapping'
    bl_description = "Detect Bone Mapping"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Detecting bone mapping.......")

        animation_props = context.scene.freemocap_ui_properties.retarget_animation_properties

        # Get source and target pose bones names
        source_armature = animation_props.retarget_source_armature

        animation_props.retarget_pairs.clear()
        for bone in bpy.data.objects[source_armature].pose.bones:
            pair = animation_props.retarget_pairs.add()
            pair.source_bone = bone.name

        target_armature = animation_props.retarget_target_armature
        target_pose_bones = bpy.data.objects[target_armature].pose.bones

        for pair in animation_props.retarget_pairs:
            pair.target_bone = find_matching_bone_in_target_list(pair.source_bone, target_pose_bones.keys())

        return {'FINISHED'}
