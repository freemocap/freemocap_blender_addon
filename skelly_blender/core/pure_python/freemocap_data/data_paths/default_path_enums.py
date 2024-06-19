from enum import Enum

from skelly_blender.core.blender_stuff.blenderizable_enum import BlenderizableEnum


class PathPlaceholders(Enum):
    TRACKER_TYPE_PLACEHOLDER = "TRACKER_TYPE_PLACEHOLDER"
    RIGHT_LEFT_PLACEHOLDER = "RIGHT_LEFT_PLACEHOLDER"
    RECORDING_PATH_PLACEHOLDER = "RECORDING_PATH_PLACEHOLDER"


SKELETON_NPY_PARENT_DIRECTORY = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}/output_data"
CENTER_OF_MASS_NPY_PARENT_DIRECTORY = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}/output_data/center_of_mass"
VIDEO_PARENT_DIRECTORY = f"{PathPlaceholders.RECORDING_PATH_PLACEHOLDER.value}"


class RightLeft(BlenderizableEnum):
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
