import bpy

from ajc27_freemocap_blender_addon.core_functions.export_video.export_video import export_video

class FREEMOCAP_OT_export_video(bpy.types.Operator):
    bl_idname = 'freemocap._export_video'
    bl_label = 'Export Video'
    bl_description = "Export the Freemocap Blender output as a video file"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene

        export_video_props = scene.freemocap_ui_properties.export_video_properties

        print("Exporting video.......")

        export_video(
            scene=context.scene,
            recording_folder=context.scene.freemocap_properties.recording_path,
            start_frame=scene.frame_start,
            end_frame=scene.frame_end,
            export_profile=export_video_props.export_profile,
        )

        print("Video export completed.")

        return {'FINISHED'}
