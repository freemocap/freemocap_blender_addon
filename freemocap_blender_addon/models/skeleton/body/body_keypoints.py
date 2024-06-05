from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import KeypointsEnum


class AxialBodyKeypoints(KeypointsEnum):
    # head
    SKULL_CENTER_C1 = auto()
    SKULL__TOP_BREGMA = auto()  # tippy top of the head

    # face
    NOSE_TIP = auto()

    # right-face
    RIGHT_EYE_INNER = auto()
    RIGHT_EYE_CENTER = auto()
    RIGHT_EYE_OUTER = auto()
    RIGHT_EAR_TRAGUS = auto()
    RIGHT_MOUTH = auto()

    # left-face
    LEFT_EYE_INNER = auto()
    LEFT_EYE_CENTER = auto()
    LEFT_EYE_OUTER = auto()
    LEFT_EAR_TRAGUS = auto()
    LEFT_MOUTH = auto()

    # neck
    NECK_TOP_C1 = auto()
    NECK_BASE_C7 = auto()

    # chest
    CHEST_CENTER_T1 = auto()  # Center of the chest volume

    # root
    PELVIS_SACRUM = auto()  # Center of the pelvis volume


class RightBodyKeypoints(KeypointsEnum):
    # arm
    RIGHT_CLAVICLE = auto()
    RIGHT_SHOULDER = auto()
    RIGHT_ELBOW = auto()
    RIGHT_WRIST = auto()

    # (mitten) hand
    RIGHT_INDEX_KNUCKLE = auto()
    RIGHT_PINKY_KNUCKLE = auto()
    RIGHT_THUMB_KNUCKLE = auto()

    # leg
    RIGHT_HIP = auto()
    RIGHT_KNEE = auto()
    RIGHT_ANKLE = auto()
    RIGHT_HEEL = auto()
    RIGHT_HALLUX_TIP = auto()  # hallux is the big toe


class LeftBodyKeypoints(KeypointsEnum):
    # arm
    LEFT_CLAVICLE = auto()
    LEFT_SHOULDER = auto()
    LEFT_ELBOW = auto()
    LEFT_WRIST = auto()

    # (mitten) hand
    LEFT_INDEX_KNUCKLE = auto()
    LEFT_PINKY_KNUCKLE = auto()
    LEFT_THUMB_KNUCKLE = auto()

    # leg
    LEFT_HIP = auto()
    LEFT_KNEE = auto()
    LEFT_ANKLE = auto()
    LEFT_HEEL = auto()
    LEFT_HALLUX_TIP = auto()  # hallux is the big toe
