from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigid_body_abc import KeypointABC


class ArmKeypoints(KeypointABC):
    SHOULDER = auto()
    ELBOW = auto()
    WRIST = auto()
    MIDDLE_KNUCKLE = auto()


class MittenHandKeypoints(KeypointABC):
    """
    A simplified hand model, like the one used in the Mediapipe body pose estimation model.
    See `FullyHandKeypointEnumABC` for a more detailed hand model.
    """
    WRIST = auto()
    PINKY_KNUCKLE = auto()
    INDEX_KNUCKLE = auto()
    THUMB_KNUCKLE = auto()


class FingerKeypoints(KeypointABC):
    # https://www.assh.org/handcare/safety/joints
    WRIST = auto()
    CARPO_META_CARPAL = auto()
    META_CARPO_PHALANGEAL = auto()
    PROXIMAL_INTER_PHALANGEAL = auto()
    DISTAL_INTER_PHALANGEAL = auto()
    TIP = auto()


class ThumbKeypoints(KeypointABC):
    # https://www.assh.org/handcare/safety/joints
    WRIST = auto()
    BASAL_CARPO_METACARPAL = auto()
    META_CARPO_PHALANGEAL = auto()
    INTER_PHALANGEAL = auto()
    TIP = auto()
