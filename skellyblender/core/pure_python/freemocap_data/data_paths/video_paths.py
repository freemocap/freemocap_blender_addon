from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from skellyblender.core.pure_python.freemocap_data.data_paths.paths_dataclass import PathsDataclass


class AvailableVideoFormats(str, Enum):
    MP4 = "mp4"
    AVI = "avi"
    MOV = "mov"


DEFAULT_VIDEO_FORMAT = AvailableVideoFormats.MP4


@dataclass
class VideoFolder(PathsDataclass):
    path: str
    format: AvailableVideoFormats = DEFAULT_VIDEO_FORMAT

    def __post_init__(self):
        if not Path(self.path).exists():
            raise FileNotFoundError(f"Path {self.path} does not exist")
        if not Path(self.path).is_dir():
            raise ValueError(f"Path {self.path} is not a directory")
        if len(self.videos) == 0:
            raise FileNotFoundError(f"No videos found in {self.path}")

    @property
    def videos(self):
        return [video for video in Path(self.path).iterdir() if video.suffix.lower() == f".{self.format.value}"]

    def __str__(self):
        out_str = f"{Path(self.path).name} (format:{self.format.value}):\n"
        for video in self.videos:
            out_str += f"\t{video.name}\n"
        return out_str


@dataclass
class FreemocapVideoPaths(PathsDataclass):
    raw: VideoFolder
    annotated: VideoFolder
