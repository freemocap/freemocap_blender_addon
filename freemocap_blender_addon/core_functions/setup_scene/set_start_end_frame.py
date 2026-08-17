import bpy


def set_start_end_frame(number_of_frames: int):
    # %% Set start and end frames
    start_frame = 0
    end_frame = number_of_frames
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    print(f"Set start frame to {start_frame} and end frame to {end_frame}")


def set_scene_framerate(framerate: float):
    """Set the scene framerate, which .blend/.fbx/.bvh exports inherit.

    Blender stores the rate as `fps / fps_base`, so a non-integer capture rate is expressed
    the same way 29.97 is (fps=30, fps_base=1.001) rather than being rounded away.
    """
    scene = bpy.context.scene
    rounded = max(1, round(framerate))
    scene.render.fps = rounded
    scene.render.fps_base = rounded / framerate
    effective = scene.render.fps / scene.render.fps_base
    print(f"Set scene framerate to {effective:.3f} fps (fps={scene.render.fps}, "
          f"fps_base={scene.render.fps_base:.6f})")