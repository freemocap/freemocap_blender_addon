from copy import copy
from dataclasses import dataclass
from typing import List, Optional

from freemocap_blender_addon.freemocap_data.freemocap_data_paths import RightLeft

MEDIAPIPE_HAND_NAMES = ["wrist",
                        "thumb_cmc",
                        "thumb_mcp",
                        "thumb_ip",
                        "thumb_tip",
                        "index_finger_mcp",
                        "index_finger_pip",
                        "index_finger_dip",
                        "index_finger_tip",
                        "middle_finger_mcp",
                        "middle_finger_pip",
                        "middle_finger_dip",
                        "middle_finger_tip",
                        "ring_finger_mcp",
                        "ring_finger_pip",
                        "ring_finger_dip",
                        "ring_finger_tip",
                        "pinky_mcp",
                        "pinky_pip",
                        "pinky_dip",
                        "pinky_tip",
                        ]

MEDIAPIPE_BODY_NAMES = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index",
]
MEDIAPIPE_NAMED_FACE_POINTS = ["face_right_eye",
                               "face_left_eye",
                               "nose_tip",
                               "mouth_center",
                               "right_ear_tragion",
                               "left_ear_tragion"]

NUMBER_OF_MEDIAPIPE_BODY_MARKERS = len(MEDIAPIPE_BODY_NAMES)
NUMBER_OF_MEDIAPIPE_HAND_MARKERS = len(MEDIAPIPE_HAND_NAMES)
NUMBER_OF_MEDIAPIPE_FACE_POINTS = 478

MEDIAPIPE_GENERIC_FACE_POINTS = [f"face_{i:03}" for i in range(NUMBER_OF_MEDIAPIPE_FACE_POINTS)]

MEDIAPIPE_FACE_NAMES = copy(MEDIAPIPE_GENERIC_FACE_POINTS)
MEDIAPIPE_FACE_NAMES[:len(MEDIAPIPE_NAMED_FACE_POINTS)] = MEDIAPIPE_NAMED_FACE_POINTS


@dataclass
class HandsTrajectoryNames:
    right: Optional[List[str]]
    left: Optional[List[str]]


@dataclass
class HumanTrajectoryNames:
    body: Optional[List[str]]
    face: Optional[List[str]]
    hands: Optional[HandsTrajectoryNames]


@dataclass
class MediapipeTrajectoryNames(HumanTrajectoryNames):
    def __init__(self):
        self.body = MEDIAPIPE_BODY_NAMES
        self.hands = HandsTrajectoryNames(right=[f"{RightLeft.RIGHT.value}_{name}" for name in MEDIAPIPE_HAND_NAMES],
                                          left=[f"{RightLeft.LEFT.value}_{name}" for name in MEDIAPIPE_HAND_NAMES])
        self.face = MEDIAPIPE_FACE_NAMES
        self._validate_name_list_lengths()

    def _validate_name_list_lengths(self):
        if not len(self.body) == NUMBER_OF_MEDIAPIPE_BODY_MARKERS:
            raise ValueError(
                f"Number of mediapipe body markers {len(self.body)} does not match expected {NUMBER_OF_MEDIAPIPE_BODY_MARKERS}")
        if not len(self.face) == NUMBER_OF_MEDIAPIPE_FACE_POINTS:
            raise ValueError(
                f"Number of mediapipe face markers {len(self.face)} does not match expected {NUMBER_OF_MEDIAPIPE_FACE_POINTS}")
        if not len(self.hands.right) == NUMBER_OF_MEDIAPIPE_HAND_MARKERS:
            raise ValueError(
                f"Number of mediapipe right hand markers {len(self.hands.right)} does not match expected {NUMBER_OF_MEDIAPIPE_HAND_MARKERS}")
        if not len(self.hands.left) == NUMBER_OF_MEDIAPIPE_HAND_MARKERS:
            raise ValueError(
                f"Number of mediapipe left hand markers {len(self.hands.left)} does not match expected {NUMBER_OF_MEDIAPIPE_HAND_MARKERS}")


MEDIAPIPE_TRAJECTORY_NAMES = MediapipeTrajectoryNames()
