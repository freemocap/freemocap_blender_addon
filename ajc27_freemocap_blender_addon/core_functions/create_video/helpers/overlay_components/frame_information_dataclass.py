from dataclasses import dataclass
from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler
import bpy


@dataclass
class FrameInformation:
    file_directory: str
    width: int
    height: int
    total_frames: int
    total_frames_digits: int
    handler: FreemocapDataHandler
    scene: bpy.types.Scene
    frame_start: int = 0
    frame_end: int = 0
    frame_number: int = 0

