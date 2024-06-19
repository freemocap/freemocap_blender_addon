from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Union, Optional, Dict

from skelly_blender.core.pure_python.load_data.data_paths.default_path_enums import PathPlaceholders, RightLeft, \
    SkeletonNpyFiles, CenterOfMassNpyFiles, VideoFolders
from skelly_blender.core.pure_python.load_data.data_paths.numpy_paths import SkeletonNpyPaths, CenterOfMassNpyPaths, \
    HandsNpyPaths
from skelly_blender.core.pure_python.load_data.data_paths.video_paths import FreemocapVideoPaths, VideoFolder
from skelly_blender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import DEFAULT_TRACKER_TYPE, \
    TrackerSourceType


@dataclass
class FreemocapDataPaths:
    recording_folder_path: str
    skeleton: SkeletonNpyPaths
    center_of_mass: CenterOfMassNpyPaths
    video: FreemocapVideoPaths

    @classmethod
    def from_recording_path(cls, path: str,
                            tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE) -> 'FreemocapDataPaths':

        if not Path(path).exists():
            raise FileNotFoundError(f"Path {path} does not exist")

        replacements: Dict[str, Union[str, TrackerSourceType]] = {
            PathPlaceholders.TRACKER_TYPE_PLACEHOLDER.value: tracker_type.value,
            PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value: path,
        }

        def replace_placeholders(file_template: str,
                                 right_left: Optional[RightLeft] = None) -> str:
            for key, value in replacements.items():
                file_template = file_template.replace(key, value)
            if right_left:
                file_template = file_template.replace(PathPlaceholders.RIGHT_LEFT_PLACEHOLDER.value, right_left.value)
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
    from skelly_blender.system.get_path_to_test_data import get_path_to_test_data

    paths = FreemocapDataPaths.from_recording_path(path=get_path_to_test_data(),
                                                   tracker_type=DEFAULT_TRACKER_TYPE)
    pprint(paths)
