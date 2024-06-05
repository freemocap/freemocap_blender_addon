from enum import auto

from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import KeypointsEnum


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
    RIGHT_HALLUX_TIP = auto() #hallux is the big toe

