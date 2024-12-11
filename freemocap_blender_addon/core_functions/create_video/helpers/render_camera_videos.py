from pathlib import Path
from typing import Dict, Any

import bpy


def render_camera_videos(
        recording_folder: str,
        render_camera_configs: Dict[str, Any]):
    # For each camera in the export profile cameras, render the animation
    for camera_name, camera_config in render_camera_configs.items():

        # Set the camera
        bpy.context.scene.camera = bpy.data.objects['Camera_' + camera_name]
        print(f"Rendering animation for {camera_name} camera...")

        # Set the render resolution based on the camera resolution
        bpy.context.scene.render.resolution_x = camera_config['resolution_x']
        bpy.context.scene.render.resolution_y = camera_config['resolution_y']

        # Set the output file name
        video_file_name = Path(recording_folder).name + '_' + camera_name + '.mp4'
        # Set the output file
        video_render_path = str(Path(recording_folder) / 'video_export' / 'render_cameras' / video_file_name)
        bpy.context.scene.render.filepath = video_render_path
        print(f"Exporting video to: {video_render_path} ...")

        # Render the animation
        bpy.ops.render.render(animation=True)

        if Path(video_render_path).exists():
            print(f"Render Camera Video file successfully created at: {video_render_path}")
        else:
            raise ValueError(f"Render Camera Video file was not created!! Nothing found at:  {video_render_path} ")


