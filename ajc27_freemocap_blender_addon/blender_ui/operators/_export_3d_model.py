import bpy

from ajc27_freemocap_blender_addon.core_functions.export_3d_model.export_3d_model import export_3d_model

class FREEMOCAP_OT_export_3d_model(bpy.types.Operator):
    bl_idname = 'freemocap._export_3d_model'
    bl_label = 'Export 3D Model'
    bl_description = "Export 3D Model"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        
        props = context.scene.freemocap_ui_properties.export_3d_model_properties

        print("Exporting 3D model.......")

        data_parent_empty = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]

        # Get the armature object from the data parent
        armature = None
        for child in data_parent_empty.children_recursive:
            if child.type == 'ARMATURE':
                armature = child
                break

        if armature is None:
            print("No armature found for the data parent: " + data_parent_empty.name)
            return {'FINISHED'}
        
        # Get the model destination path
        model_destination_folder = bpy.path.abspath(props.model_destination_folder)

        # If the model destination path is empty, return
        if model_destination_folder == '':
            print("Model destination path is empty")
            self.report({'INFO'}, "Model destination path is empty")
            # bpy.ops.wm.simple_popup('INVOKE_DEFAULT', message="This is a popup!")
            return {'FINISHED'}

        export_3d_model(
            data_parent_empty=data_parent_empty,
            armature=armature,
            formats=[props.model_format],
            destination_folder=model_destination_folder,
            add_subfolder=False,
            rename_root_bone=True,
            bones_naming_convention=props.bones_naming_convention,
            rest_pose_type=props.rest_pose_type,
            restore_defaults_after_export=props.restore_defaults_after_export,
            fbx_add_leaf_bones=props.fbx_add_leaf_bones,
            fbx_primary_bone_axis=props.fbx_primary_bone_axis,
            fbx_secondary_bone_axis=props.fbx_secondary_bone_axis,
        )

        return {'FINISHED'}
