import time
from pathlib import Path

import bpy


def create_video(scene: bpy.types.Scene,
                 recording_folder: str,
                 start_frame: int,
                 end_frame: int,
                 export_profile: str = 'debug',) -> None:

    # Set the output file name
    video_file_name = Path(recording_folder).name + '.mp4'
    # Set the output file
    video_render_path = str(Path(recording_folder) / video_file_name)
    bpy.context.scene.render.filepath = video_render_path
    print(f"Exporting video to: {video_render_path} ...")

    # Set the output format to MPEG4
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'

    # Set the codec
    bpy.context.scene.render.ffmpeg.codec = 'H264'

    # Set the start and end frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Get start time
    start = time.time()


    # Render the animation
    bpy.ops.render.render(animation=True)



    if  Path(video_render_path).exists():
        print(f"Video file successfully created at: {video_render_path}")
    else:
        print("ERROR - Video file was not created!! Nothing found at:  {video_render_path} ")
    