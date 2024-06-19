from enum import Enum


class TrackerSourceType(str, Enum):
    GENERIC = "generic"
    MEDIAPIPE = "mediapipe"
    OPENPOSE = "openpose"


DEFAULT_TRACKER_TYPE = TrackerSourceType.MEDIAPIPE
