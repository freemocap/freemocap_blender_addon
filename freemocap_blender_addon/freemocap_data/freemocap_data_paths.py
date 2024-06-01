from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from pprint import pprint
from typing import Union, Optional, Dict

import numpy as np


class DataSourceType(str, Enum):
    MEDIAPIPE = "mediapipe"
    OPENPOSE = "openpose"


DEFAULT_DATA_SOURCE = DataSourceType.MEDIAPIPE

# Constants for placeholders
TRACKER_TYPE_PLACEHOLDER = "TRACKER_TYPE_PLACEHOLDER"
RIGHT_LEFT_PLACEHOLDER = "RIGHT_LEFT_PLACEHOLDER"
RECORDING_PATH_PLACEHOLDER = "RECORDING_PATH_PLACEHOLDER"

# Directory paths
SKELETON_NPY_PARENT_DIRECTORY = f"{RECORDING_PATH_PLACEHOLDER}/output_data"
CENTER_OF_MASS_NPY_PARENT_DIRECTORY = f"{RECORDING_PATH_PLACEHOLDER}/output_data/center_of_mass"
VIDEO_PARENT_DIRECTORY = f"{RECORDING_PATH_PLACEHOLDER}"


class SkeletonNpyFiles(str, Enum):
    BODY_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/{TRACKER_TYPE_PLACEHOLDER}_body_3d_xyz.npy"
    HAND_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/{TRACKER_TYPE_PLACEHOLDER}_{RIGHT_LEFT_PLACEHOLDER}_hand_3d_xyz.npy"
    FACE_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/{TRACKER_TYPE_PLACEHOLDER}_face_3d_xyz.npy"
    REPROJECTION_ERROR_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/raw_data/{TRACKER_TYPE_PLACEHOLDER}3dData_numFrames_numTrackedPoints_reprojectionError.npy"


class CenterOfMassNpyFiles(str, Enum):
    TOTAL_BODY_CENTER_OF_MASS_NPY = f"{CENTER_OF_MASS_NPY_PARENT_DIRECTORY}/total_body_center_of_mass_xyz.npy"
    SEGMENT_CENTER_OF_MASS_NPY = f"{CENTER_OF_MASS_NPY_PARENT_DIRECTORY}/segmentCOM_frame_joint_xyz.npy"


class VideoFolders(str, Enum):
    RAW = f"{RECORDING_PATH_PLACEHOLDER}/synchronized_videos"
    ANNOTATED = f"{RECORDING_PATH_PLACEHOLDER}/annotated_videos"


class RightLeft(str, Enum):
    RIGHT = "right"
    LEFT = "left"


@dataclass
class PathsDataclass:
    def __post_init__(self):
        for field in self.__dict__.values():
            if isinstance(field, Path):
                if not field.exists():
                    raise FileNotFoundError(f"Path {field} does not exist")

    def __str__(self):
        classname = self.__class__.__name__
        fields = [f"\t{k}: {v}" for k, v in self.__dict__.items()]
        joined_fields = "\n".join(fields)


@dataclass
class NpyPaths(PathsDataclass):
    def __post_init__(self):
        super().__post_init__()
        for field in self.__dict__.values():
            if isinstance(field, NpyPaths):
                continue
            try:
                npy_data = np.load(str(field))
                if npy_data.size == 0:
                    raise ValueError(f"Empty npy file: {field}")
            except FileNotFoundError:
                raise FileNotFoundError(f"Path {field} does not exist")

    def __str__(self):
        return super().__str__()


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


@dataclass
class HandsNpyPaths(NpyPaths):
    right: str
    left: str


@dataclass
class SkeletonNpyPaths(NpyPaths):
    body: str
    hands: HandsNpyPaths
    face: str
    reprojection_error: str


@dataclass
class CenterOfMassNpyPaths(NpyPaths):
    total_body_center_of_mass: str
    segment_center_of_mass: str


@dataclass
class FreemocapDataPaths:
    recording_folder_path: str
    skeleton: SkeletonNpyPaths
    center_of_mass: CenterOfMassNpyPaths
    video: FreemocapVideoPaths

    @classmethod
    def from_recording_path(cls, path: str, data_source: DataSourceType) -> 'FreemocapDataPaths':

        if not Path(path).exists():
            raise FileNotFoundError(f"Path {path} does not exist")

        replacements: Dict[str, Union[str, DataSourceType]] = {
            TRACKER_TYPE_PLACEHOLDER: data_source.value,
            RECORDING_PATH_PLACEHOLDER: path,
        }

        def replace_placeholders(file_template: str, right_left: Optional[RightLeft] = None) -> str:
            for key, value in replacements.items():
                file_template = file_template.replace(key, value)
            if right_left:
                file_template = file_template.replace(RIGHT_LEFT_PLACEHOLDER, right_left.value)
            return file_template

        hands = HandsNpyPaths(
            right=replace_placeholders(SkeletonNpyFiles.HAND_NPY_FILE.value, RightLeft.RIGHT),
            left=replace_placeholders(SkeletonNpyFiles.HAND_NPY_FILE.value, RightLeft.LEFT)
        )

        skeleton_npy_paths = SkeletonNpyPaths(
            body=replace_placeholders(SkeletonNpyFiles.BODY_NPY_FILE.value),
            hands=hands,
            face=replace_placeholders(SkeletonNpyFiles.FACE_NPY_FILE.value),
            reprojection_error=replace_placeholders(SkeletonNpyFiles.REPROJECTION_ERROR_NPY_FILE.value)
        )

        center_of_mass_npy_paths = CenterOfMassNpyPaths(
            total_body_center_of_mass=replace_placeholders(CenterOfMassNpyFiles.TOTAL_BODY_CENTER_OF_MASS_NPY.value),
            segment_center_of_mass=replace_placeholders(CenterOfMassNpyFiles.SEGMENT_CENTER_OF_MASS_NPY.value)
        )

        video_paths = FreemocapVideoPaths(
            raw=VideoFolder(replace_placeholders(VideoFolders.RAW.value)),
            annotated=VideoFolder(replace_placeholders(VideoFolders.ANNOTATED.value))
        )

        return cls(
            recording_folder_path=path,
            skeleton=skeleton_npy_paths,
            center_of_mass=center_of_mass_npy_paths,
            video=video_paths
        )


# Example Usage
if __name__ == "__main__":
    from freemocap_blender_addon.core_functions.setup_scene.get_path_to_test_data import get_path_to_test_data

    paths = FreemocapDataPaths.from_recording_path(path=get_path_to_test_data(),
                                                   data_source=DEFAULT_DATA_SOURCE)
    pprint(paths)
