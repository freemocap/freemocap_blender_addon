import bpy
from pathlib import Path
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
)

# Funtion to create individual render scenes for each camera in the scene
# This helps to manage rendering settings and compositing for each camera separately
def create_render_scenes(
    scene: bpy.types.Scene,
    recording_folder: str,
    export_profile: dict,
) -> None:
    
    # Get a list of all cameras in the scene
    cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']

    for camera in cameras:
        # Create a new scene for each camera
        bpy.ops.scene.new(type='LINK_COPY')
        render_scene = bpy.context.scene
        render_scene.name = f"Render_{camera.name}"

        # Set the camera as the active camera for the new scene
        render_scene.camera = camera

        # Set render resolution based on the export profile and camera settings
        camera_settings = export_profile['render_cameras']
        render_scene.render.resolution_x = camera_settings[camera.name.split('_')[1]]['resolution_x']
        render_scene.render.resolution_y = camera_settings[camera.name.split('_')[1]]['resolution_y']

        # Set the output file name
        video_file_name = Path(recording_folder).name + '_' + camera.name.split('_')[1] + '.mp4'
        # Set the output file
        video_render_path = str(Path(recording_folder) / 'video_export' / 'render_cameras' / video_file_name)
        bpy.context.scene.render.filepath = video_render_path


    # Set the current scene back to the original scene
    bpy.context.window.scene = scene        

    return