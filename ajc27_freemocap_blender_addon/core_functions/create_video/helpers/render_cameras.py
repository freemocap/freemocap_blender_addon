import bpy
from pathlib import Path
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
)

def render_cameras(
    recording_folder: str,
    export_profile: str = 'debug',
) -> None:

    # For each camera in the export profile cameras, render the animation
    for camera in EXPORT_PROFILES[export_profile]['render_cameras']:

        # Set the camera
        bpy.context.scene.camera = bpy.data.objects['Camera_' + camera]
        print(f"Rendering animation for camera: {camera} ...")

        # Set the render resolution based on the camera resolution
        bpy.context.scene.render.resolution_x = EXPORT_PROFILES[export_profile]['render_cameras'][camera]['resolution_x']
        bpy.context.scene.render.resolution_y = EXPORT_PROFILES[export_profile]['render_cameras'][camera]['resolution_y']

        # Set the output file name
        video_file_name = Path(recording_folder).name + '_' + camera + '.mp4'
        # Set the output file
        video_render_path = str(Path(recording_folder) / 'video_export' / 'render_cameras' / video_file_name)
        bpy.context.scene.render.filepath = video_render_path
        print(f"Exporting video to: {video_render_path} ...")

        # Render the animation
        bpy.ops.render.render(animation=True)

        if  Path(video_render_path).exists():
            print(f"Render Camera Video file successfully created at: {video_render_path}")
        else:
            print("ERROR - Render Camera Video file was not created!! Nothing found at:  {video_render_path} ")

    return
