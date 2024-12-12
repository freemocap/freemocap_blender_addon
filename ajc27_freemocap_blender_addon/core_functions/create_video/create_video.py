import bpy

from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.place_render_cameras import place_render_cameras
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.place_lights import place_lights
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.rearrange_background_videos import rearrange_background_videos
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.set_render_elements import set_render_elements
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.set_render_parameters import set_render_parameters
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.render_cameras import render_cameras
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.composite_video import composite_video
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.reset_scene_defaults import reset_scene_defaults

from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
)

def create_video(
    scene: bpy.types.Scene,
    recording_folder: str,
    start_frame: int,
    end_frame: int,
    export_profile: str = 'debug',
) -> None:

    place_render_cameras(scene, export_profile)

    place_lights(scene)

    rearrange_background_videos(scene, videos_x_separation=0.1)

    set_render_elements(export_profile=export_profile)

    set_render_parameters()

    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    render_cameras(
        recording_folder=recording_folder,
        export_profile=export_profile,
    )

    composite_video(
        scene=scene,
        recording_folder=recording_folder,
        export_profile=export_profile,
    )

    reset_scene_defaults()

    return
    