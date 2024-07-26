from dataclasses import dataclass

import bpy


@dataclass
class FrameInformation:
    file_directory: str
    width: int
    height: int
    total_frames: int
    total_frames_digits: int
    frame_number: int = 0
    frame_start: int = 0
    frame_end: int = 0
    scene: bpy.types.Scene = None


pass