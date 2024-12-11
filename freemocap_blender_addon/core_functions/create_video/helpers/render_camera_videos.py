from pathlib import Path
from typing import Dict, Any

import bpy


def render_camera_videos(
        recording_folder: str,
        cameras_by_key: Dict[str, bpy.types.Object],
        render_camera_configs: Dict[str, Any],
) -> Dict[str, str]:
    # For each camera in the export profile cameras, render the animation
    rendered_videos_paths_by_camera_key = {}
    for camera_key, camera_object in cameras_by_key.items():

        # Set the camera
        bpy.context.scene.camera = camera_object
        print(f"Rendering animation for {camera_key} ...")

        # Set the render resolution based on the camera resolution
        bpy.context.scene.render.resolution_x = render_camera_configs[camera_key]['resolution_x']
        bpy.context.scene.render.resolution_y = render_camera_configs[camera_key]['resolution_y']

        # Set the output file name
        video_file_name = Path(recording_folder).name + '_' + camera_key + '.mp4'
        # Set the output file
        video_render_path = str(Path(recording_folder) / 'video_export' / 'render_cameras' / video_file_name)
        rendered_videos_paths_by_camera_key[camera_key] = video_render_path
        bpy.context.scene.render.filepath = video_render_path
        print(f"Exporting video to: {video_render_path} ...")

        # Render the animation
        bpy.ops.render.render(animation=True)

        if Path(video_render_path).exists():
            print(f"Render Camera Video file successfully created at: {video_render_path}")
        else:
            raise ValueError(f"Render Camera Video file was not created!! Nothing found at:  {video_render_path} ")
    return rendered_videos_paths_by_camera_key