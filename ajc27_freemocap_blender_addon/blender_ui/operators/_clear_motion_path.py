import bpy

from ajc27_freemocap_blender_addon.core_functions.motion_path.clear_motion_path import clear_motion_path

class FREEMOCAP_OT_clear_motion_path(bpy.types.Operator):
    bl_idname = 'freemocap._clear_motion_path'
    bl_label = 'Clear Motion Path'
    bl_description = "Clear Motion Path"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Clearing Motion Path.......")
        ui_props = context.scene.freemocap_ui_properties

        # Add Motion Path
        clear_motion_path(
            context=context,
            data_object_basename=ui_props.motion_path_target_element,
        )

        return {'FINISHED'}
