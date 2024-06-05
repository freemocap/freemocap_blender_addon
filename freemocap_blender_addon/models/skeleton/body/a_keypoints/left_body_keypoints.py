from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import KeypointsEnum


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
    LEFT_HALLUX_TIP = auto() #hallux is the big toe

