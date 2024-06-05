from enum import Enum
from typing import List


class TrackerSourceType(str, Enum):
    MEDIAPIPE = "mediapipe"
    OPENPOSE = "openpose"


class DataTypes(str, Enum):
    SKELETON = "skeleton"
    CENTER_OF_MASS = "center_of_mass"


DEFAULT_TRACKER_TYPE = TrackerSourceType.MEDIAPIPE
TRACKER_TYPE_PLACEHOLDER = "TRACKER_TYPE_PLACEHOLDER"
RIGHT_LEFT_PLACEHOLDER = "RIGHT_LEFT_PLACEHOLDER"
RECORDING_PATH_PLACEHOLDER = "RECORDING_PATH_PLACEHOLDER"


class ComponentType(Enum):
    BODY = "body"
    FACE = "face"
    RIGHT_HAND = "right_hand"
    LEFT_HAND = "left_hand"

FRAME_TRAJECTORY_XYZ: List[str] = ["frame_number", "trajectory_index", "xyz"]
