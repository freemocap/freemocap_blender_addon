from enum import Enum

from freemocap_blender_addon.models.mediapipe_stuff.mediapipe_body_keypoints_enum import MediapipeBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import WeightedSumKeypointDefinition


class MediapipeVirtualMarkers(Enum):
    HEAD_CENTER: WeightedSumKeypoint(
        parent_keypoints=[MediapipeBodyKeypoints.LEFT_EAR.value,
                          MediapipeBodyKeypoints.RIGHT_EAR.value],
    )
    NECK_CENTER: WeightedSumKeypoint(
        parent_keypoints=[MediapipeBodyKeypoints.LEFT_SHOULDER.value,
                          MediapipeBodyKeypoints.RIGHT_SHOULDER.value],
    )
    CHEST_CENTER: WeightedSumKeypoint(
        parent_keypoints=[MediapipeBodyKeypoints.LEFT_HIP.value,
                          MediapipeBodyKeypoints.RIGHT_HIP.value,
                          MediapipeBodyKeypoints.LEFT_SHOULDER.value,
                          MediapipeBodyKeypoints.RIGHT_SHOULDER.value],
    )
    HIPS_CENTER: WeightedSumKeypoint(
        parent_keypoints=[MediapipeBodyKeypoints.LEFT_HIP.value,
                          MediapipeBodyKeypoints.RIGHT_HIP.value],
    )

    RIGHT_HAND_MIDDLE: WeightedSumKeypoint(
        parent_keypoints=[MediapipeBodyKeypoints.RIGHT_INDEX.value,
                          MediapipeBodyKeypoints.RIGHT_PINKY.value],
    )
    LEFT_HAND_MIDDLE: WeightedSumKeypoint(
        parent_keypoints=[MediapipeBodyKeypoints.LEFT_INDEX.value,
                          MediapipeBodyKeypoints.LEFT_PINKY.value],
    )


class MediapipeBodyAxialSkeletonKeypointMapping(Enum):
    # head
    SKULL_C1 = "head_center"
    SKULL_BREGMA = None

    # face
    NOSE = "nose"

    # right-face
    RIGHT_EYE_INNER = "right_eye_inner"
    RIGHT_EYE_CENTER = "right_eye"
    RIGHT_EYE_OUTER = "right_eye_outer"
    RIGHT_EAR_TRAGUS = "right_ear"
    RIGHT_MOUTH_LEFT = "mouth_left"
    RIGHT_MOUTH_RIGHT = "mouth_right"

    # left-face
    LEFT_EYE_INNER = "left_eye_inner"
    LEFT_EYE_CENTER = "left_eye"
    LEFT_EYE_OUTER = "left_eye_outer"
    LEFT_EAR_TRAGUS = "left_ear"
    LEFT_MOUTH_LEFT = "mouth_left"
    LEFT_MOUTH_RIGHT = "mouth_right"

    # neck
    NECK_C1 = "neck_center"

    # chest
    CHEST_T1_CENTER = "trunk_center"

    # root
    PELVIS_SACRUM = "hips_center"
