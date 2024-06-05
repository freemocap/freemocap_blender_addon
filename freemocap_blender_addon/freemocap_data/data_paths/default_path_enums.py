from enum import Enum

from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TRACKER_TYPE_PLACEHOLDER, \
    RIGHT_LEFT_PLACEHOLDER, RECORDING_PATH_PLACEHOLDER

SKELETON_NPY_PARENT_DIRECTORY = f"{RECORDING_PATH_PLACEHOLDER}/output_data"
CENTER_OF_MASS_NPY_PARENT_DIRECTORY = f"{RECORDING_PATH_PLACEHOLDER}/output_data/center_of_mass"
VIDEO_PARENT_DIRECTORY = f"{RECORDING_PATH_PLACEHOLDER}"

class RightLeft(str, Enum):
    RIGHT = "right"
    LEFT = "left"


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
