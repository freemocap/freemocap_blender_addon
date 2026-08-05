"""Trajectory names for RTMPose whole-body output.

RTMPose is FreeMoCap's default detector, but the Blender addon previously only understood
MediaPipe, so the more accurate detector could not be exported at all.

The two skeletons are closer than they look. RTMPose's hand chain is positionally identical
to MediaPipe's, and its body already contains every joint `bone_definitions.py` references -
under the same names, except the toes. So rather than teaching the rig a second skeleton, the
RTMPose trajectories are labelled with the names the rig already expects:

    left_big_toe   -> left_foot_index
    right_big_toe  -> right_foot_index
    hand_root      -> wrist
    thumb1..4      -> thumb_cmc / thumb_mcp / thumb_ip / thumb_tip
    forefinger1..4 -> index_finger_mcp / pip / dip / tip
    ...

Everything downstream looks joints up by name, so no other change is needed.
"""
from dataclasses import dataclass, field
from typing import List

from freemocap_blender_addon.data_models.mediapipe_names.mediapipe_trajectory_names import (
    HumanTrajectoryNames,
)

NUMBER_OF_RTMPOSE_BODY_MARKERS = 27
NUMBER_OF_RTMPOSE_HAND_MARKERS = 21

# RTMPose body order, relabelled where the rig expects a different name.
# Index order must match the detector's output exactly - it is positional.
RTMPOSE_BODY_NAMES: List[str] = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_foot_index",   # rtmpose calls this left_big_toe
    "left_small_toe",
    "left_heel",
    "right_foot_index",  # rtmpose calls this right_big_toe
    "right_small_toe",
    "right_heel",
    # virtual markers, computed by freemocap
    "head_center",
    "neck_center",
    "trunk_center",
    "hips_center",
]

# Positionally identical to MediaPipe's hand chain, so the same labels apply.
RTMPOSE_HAND_NAMES: List[str] = [
    "wrist",             # hand_root
    "thumb_cmc",         # thumb1
    "thumb_mcp",         # thumb2
    "thumb_ip",          # thumb3
    "thumb_tip",         # thumb4
    "index_finger_mcp",  # forefinger1
    "index_finger_pip",  # forefinger2
    "index_finger_dip",  # forefinger3
    "index_finger_tip",  # forefinger4
    "middle_finger_mcp",
    "middle_finger_pip",
    "middle_finger_dip",
    "middle_finger_tip",
    "ring_finger_mcp",
    "ring_finger_pip",
    "ring_finger_dip",
    "ring_finger_tip",
    "pinky_mcp",         # pinky_finger1
    "pinky_pip",
    "pinky_dip",
    "pinky_tip",
]


@dataclass
class RtmposeTrajectoryNames(HumanTrajectoryNames):
    body: List[str] = field(default_factory=list)
    face: List[str] = field(default_factory=list)
    right_hand: List[str] = field(default_factory=list)
    left_hand: List[str] = field(default_factory=list)
    num_face_markers: int = 0

    def __post_init__(self):
        self.body = list(RTMPOSE_BODY_NAMES)
        self.right_hand = [f"right_hand_{name}" for name in RTMPOSE_HAND_NAMES]
        self.left_hand = [f"left_hand_{name}" for name in RTMPOSE_HAND_NAMES]
        # RTMPose ships several face models (68 / 136 points), so size to the loaded data
        # rather than asserting one count.
        self.face = [f"face_{index}" for index in range(self.num_face_markers)]
        self._validate_name_list_lengths()

    def _validate_name_list_lengths(self):
        if len(self.body) != NUMBER_OF_RTMPOSE_BODY_MARKERS:
            raise ValueError(
                f"Number of rtmpose body markers {len(self.body)} does not match expected "
                f"{NUMBER_OF_RTMPOSE_BODY_MARKERS}")
        for side, names in (("right", self.right_hand), ("left", self.left_hand)):
            if len(names) != NUMBER_OF_RTMPOSE_HAND_MARKERS:
                raise ValueError(
                    f"Number of rtmpose {side} hand markers {len(names)} does not match "
                    f"expected {NUMBER_OF_RTMPOSE_HAND_MARKERS}")
