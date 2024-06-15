from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Union, Optional, Dict

from freemocap_blender_addon.freemocap_data.data_paths.default_path_enums import SkeletonNpyFiles, CenterOfMassNpyFiles, \
    VideoFolders, RightLeft
from freemocap_blender_addon.freemocap_data.data_paths.numpy_paths import HandsNpyPaths, SkeletonNpyPaths, \
    CenterOfMassNpyPaths
from freemocap_blender_addon.freemocap_data.data_paths.video_paths import VideoFolder, FreemocapVideoPaths
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, DEFAULT_TRACKER_TYPE, \
    TRACKER_TYPE_PLACEHOLDER, RIGHT_LEFT_PLACEHOLDER, RECORDING_PATH_PLACEHOLDER


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
            TRACKER_TYPE_PLACEHOLDER: tracker_type.value,
            RECORDING_PATH_PLACEHOLDER: path,
        }

        def replace_placeholders(file_template: str,
                                 right_left: Optional[RightLeft] = None) -> str:
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
    from freemocap_blender_addon.utilities.get_path_to_test_data import get_path_to_test_data

    paths = FreemocapDataPaths.from_recording_path(path=get_path_to_test_data(),
                                                   tracker_type=DEFAULT_TRACKER_TYPE)
    pprint(paths)
