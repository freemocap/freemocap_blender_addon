from enum import auto

from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import Keypoints


class RightSideKeypoints(Keypoints):
    RIGHT_HIP = auto()
    RIGHT_KNEE = auto()
    RIGHT_ANKLE = auto()
    RIGHT_HEEL = auto()
    RIGHT_HALLUX_TIP = auto() #hallux is the big toe

    # arm
    RIGHT_CLAVICLE = auto()
    RIGHT_SHOULDER = auto()
    RIGHT_ELBOW = auto()
    RIGHT_WRIST = auto()

    # hand
    # https://www.assh.org/handcare/safety/joints
    # https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg
    # thumb
    RIGHT_THUMB_BASAL_CARPO_METACARPAL = auto() # wrist connection
    RIGHT_THUMB_META_CARPO_PHALANGEAL = auto() # thumb knuckle
    RIGHT_THUMB_INTER_PHALANGEAL = auto()
    RIGHT_THUMB_TIP = auto()

    # index
    RIGHT_INDEX_FINGER_CARPO_META_CARPAL = auto() # wrist connection
    RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL = auto() # knuckle
    RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_INDEX_FINGER_TIP = auto()

    # middle
    RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL = auto()
    RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL = auto()
    RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_MIDDLE_FINGER_TIP = auto()

    # ring
    RIGHT_RING_FINGER_CARPO_META_CARPAL = auto()
    RIGHT_RING_FINGER_META_CARPO_PHALANGEAL = auto()
    RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_RING_FINGER_TIP = auto()

    # pinky
    RIGHT_PINKY_FINGER_CARPO_META_CARPAL = auto()
    RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL = auto()
    RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_PINKY_FINGER_TIP = auto()

