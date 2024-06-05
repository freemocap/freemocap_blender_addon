from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import KeypointsEnum


# "axial" means like non-mirrored

class AxialBodyKeypoints(KeypointsEnum):
    # head
    SKULL_C1 = auto()
    SKULL_BREGMA = auto()  # tippy top of the head

    # face
    NOSE = auto()

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
    NECK_C1 = auto()
    NECK_C7 = auto()

    # chest
    CHEST_T1_CENTER = auto()  # Center of the chest volume

    # root
    PELVIS_SACRUM = auto()  # Center of the pelvis volume
