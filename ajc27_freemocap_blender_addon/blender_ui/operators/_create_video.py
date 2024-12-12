import bpy


class FREEMOCAP_OT_create_video(bpy.types.Operator):
    bl_idname = 'fmc_export_video.export_video'
    bl_label = 'Freemocap Export Video'
    bl_description = "Export the Freemocap Blender output as a video file"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene

        print("Exporting video.......")

        # config_variables.visual_components['plot_com_bos'][
        #     'ground_contact_threshold'] = scene.freemocap_properties.ground_contact_threshold
        #
        # create_export_video(scene=scene, export_profile=scene.freemocap_properties.export_profile)

        print("Video export completed.")

        return {'FINISHED'}
