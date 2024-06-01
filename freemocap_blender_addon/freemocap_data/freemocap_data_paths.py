from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from pprint import pprint
from typing import Union, Optional, Dict

import numpy as np

# Constants for placeholders
TRACKER_TYPE_PLACEHOLDER = "TRACKER_TYPE_PLACEHOLDER"
RIGHT_LEFT_PLACEHOLDER = "RIGHT_LEFT_PLACEHOLDER"
RECORDING_PATH_PLACEHOLDER = "RECORDING_PATH_PLACEHOLDER"

# Directory paths
SKELETON_NPY_PARENT_DIRECTORY = "RECORDING_PATH_PLACEHOLDER/output_data"
CENTER_OF_MASS_NPY_PARENT_DIRECTORY = "RECORDING_PATH_PLACEHOLDER/output_data/center_of_mass"
VIDEO_PARENT_DIRECTORY = "RECORDING_PATH_PLACEHOLDER"


# Enum Definitions
class TrackerType(str, Enum):
    MEDIAPIPE = "mediapipe"


DEFAULT_TRACKER_TYPE = TrackerType.MEDIAPIPE


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

@dataclass
class FreemocapVideoPaths(PathsDataclass):
    raw: Path
    annotated: Path


@dataclass
class HandsNpyPaths(NpyPaths):
    right: Path
    left: Path


@dataclass
class SkeletonNpyPaths(NpyPaths):
    body: Path
    hands: HandsNpyPaths
    face: Path
    reprojection_error: Path


@dataclass
class CenterOfMassNpyPaths(NpyPaths):
    total_body_center_of_mass: Path
    segment_center_of_mass: Path


@dataclass
class FreemocapNpyPaths:
    recording_folder_path: Path
    skeleton: SkeletonNpyPaths
    center_of_mass: CenterOfMassNpyPaths
    video: FreemocapVideoPaths

    @classmethod
    def from_recording_path(cls, path: str, tracker_type: TrackerType = DEFAULT_TRACKER_TYPE) -> 'FreemocapNpyPaths':

        parent_path = Path(path)
        if not parent_path.exists():
            raise FileNotFoundError(f"Path {parent_path} does not exist")

        replacements: Dict[str, Union[str, TrackerType]] = {
            TRACKER_TYPE_PLACEHOLDER: tracker_type.value,
            RECORDING_PATH_PLACEHOLDER: str(parent_path),
        }

        def replace_placeholders(file_template: str, right_left: Optional[RightLeft] = None) -> Path:
            for key, value in replacements.items():
                file_template = file_template.replace(key, value)
            if right_left:
                file_template = file_template.replace(RIGHT_LEFT_PLACEHOLDER, right_left.value)
            return Path(file_template)

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
            raw=replace_placeholders(VideoFolders.RAW.value),
            annotated=replace_placeholders(VideoFolders.ANNOTATED.value)
        )

        return cls(
            recording_folder_path=parent_path,
            skeleton=skeleton_npy_paths,
            center_of_mass=center_of_mass_npy_paths,
            video=video_paths
        )


# Example Usage
if __name__ == "__main__":
    test_data_path = Path().home() / "freemocap_data" / "recording_sessions" / "freemocap_test_data"
    paths = FreemocapNpyPaths.from_recording_path(path=str(test_data_path))
    pprint(paths)
