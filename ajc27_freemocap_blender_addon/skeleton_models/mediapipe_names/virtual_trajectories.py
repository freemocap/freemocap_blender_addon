from copy import deepcopy

_MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS = {
    "head_center": {
        "marker_names": ["left_ear", "right_ear"],
        "marker_weights": [0.5, 0.5],
    },
    "neck_center": {
        "marker_names": ["left_shoulder", "right_shoulder"],
        "marker_weights": [0.5, 0.5],
    },
    "trunk_center": {
        "marker_names": ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
        "marker_weights": [0.25, 0.25, 0.25, 0.25],
    },
    "hips_center": {
        "marker_names": ["left_hip", "right_hip"],
        "marker_weights": [0.5, 0.5],
    },
    "right_hand_middle": {
        "marker_names": ["right_index", "right_pinky"],
        "marker_weights": [0.5, 0.5],
    },
    "left_hand_middle": {
        "marker_names": ["left_index", "left_pinky"],
        "marker_weights": [0.5, 0.5],
    },
}


def get_media_pipe_virtual_trajectory_definition():
    """
    Returns a deep copy of the MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS dictionary to prevent accidental modification.
    """
    return deepcopy(_MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS)
