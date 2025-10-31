from copy import deepcopy
import bpy
from pathlib import Path

from ajc27_freemocap_blender_addon.core_functions.export_video.export_video import export_video
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
    RENDER_BACKGROUND
)
from ajc27_freemocap_blender_addon import PACKAGE_ROOT_PATH

class FREEMOCAP_OT_export_video(bpy.types.Operator):
    bl_idname = 'freemocap._export_video'
    bl_label = 'Export Video'
    bl_description = "Export the Freemocap Blender output as a video file"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene

        export_video_props = scene.freemocap_ui_properties.export_video_properties

        print("Exporting video.......")

        export_profile = deepcopy(EXPORT_PROFILES[export_video_props.export_profile])

        # Clear all existing compositor nodes and clips
        try:
            for node in bpy.context.scene.node_tree.nodes:
                bpy.context.scene.node_tree.nodes.remove(node)
        except:
            pass
        try:
            for clip in list(bpy.data.movieclips):
                bpy.data.movieclips.remove(clip)
        except:
            pass

        # Clear all the images with the name of the RENDER BACKGROUND file
        for img in list(bpy.data.images):
            if img.name.split('.')[0] in RENDER_BACKGROUND['base_image_path']:
                bpy.data.images.remove(img)

        # Clear all the scnes that have "Render_Camera" in their name
        for scene in list(bpy.data.scenes):
            if "Render_Camera" in scene.name:
                bpy.data.scenes.remove(scene)

        if export_video_props.export_profile == 'custom':
            
            export_profile['render_elements'] == []
            # Apply custom resolution settings
            export_profile['resolution_x'] = export_video_props.custom_profile_width
            export_profile['resolution_y'] = export_video_props.custom_profile_height

            # Add the camera angles
            export_profile['render_cameras'] = {}
            if export_video_props.custom_use_front_camera:
                export_profile['render_cameras']['Front'] = {
                    'resolution_x': export_video_props.custom_front_camera_width,
                    'resolution_y': export_video_props.custom_front_camera_height,
                    'scale_space': 'RELATIVE',
                    'scale_x': 1.0,
                    'scale_y': 1.0,
                    'translate_x': export_video_props.custom_front_camera_position_x,
                    'translate_y': export_video_props.custom_front_camera_position_y,
                    'view_margin': 0.1,
                }
            if export_video_props.custom_use_left_camera:
                export_profile['render_cameras']['Left'] = {
                    'resolution_x': export_video_props.custom_left_camera_width,
                    'resolution_y': export_video_props.custom_left_camera_height,
                    'scale_space': 'RELATIVE',
                    'scale_x': 1.0,
                    'scale_y': 1.0,
                    'translate_x': export_video_props.custom_left_camera_position_x,
                    'translate_y': export_video_props.custom_left_camera_position_y,
                    'view_margin': 0.1,
                }
            if export_video_props.custom_use_right_camera:
                export_profile['render_cameras']['Right'] = {
                    'resolution_x': export_video_props.custom_right_camera_width,
                    'resolution_y': export_video_props.custom_right_camera_height,
                    'scale_space': 'RELATIVE',
                    'scale_x': 1.0,
                    'scale_y': 1.0,
                    'translate_x': export_video_props.custom_right_camera_position_x,
                    'translate_y': export_video_props.custom_right_camera_position_y,
                    'view_margin': 0.1,
                }
            if export_video_props.custom_use_top_camera:
                export_profile['render_cameras']['Top'] = {
                    'resolution_x': export_video_props.custom_top_camera_width,
                    'resolution_y': export_video_props.custom_top_camera_height,
                    'scale_space': 'RELATIVE',
                    'scale_x': 1.0,
                    'scale_y': 1.0,
                    'translate_x': export_video_props.custom_top_camera_position_x,
                    'translate_y': export_video_props.custom_top_camera_position_y,
                    'view_margin': 0.1,
                }

            # Add overlays
            export_profile['overlays'] = {}
            if export_video_props.custom_overlays_add_freemocap_logo:
                export_profile['overlays']['logo'] = {
                    'type': 'image',
                    'path': str(Path(PACKAGE_ROOT_PATH) / "assets" / "freemocap_logo_white_outline.png"),
                    'scale_space': 'RELATIVE',
                    'scale_x': export_video_props.custom_overlays_freemocap_logo_scale_x,
                    'scale_y': export_video_props.custom_overlays_freemocap_logo_scale_y,
                    'translate_x': export_video_props.custom_overlays_freemocap_logo_position_x,
                    'translate_y': export_video_props.custom_overlays_freemocap_logo_position_y,
                }

        export_video(
            scene=context.scene,
            recording_folder=context.scene.freemocap_properties.recording_path,
            start_frame=scene.frame_start,
            end_frame=scene.frame_end,
            export_profile=export_profile,
        )

        print("Video export completed.")

        return {'FINISHED'}
