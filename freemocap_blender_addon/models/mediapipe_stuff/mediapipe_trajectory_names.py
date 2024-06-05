from copy import copy
from dataclasses import dataclass

from freemocap_blender_addon.freemocap_data.data_paths.default_path_enums import RightLeft
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass

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


