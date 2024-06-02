from enum import auto

from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import Keypoints


class LeftSideKeypoints(Keypoints):
    LEFT_HIP = auto()
    LEFT_KNEE = auto()
    LEFT_ANKLE = auto()
    LEFT_HEEL = auto()
    LEFT_HALLUX_TIP = auto()  # hallux is the big toe

    # arm
    LEFT_SHOULDER = auto()
    LEFT_ELBOW = auto()
    LEFT_WRIST = auto()

    # hand
    # https://www.assh.org/handcare/safety/joints

    # index
    LEFT_INDEX_CARPO_META_CARPAL = auto()  # wrist connection
    LEFT_INDEX_META_CARPO_PHALANGEAL = auto()  # knuckle
    LEFT_INDEX_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_INDEX_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_INDEX_TIP = auto()

    # middle
    LEFT_MIDDLE_CARPO_META_CARPAL = auto()
    LEFT_MIDDLE_META_CARPO_PHALANGEAL = auto()
    LEFT_MIDDLE_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_MIDDLE_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_MIDDLE_TIP = auto()

    # ring
    LEFT_RING_CARPO_META_CARPAL = auto()
    LEFT_RING_META_CARPO_PHALANGEAL = auto()
    LEFT_RING_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_RING_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_RING_TIP = auto()

    # pinky
    LEFT_PINKY_CARPO_META_CARPAL = auto()
    LEFT_PINKY_META_CARPO_PHALANGEAL = auto()
    LEFT_PINKY_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_PINKY_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_PINKY_TIP = auto()

    # thumb
    LEFT_THUMB_BASAL_CARPO_METACARPAL = auto()  # wrist connection
    LEFT_THUMB_META_CARPO_PHALANGEAL = auto()  # thumb knuckle
    LEFT_THUMB_INTER_PHALANGEAL = auto()
    LEFT_THUMB_TIP = auto()
