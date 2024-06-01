from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigid_body_abc import Keypoints


# "axial" means like non-mirrored

class HeadKeypoints(Keypoints):
    NOSE = auto()
    EYE_INNER = auto()
    EYE_CENTER = auto()
    EYE_OUTER = auto()
    EAR_TRAGUS = auto()
    MOUTH_LEFT = auto()
    MOUTH_RIGHT = auto()
    HEAD_CENTER = auto()
    HEAD_TOP = auto()
    NECK_C1 = auto()


class TorsoKeypoints(Keypoints):
    NECK_C7 = auto()
    CHEST_CENTER = auto()  # Center of the chest volume
    HIPS_CENTER = auto()  # Center of the pelvis volume



