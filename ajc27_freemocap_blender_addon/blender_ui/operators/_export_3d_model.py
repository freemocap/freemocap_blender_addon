import bpy

from ajc27_freemocap_blender_addon.core_functions.export_3d_model.export_3d_model import export_3d_model
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes

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
            armature=armature,
            formats=[props.model_format],
            destination_folder=model_destination_folder,
            add_subfolder=False,
            rename_root_bone=True,
            add_leaf_bones=props.fbx_add_leaf_bones
        )

        return {'FINISHED'}
    
# bpy.utils.register_class(SimplePopupOperator)
# class SimplePopupOperator(bpy.types.Operator):
#     bl_idname = "wm.simple_popup"
#     bl_label = "Popup Message"

#     message: PropertyTypes.String() # type: ignore

#     def execute(self, context):
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         return context.window_manager.invoke_props_dialog(self)

#     def draw(self, context):
#         layout = self.layout
#         layout.label(text=self.message)


