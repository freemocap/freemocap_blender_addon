from enum import Enum

from freemocap_blender_addon.freemocap_data.file_path_dataclass_abc import FilePathDataclass

# Constants for placeholders
TRACKER_TYPE_PLACEHOLDER = "[tracker_type]"
RIGHT_LEFT_PLACEHOLDER = "[right_left]"
PARENT_DIRECTORY_PLACEHOLDER = "[parent_path]"
RECORDING_FOLDER_DIRECTORY_PLACEHOLDER = "[recording_folder_path]"

# Directory paths
SKELETON_NPY_PARENT_DIRECTORY = "[recording_folder_path]/output_data"
CENTER_OF_MASS_NPY_PARENT_DIRECTORY = "[recording_folder_path]/output_data/center_of_mass"
VIDEO_PARENT_DIRECTORY = "[recording_folder_path]"


# Enum Definitions
class TrackerType(Enum):
    MEDIAPIPE = "mediapipe"


DEFAULT_TRACKER_TYPE = TrackerType.MEDIAPIPE.value


class SkeletonNpyFiles(Enum):
    BODY_NPY_FILE = "[parent_path]/[tracker_type]_body_3d_xyz.npy"
    HAND_NPY_FILE = "[parent_path]/[tracker_type]_[right_left]_hand_3d_xyz.npy"
    FACE_NPY_FILE = "[parent_path]/[tracker_type]_face_3d_xyz.npy"
    REPROJECTION_ERROR_NPY_FILE = "[parent_path]/[tracker_type]3dData_numFrames_numTrackedPoints_reprojectionError.npy"


class CenterOfMassNpyFiles(Enum):
    TOTAL_BODY_CENTER_OF_MASS_NPY = "[parent_path]/total_body_center_of_mass_xyz.npy"
    SEGMENT_CENTER_OF_MASS_NPY = "[parent_path]/segment_center_of_mass_xyz.npy"


class VideoFolders(Enum):
    RAW = "[parent_path]/synchronized_videos"
    ANNOTATED = "[parent_path]/annotated_videos"


class RightLeft(Enum):
    RIGHT = "right"
    LEFT = "left"


from dataclasses import dataclass
from pathlib import Path
from typing import Dict


class HandNpyPaths(FilePathDataclass):
    right: Path
    left: Path

@dataclass
class SkeletonNpyPaths(FilePathDataclass):
    body: Path
    hands: Dict[RightLeft, Path]
    face: Path
    reprojection_error: Path



@dataclass
class CenterOfMassNpyPaths(FilePathDataclass):
    total_body_center_of_mass: Path
    segment_center_of_mass: Path


@dataclass
class FreemocapVideoPaths(FilePathDataclass):
    raw: Path
    annotated: Path



@dataclass
class FreemocapNpyPaths(FilePathDataclass):
    skeleton: SkeletonNpyPaths
    center_of_mass: CenterOfMassNpyPaths
    video: FreemocapVideoPaths

    @classmethod
    def from_recording_path(cls, path: str) -> 'FreemocapNpyPaths':
        parent_path = Path(path)

        def replace_placeholders(file_template: str, **replacements) -> Path:
            for key, value in replacements.items():
                file_template = file_template.replace(key, value)
            return Path(file_template)

        skeleton_npy_paths = SkeletonNpyPaths(
            body=replace_placeholders(SkeletonNpyFiles.BODY_NPY_FILE.value,
                                      parent_path=str(parent_path),
                                      tracker_type=DEFAULT_TRACKER_TYPE),
            hands={
                RightLeft.RIGHT: replace_placeholders(SkeletonNpyFiles.HAND_NPY_FILE.value,
                                                      parent_path=str(parent_path),
                                                      tracker_type=DEFAULT_TRACKER_TYPE,
                                                      right_left=RightLeft.RIGHT.value),
                RightLeft.LEFT: replace_placeholders(SkeletonNpyFiles.HAND_NPY_FILE.value,
                                                     parent_path=str(parent_path),
                                                     tracker_type=DEFAULT_TRACKER_TYPE,
                                                     right_left=RightLeft.LEFT.value)
            },
            face=replace_placeholders(SkeletonNpyFiles.FACE_NPY_FILE.value,
                                      parent_path=str(parent_path),
                                      tracker_type=DEFAULT_TRACKER_TYPE),
            reprojection_error=replace_placeholders(SkeletonNpyFiles.REPROJECTION_ERROR_NPY_FILE.value,
                                                    parent_path=str(parent_path),
                                                    tracker_type=DEFAULT_TRACKER_TYPE)
        )

        center_of_mass_npy_paths = CenterOfMassNpyPaths(
            total_body_center_of_mass=replace_placeholders(CenterOfMassNpyFiles.TOTAL_BODY_CENTER_OF_MASS_NPY.value,
                                                           parent_path=str(parent_path)),
            segment_center_of_mass=replace_placeholders(CenterOfMassNpyFiles.SEGMENT_CENTER_OF_MASS_NPY.value,
                                                        parent_path=str(parent_path))
        )

        video_paths = FreemocapVideoPaths(
            raw=replace_placeholders(VideoFolders.RAW.value, parent_path=str(parent_path)),
            annotated=replace_placeholders(VideoFolders.ANNOTATED.value, parent_path=str(parent_path))
        )

        return cls(skeleton=skeleton_npy_paths,
                   center_of_mass=center_of_mass_npy_paths,
                   video=video_paths)


# Example Usage
if __name__ == "__main__":
    paths = FreemocapNpyPaths.from_recording_path("~/example_recording")
    print(paths)
