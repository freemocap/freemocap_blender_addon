import bpy

from ajc27_freemocap_blender_addon.core_functions.motion_path.add_motion_path import add_motion_path

class FREEMOCAP_OT_add_motion_path(bpy.types.Operator):
    bl_idname = 'freemocap._add_motion_path'
    bl_label = 'Add Motion Path'
    bl_description = "Add Motion Path"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Adding Motion Path.......")
        ui_props = context.scene.freemocap_ui_properties

        # Add Motion Path
        add_motion_path(
            context=context,
            data_object_basename=ui_props.motion_path_target_element,
            show_line=ui_props.motion_path_show_line,
            line_thickness=ui_props.motion_path_line_thickness,
            use_custom_color=True,
            line_color=ui_props.motion_path_line_color,
            line_color_post=ui_props.motion_path_line_color_post,
            frames_before=ui_props.motion_path_frames_before,
            frames_after=ui_props.motion_path_frames_after,
            frame_step=ui_props.motion_path_frame_step,
            show_frame_numbers=ui_props.motion_path_show_frame_numbers,
            show_keyframes=ui_props.motion_path_show_keyframes,
            show_keyframe_number=ui_props.motion_path_show_keyframe_number
        )

        return {'FINISHED'}
    
