from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigid_body_abc import KeypointABC


class LegKeypoints(KeypointABC):
    HIP = auto()
    KNEE = auto()
    ANKLE = auto()


class FullFootKeypoints(KeypointABC):
    ANKLE = auto()
    HEEL = auto()
    HALLUX_BASE = auto()
    HALLUX_TIP = auto()
    PINKY_TOE_BASE = auto()
    PINKY_TOE_TIP = auto()


class SimpleFootKeypoints(KeypointABC):
    ANKLE = auto()
    HEEL = auto()
    HALLUX_TIP = auto()
