from bpy.types import Operator

from freemocap_video_export.create_video.create_video import create_export_video


class FMC_ADAPTER_OT_export_video(Operator):
    bl_idname = 'fmc_export_video.export_video'
    bl_label = 'Freemocap Export Video'
    bl_description = "Export the Freemocap Blender output as a video file"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_video_export_tool = scene.fmc_video_export_tool

        print("Exporting video.......")

        config_variables.visual_components['plot_com_bos'][
            'ground_contact_threshold'] = fmc_video_export_tool.ground_contact_threshold

        create_export_video(scene=scene, export_profile=fmc_video_export_tool.export_profile)

        print("Video export completed.")

        return {'FINISHED'}
