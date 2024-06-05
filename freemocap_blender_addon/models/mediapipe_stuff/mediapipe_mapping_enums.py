from enum import Enum


class AxialSkeletonFromMediapipe(Enum):
    # head
    SKULL_C1 = "head_center"

    # face
    NOSE = "nose"

    # right-face
    RIGHT_EYE_INNER = "right_eye_inner"
    RIGHT_EYE_CENTER = "right_eye"
    RIGHT_EYE_OUTER = "right_eye_outer"
    RIGHT_EAR_TRAGUS = "right_ear"
    RIGHT_MOUTH = "mouth_right"

    # left-face
    LEFT_EYE_INNER = "left_eye_inner"
    LEFT_EYE_CENTER = "left_eye"
    LEFT_EYE_OUTER = "left_eye_outer"
    LEFT_EAR_TRAGUS = "left_ear"
    LEFT_MOUTH = "mouth_left"

    # neck
    NECK_C1 = "neck_center"

    # chest
    CHEST_T1_CENTER = "trunk_center"

    # root
    PELVIS_SACRUM = "hips_center"
