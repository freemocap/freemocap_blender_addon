import os
from pathlib import Path
from mathutils import Vector
import bpy
import cv2

from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler
from ajc27_freemocap_blender_addon import PACKAGE_ROOT_PATH
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
    RENDER_PARAMETERS,
)

from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.rearrange_background_videos import rearrange_background_videos
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.place_cameras import place_cameras
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.place_lights import place_lights
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.set_render_elements import set_render_elements
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.add_render_background import add_render_background
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.set_render_parameters import set_render_parameters
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.reset_scene_defaults import reset_scene_defaults

from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.frame_information_dataclass import FrameInformation
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.frame_number_overlay import OverlayFrameNumber
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.image_overlays import OverlayLogo
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.json_table_overlays import OverlayRecordingParameters
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.json_table_overlays import OverlayMediapipeSkeletonSegmentLengths
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.matplotlib_plot_overlays import OverlayPlotComBos
from ajc27_freemocap_blender_addon.core_functions.create_video.helpers.overlay_components.matplotlib_plot_overlays import OverlayPlotFootDeviation

def create_video(
    handler: FreemocapDataHandler,
    scene: bpy.types.Scene,
    recording_folder: str,
    start_frame: int,
    end_frame: int,
    export_profile: str = 'scientific',
) -> None:

    # Place the required cameras
    cameras_positions = place_cameras(scene, export_profile)

    # Place the required lights
    place_lights(scene, cameras_positions)

    # Rearrange the background videos
    rearrange_background_videos(scene, videos_x_separation=0.1)

    set_render_elements(export_profile=export_profile)

    add_render_background(scene, export_profile=export_profile)

    # Set the rendering properties
    set_render_parameters()

    # Set the render resolution based on the export profile
    bpy.context.scene.render.resolution_x = EXPORT_PROFILES[export_profile]['resolution_x']
    bpy.context.scene.render.resolution_y = EXPORT_PROFILES[export_profile]['resolution_y']

    # Set the output file name
    video_file_name = Path(recording_folder).name + '.mp4'
    # Set the output file
    video_render_path = str(Path(recording_folder) / video_file_name)
    bpy.context.scene.render.filepath = video_render_path
    print(f"Exporting video to: {video_render_path} ...")

    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = start_frame + 50

    # Render the animation
    bpy.ops.render.render(animation=True)

    # Reset the scene defaults
    reset_scene_defaults()

    # Add the visual components
    add_visual_components(render_path=video_render_path,
                          file_directory=recording_folder,
                          export_profile=export_profile,
                          start_frame=start_frame,
                          handler=handler
    )

    if  Path(video_render_path).exists():
        print(f"Video file successfully created at: {video_render_path}")
    else:
        print("ERROR - Video file was not created!! Nothing found at:  {video_render_path} ")

    return

def add_visual_components(
    render_path: str,
    file_directory: Path,
    export_profile: str='debug',
    start_frame: int=0,
    handler: FreemocapDataHandler=None,
) -> None:

    # Get a reference to the render
    video = cv2.VideoCapture(render_path)

    # Create a VideoWriter object to write the output frames
    output_writer = cv2.VideoWriter(
        (os.path.dirname(render_path)
        + '/' + os.path.basename(render_path)[:-4]
        + '_' + export_profile + '.mp4'),
        cv2.VideoWriter_fourcc(*'mp4v'),
        RENDER_PARAMETERS['scene.render.fps'],
        (EXPORT_PROFILES[export_profile]['resolution_x'],
         EXPORT_PROFILES[export_profile]['resolution_y']),
         EXPORT_PROFILES[export_profile]['bitrate'],
    )
    
    # Create new frame_info object
    frame_info = FrameInformation(
        file_directory=str(file_directory),
        width=EXPORT_PROFILES[export_profile]['resolution_x'],
        height=EXPORT_PROFILES[export_profile]['resolution_y'],
        total_frames=int(video.get(cv2.CAP_PROP_FRAME_COUNT)),
        total_frames_digits=len(str(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))),
        handler=handler,
        frame_start=start_frame,
        scene=bpy.context.scene
    )

    # Create the visual component objects list
    visual_components_list = []
    for visual_component in EXPORT_PROFILES[export_profile]['visual_components']:
        if visual_component == "frame_number":
            visual_component_class = OverlayFrameNumber
        elif visual_component == "logo":
            visual_component_class = OverlayLogo
        elif visual_component == "recording_parameters":
            visual_component_class = OverlayRecordingParameters
        elif visual_component == "mediapipe_skeleton_segment_lengths":
            visual_component_class = OverlayMediapipeSkeletonSegmentLengths
        elif visual_component == "plot_com_bos":
            visual_component_class = OverlayPlotComBos
        elif visual_component == "plot_foot_deviation":
            visual_component_class = OverlayPlotFootDeviation
        else:
            raise ValueError("Invalid visual component: " + visual_component)

        visual_components_list.append(visual_component_class(frame_info))

    index_frame = 0
    # Add the logo to the video
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        # Update the frame number in frame_info
        frame_info.frame_number = index_frame

        # Add each visual component
        for visual_component in visual_components_list:
            frame = visual_component.add_component(frame, frame_info)

        # Write the frame
        output_writer.write(frame)

        index_frame += 1

    video.release()
    output_writer.release()
    cv2.destroyAllWindows()

    return
