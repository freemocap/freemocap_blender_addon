from typing import Any, Dict

import bpy

from freemocap_blender_addon.core_functions.create_video.helpers.rearrange_background_videos import \
    rearrange_background_videos
from freemocap_blender_addon.core_functions.create_video.helpers.render_camera_videos import render_camera_videos
from freemocap_blender_addon.core_functions.create_video.helpers.render_composite_video import composite_video
from freemocap_blender_addon.core_functions.create_video.helpers.reset_scene_defaults import reset_scene_defaults
from freemocap_blender_addon.core_functions.create_video.helpers.set_render_elements import set_render_elements
from freemocap_blender_addon.core_functions.create_video.helpers.set_render_parameters import set_render_parameters
from freemocap_blender_addon.core_functions.setup_scene.scene_objects.create_lights import create_lights
from freemocap_blender_addon.core_functions.setup_scene.scene_objects.create_render_cameras import \
    create_cameras_objects


def create_video(
        scene: bpy.types.Scene,
        recording_folder: str,
        start_frame: int,
        end_frame: int,
        render_parameters: Dict[str, Any],
        export_config: Dict[str, Any],
        fov_config: Dict[str, Any]):
    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    render_camera_configs = export_config['render_cameras']
    cameras_by_key = create_cameras_objects(scene=scene,
                                            render_camera_configs=render_camera_configs,
                                            camera_horizontal_fov=fov_config['horizontal_fov'],
                                            camera_vertical_fov=fov_config['vertical_fov'],
                                            )

    create_lights(scene=scene, camera_objects_by_key=cameras_by_key)

    # TODO - Use the to set the default video placement code
    rearrange_background_videos(scene, videos_x_separation=0.1)

    set_render_elements(render_elements=export_config['render_elements'])

    set_render_parameters(render_parameters=render_parameters)

    rendered_video_paths_by_camera_key = render_camera_videos(
        recording_folder=recording_folder,
        render_camera_configs=render_camera_configs,
        cameras_by_key=cameras_by_key,
    )

    # composite_video(
    #     scene=scene,
    #     recording_folder=recording_folder,
    #     export_config=export_config,
    #     render_camera_configs=render_camera_configs,
    #     rendered_video_paths_by_camera_key=rendered_video_paths_by_camera_key,
    # )

    reset_scene_defaults()
