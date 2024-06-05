from enum import Enum

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import KeypointMapping

_MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS = {
    "HEAD_CENTER": [],
    "NECK_CENTER": [],
    "CHEST_CENTER": [],
    "HIPS_CENTER": ["left_hip", "right_hip"],
    "RIGHT_MIDDLE_KNUCKLE": {"right_index": 0.66, "right_pinky": 0.33},
    "RIGHT_RING_KNUCKLE": {"right_index": 0.33, "right_pinky": 0.66},
    "RIGHT_PALM_CENTER": ["right_wrist", "right_index", "right_pinky"],
    "LEFT_MIDDLE_KNUCKLE": {"left_index": 0.66, "left_pinky": 0.33},
    "LEFT_RING_KNUCKLE": {"left_index": 0.33, "left_pinky": 0.66},
    "LEFT_PALM_CENTER": ["left_wrist", "left_index", "left_pinky"],
}


