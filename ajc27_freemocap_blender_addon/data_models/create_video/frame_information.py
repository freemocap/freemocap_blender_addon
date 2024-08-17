from pathlib import Path
from ajc27_freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler

class frame_information:
    def __init__(
        self,
        file_directory: Path,
        width: int,
        height: int,
        total_frames: int,
        frame_start: int,
        handler: FreemocapDataHandler,
    ):
        self.file_directory = file_directory
        self.width = width
        self.height = height
        self.total_frames = total_frames
        self.frame_start = frame_start
        self.handler = handler
        self.frame_number = 0