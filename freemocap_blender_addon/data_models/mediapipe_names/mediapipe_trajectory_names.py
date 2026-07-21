from dataclasses import dataclass, field
from typing import List

NUMBER_OF_MEDIAPIPE_BODY_MARKERS = 37
NUMBER_OF_MEDIAPIPE_HAND_MARKERS = 21
# MediaPipe ships multiple face models; we accept any of them and size the name
# list to whatever the loaded data actually contains.
NUMBER_OF_MEDIAPIPE_FACE_MARKERS_TESSELLATED = 478
NUMBER_OF_MEDIAPIPE_FACE_MARKERS_CONTOUR = 136
# Back-compat alias; treated as the default when no marker count is supplied.
NUMBER_OF_MEDIAPIPE_FACE_MARKERS = NUMBER_OF_MEDIAPIPE_FACE_MARKERS_TESSELLATED


@dataclass
class HumanTrajectoryNames:
    body: List[str] = field(default_factory=list)
    face: List[str] = field(default_factory=list)
    right_hand: List[str] = field(default_factory=list)
    left_hand: List[str] = field(default_factory=list)


@dataclass
class MediapipeTrajectoryNames(HumanTrajectoryNames):
    body: List[str] = field(default_factory=list)
    face: List[str] = field(default_factory=list)
    right_hand: List[str] = field(default_factory=list)
    left_hand: List[str] = field(default_factory=list)
    num_face_markers: int = NUMBER_OF_MEDIAPIPE_FACE_MARKERS

    def __post_init__(self):
        self.body = [
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
            #virtual markers
            "head_center",
            "neck_center",
            "trunk_center",
            "hips_center"
        ]
        hand_names = ["wrist",
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
        self.right_hand = [f"right_hand_{name}" for name in hand_names]
        self.left_hand = [f"left_hand_{name}" for name in hand_names]

        # NOTE - these are the names of the first couple face markers, there are like 400 more points in that mesh that will be given names like `face_012` etc
        face_named_points = ["face_right_eye",
                             "face_left_eye",
                             "nose_tip",
                             "mouth_center",
                             "right_ear_tragion",
                             "left_ear_tragion"]
        mediapipe_face_names = []
        for index in range(self.num_face_markers):
            if index < len(face_named_points):
                mediapipe_face_names.append(face_named_points[index])
            else:
                mediapipe_face_names.append(f"face_{index}")
        self.face = mediapipe_face_names

        self._validate_name_list_lengths()

    def _validate_name_list_lengths(self):
        if not len(self.body) == NUMBER_OF_MEDIAPIPE_BODY_MARKERS:
            raise ValueError(
                f"Number of mediapipe body markers {len(self.body)} does not match expected {NUMBER_OF_MEDIAPIPE_BODY_MARKERS}")
        # Face length is intentionally not strictly validated — MediaPipe has
        # multiple face models (tessellated 478, contour 136, etc.) and we
        # size the name list dynamically from the incoming data.
        if self.num_face_markers not in (
            NUMBER_OF_MEDIAPIPE_FACE_MARKERS_TESSELLATED,
            NUMBER_OF_MEDIAPIPE_FACE_MARKERS_CONTOUR,
        ):
            print(
                f"WARNING - unexpected number of mediapipe face markers: {self.num_face_markers} "
                f"(known values: {NUMBER_OF_MEDIAPIPE_FACE_MARKERS_TESSELLATED} tessellated, "
                f"{NUMBER_OF_MEDIAPIPE_FACE_MARKERS_CONTOUR} contour) — proceeding anyway."
            )
        if not len(self.right_hand) == NUMBER_OF_MEDIAPIPE_HAND_MARKERS:
            raise ValueError(
                f"Number of mediapipe right hand markers {len(self.right_hand)} does not match expected {NUMBER_OF_MEDIAPIPE_HAND_MARKERS}")
        if not len(self.left_hand) == NUMBER_OF_MEDIAPIPE_HAND_MARKERS:
            raise ValueError(
                f"Number of mediapipe left hand markers {len(self.left_hand)} does not match expected {NUMBER_OF_MEDIAPIPE_HAND_MARKERS}")
