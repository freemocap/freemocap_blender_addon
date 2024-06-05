from copy import copy

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import WeightedSumDefiniton

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

MEDIAPIPE_BODY_NAMES = ["nose",
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

NUMBER_OF_MEDIAPIPE_FACE_POINTS = 478

MEDIAPIPE_GENERIC_FACE_POINTS = [f"face_{i:03}" for i in range(NUMBER_OF_MEDIAPIPE_FACE_POINTS)]

MEDIAPIPE_FACE_NAMES = copy(MEDIAPIPE_GENERIC_FACE_POINTS)
MEDIAPIPE_FACE_NAMES[:len(MEDIAPIPE_NAMED_FACE_POINTS)] = MEDIAPIPE_NAMED_FACE_POINTS

MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS = [
    WeightedSumDefiniton(
        name="head_center",
        parent_keypoints=["left_ear", "right_ear"]),
    WeightedSumDefiniton(
        name="neck_center",
        parent_keypoints=["left_shoulder", "right_shoulder"]),

    WeightedSumDefiniton(
        name="chest_center",
        parent_keypoints=["left_hip",
                          "right_hip",
                          "left_shoulder",
                          "right_shoulder"],
    ),
    WeightedSumDefiniton(
        name="hips_center",
        parent_keypoints=["left_hip",
                          "right_hip"]
    ),

    WeightedSumDefiniton(
        name="right_hand_middle",
        parent_keypoints=["right_index",
                          "right_pinky"],
    ),
    WeightedSumDefiniton(
        name="left_hand_middle",
        parent_keypoints=["left_index",
                          "left_pinky"],
    )
]

for vm in MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS:
    if not all([kp in MEDIAPIPE_BODY_NAMES for kp in vm.parent_keypoints]):
        raise ValueError(f"Virtual trajectory {vm.name} has parent keypoints not in body names: {vm.parent_keypoints}")

