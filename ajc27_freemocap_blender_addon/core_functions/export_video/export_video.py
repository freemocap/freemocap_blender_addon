import time
import bpy

from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.place_render_cameras import place_render_cameras
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.place_lights import place_lights
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.rearrange_background_videos import rearrange_background_videos
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.set_render_elements import set_render_elements
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.create_render_scenes import create_render_scenes
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.set_render_parameters import set_render_parameters
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.render_cameras import render_cameras
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.composite_video import composite_video
from ajc27_freemocap_blender_addon.core_functions.export_video.helpers.reset_scene_defaults import reset_scene_defaults

from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
)

def export_video(
    scene: bpy.types.Scene,
    recording_folder: str,
    start_frame: int,
    end_frame: int,
    export_profile: dict,
) -> None:

    place_render_cameras(scene, export_profile)
    place_lights(scene)
    rearrange_background_videos(scene, videos_x_separation=0.1)
    set_render_elements(scene, export_profile=export_profile)
    create_render_scenes(
        scene,
        recording_folder=recording_folder,
        export_profile=export_profile
    )
    set_render_parameters()

    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    
    # Render each camera scene if prerender_cameras is True in the profile
    # if EXPORT_PROFILES[export_profile]['prerender_cameras']:
    if export_profile['prerender_cameras']:
        start_time = time.perf_counter_ns()
        render_cameras(
            export_profile=export_profile,
        )
        end_time = time.perf_counter_ns()
        print(f"Rendering cameras time: {(end_time - start_time) / 1e9} seconds")

    # Set the main scene as the current scene
    bpy.context.window.scene = scene

    # Composite the final video
    start_time = time.perf_counter_ns()
    composite_video(
        scene=scene,
        recording_folder=recording_folder,
        export_profile=export_profile,
        start_frame=start_frame,
        end_frame=end_frame,
    )
    end_time = time.perf_counter_ns()
    print(f"Compositing video time: {(end_time - start_time) / 1e9} seconds")

    reset_scene_defaults()

    return
    