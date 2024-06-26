from enum import Enum

from skelly_blender.core.pure_python.custom_types.base_enums import BlenderizableEnum


class PathPlaceholders(Enum):
    TRACKER_TYPE_PLACEHOLDER = "TRACKER_TYPE_PLACEHOLDER"
    RIGHT_LEFT_PLACEHOLDER = "RIGHT_LEFT_PLACEHOLDER"
    RECORDING_PATH_PLACEHOLDER = "RECORDING_PATH_PLACEHOLDER"


SKELETON_NPY_PARENT_DIRECTORY = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}/output_data"
CENTER_OF_MASS_NPY_PARENT_DIRECTORY = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}/output_data/center_of_mass"
VIDEO_PARENT_DIRECTORY = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}"


class RightLeftAxial(BlenderizableEnum):
    AXIAL = "axial"
    RIGHT = "right"
    LEFT = "left"


class SkeletonNpyFiles(Enum):
    BODY_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/{PathPlaceholders.TRACKER_TYPE_PLACEHOLDER.value}_body_3d_xyz.npy"
    HAND_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/{PathPlaceholders.TRACKER_TYPE_PLACEHOLDER.value}_{PathPlaceholders.RIGHT_LEFT_PLACEHOLDER.value}_hand_3d_xyz.npy"
    FACE_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/{PathPlaceholders.TRACKER_TYPE_PLACEHOLDER.value}_face_3d_xyz.npy"
    REPROJECTION_ERROR_NPY_FILE = f"{SKELETON_NPY_PARENT_DIRECTORY}/raw_data/{PathPlaceholders.TRACKER_TYPE_PLACEHOLDER.value}3dData_numFrames_numTrackedPoints_reprojectionError.npy"


class CenterOfMassNpyFiles(Enum):
    TOTAL_BODY_CENTER_OF_MASS_NPY = f"{CENTER_OF_MASS_NPY_PARENT_DIRECTORY}/total_body_center_of_mass_xyz.npy"
    SEGMENT_CENTER_OF_MASS_NPY = f"{CENTER_OF_MASS_NPY_PARENT_DIRECTORY}/segmentCOM_frame_joint_xyz.npy"


class VideoFolders(Enum):
    RAW = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}/synchronized_videos"
    ANNOTATED = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}/annotated_videos"


if __name__ == "__main__":
    print(f"SkeletonNpyFiles.BODY_NPY_FILE.value: `{SkeletonNpyFiles.BODY_NPY_FILE.value}`")
    print(f"SkeletonNpyFiles.HAND_NPY_FILE.value: `{SkeletonNpyFiles.HAND_NPY_FILE.value}`")
    print(f"SkeletonNpyFiles.FACE_NPY_FILE.value: `{SkeletonNpyFiles.FACE_NPY_FILE.value}`")
    print(f"SkeletonNpyFiles.REPROJECTION_ERROR_NPY_FILE.value: `{SkeletonNpyFiles.REPROJECTION_ERROR_NPY_FILE.value}`")
    print(
        f"\nCenterOfMassNpyFiles.TOTAL_BODY_CENTER_OF_MASS_NPY.value: `{CenterOfMassNpyFiles.TOTAL_BODY_CENTER_OF_MASS_NPY.value}`")
    print(
        f"CenterOfMassNpyFiles.SEGMENT_CENTER_OF_MASS_NPY.value: `{CenterOfMassNpyFiles.SEGMENT_CENTER_OF_MASS_NPY.value}`")
    print(f"\nVideoFolders.RAW.value: `{VideoFolders.RAW.value}`")
    print(f"VideoFolders.ANNOTATED.value: `{VideoFolders.ANNOTATED.value}`")
    print(f"\nRightLeftAxial.AXIAL: `{RightLeftAxial.AXIAL}`")
    print(f"RightLeftAxial.RIGHT: `{RightLeftAxial.RIGHT}`")
    print(f"RightLeftAxial.LEFT: `{RightLeftAxial.LEFT}`")

    print(f"RightLeftAxial.AXIAL.blenderize(): `{RightLeftAxial.AXIAL.blenderize()}`")
    print(f"RightLeftAxial.RIGHT.blenderize(): `{RightLeftAxial.RIGHT.blenderize()}`")
    print(f"RightLeftAxial.LEFT.blenderize(): `{RightLeftAxial.LEFT.blenderize()}`")
    print(f"\nPathPlaceholders.TRACKER_TYPE_PLACEHOLDER.value: `{PathPlaceholders.TRACKER_TYPE_PLACEHOLDER.value}`")
    print(f"PathPlaceholders.RIGHT_LEFT_PLACEHOLDER.value: `{PathPlaceholders.RIGHT_LEFT_PLACEHOLDER.value}`")
    print(f"PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value: `{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}`")
    print(f"\nSKELETON_NPY_PARENT_DIRECTORY: `{SKELETON_NPY_PARENT_DIRECTORY}`")
    print(f"\nCENTER_OF_MASS_NPY_PARENT_DIRECTORY: `{CENTER_OF_MASS_NPY_PARENT_DIRECTORY}`")
    print(f"\nVIDEO_PARENT_DIRECTORY: `{VIDEO_PARENT_DIRECTORY}`")
    print(f"\nSkeletonNpyFiles.BODY_NPY_FILE: `{SkeletonNpyFiles.BODY_NPY_FILE}`")
    print(f"SkeletonNpyFiles.HAND_NPY_FILE: `{SkeletonNpyFiles.HAND_NPY_FILE}`")
    print(f"SkeletonNpyFiles.FACE_NPY_FILE: `{SkeletonNpyFiles.FACE_NPY_FILE}`")
    print(f"SkeletonNpyFiles.REPROJECTION_ERROR_NPY_FILE: `{SkeletonNpyFiles.REPROJECTION_ERROR_NPY_FILE}`")
    print(f"\nCenterOfMassNpyFiles.TOTAL_BODY_CENTER_OF_MASS_NPY: `{CenterOfMassNpyFiles.TOTAL_BODY_CENTER_OF_MASS_NPY}`")
    print(f"CenterOfMassNpyFiles.SEGMENT_CENTER_OF_MASS_NPY: `{CenterOfMassNpyFiles.SEGMENT_CENTER_OF_MASS_NPY}`")
    print(f"\nVideoFolders.RAW: `{VideoFolders.RAW}`")
    print(f"VideoFolders.ANNOTATED: `{VideoFolders.ANNOTATED}`")
    print(f"\nPathPlaceholders.TRACKER_TYPE_PLACEHOLDER: `{PathPlaceholders.TRACKER_TYPE_PLACEHOLDER}`")
    print(f"PathPlaceholders.RIGHT_LEFT_PLACEHOLDER: `{PathPlaceholders.RIGHT_LEFT_PLACEHOLDER}`")
    print(f"PathPlaceholders.RECORDING_PATH_PLACEHOLDER: `{PathPlaceholders.RECORDING_PATH_PLACEHOLDER}`")
