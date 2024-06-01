from enum import auto

from freemocap_blender_addon.models.skeleton.keypoints.keypoints_enum import Keypoints


class RightSideKeypoints(Keypoints):
    RIGHT_HIP = auto()
    RIGHT_KNEE = auto()
    RIGHT_ANKLE = auto()
    RIGHT_HEEL = auto()
    RIGHT_HALLUX_TIP = auto() #hallux is the big toe

    # arm
    RIGHT_SHOULDER = auto()
    RIGHT_ELBOW = auto()
    RIGHT_WRIST = auto()

    # hand
    # https://www.assh.org/handcare/safety/joints

    # index
    RIGHT_INDEX_CARPO_META_CARPAL = auto() # wrist connection
    RIGHT_INDEX_META_CARPO_PHALANGEAL = auto() # knuckle
    RIGHT_INDEX_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_INDEX_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_INDEX_TIP = auto()

    # middle
    RIGHT_MIDDLE_CARPO_META_CARPAL = auto()
    RIGHT_MIDDLE_META_CARPO_PHALANGEAL = auto()
    RIGHT_MIDDLE_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_MIDDLE_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_MIDDLE_TIP = auto()

    # ring
    RIGHT_RING_CARPO_META_CARPAL = auto()
    RIGHT_RING_META_CARPO_PHALANGEAL = auto()
    RIGHT_RING_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_RING_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_RING_TIP = auto()

    # pinky
    RIGHT_PINKY_CARPO_META_CARPAL = auto()
    RIGHT_PINKY_META_CARPO_PHALANGEAL = auto()
    RIGHT_PINKY_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_PINKY_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_PINKY_TIP = auto()

    # thumb
    RIGHT_THUMB_BASAL_CARPO_METACARPAL = auto() # wrist connection
    RIGHT_THUMB_META_CARPO_PHALANGEAL = auto() # thumb knuckle
    RIGHT_THUMB_INTER_PHALANGEAL = auto()
    RIGHT_THUMB_TIP = auto()