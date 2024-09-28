import bpy


def set_start_end_frame(number_of_frames: int):
    # %% Set start and end frames
    start_frame = 0
    end_frame = number_of_frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    print(f"Set start frame to {start_frame} and end frame to {end_frame}")
