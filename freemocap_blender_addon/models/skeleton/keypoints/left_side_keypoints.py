from enum import auto

from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import Keypoints


class LeftBodyKeypoints(Keypoints):
    LEFT_HIP = auto()
    LEFT_KNEE = auto()
    LEFT_ANKLE = auto()
    LEFT_HEEL = auto()
    LEFT_HALLUX_TIP = auto() #hallux is the big toe

    # arm
    LEFT_CLAVICLE = auto()
    LEFT_SHOULDER = auto()
    LEFT_ELBOW = auto()
    LEFT_WRIST = auto()



class LeftHandKeypoints(Keypoints):
    # hand
    # https://www.assh.org/handcare/safety/joints
    # https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg
    # wrist
    LEFT_RADIO_CARPAL = auto()
    LEFT_MID_CARPAL = auto()

    # thumb
    LEFT_THUMB_BASAL_CARPO_METACARPAL = auto() # wrist connection
    LEFT_THUMB_META_CARPO_PHALANGEAL = auto() # thumb knuckle
    LEFT_THUMB_INTER_PHALANGEAL = auto()
    LEFT_THUMB_TIP = auto()

    # index
    LEFT_INDEX_FINGER_CARPO_META_CARPAL = auto() # wrist connection
    LEFT_INDEX_FINGER_META_CARPO_PHALANGEAL = auto() # knuckle
    LEFT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_INDEX_FINGER_TIP = auto()

    # middle
    LEFT_MIDDLE_FINGER_CARPO_META_CARPAL = auto()
    LEFT_MIDDLE_FINGER_META_CARPO_PHALANGEAL = auto()
    LEFT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_MIDDLE_FINGER_TIP = auto()

    # ring
    LEFT_RING_FINGER_CARPO_META_CARPAL = auto()
    LEFT_RING_FINGER_META_CARPO_PHALANGEAL = auto()
    LEFT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_RING_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_RING_FINGER_TIP = auto()

    # pinky
    LEFT_PINKY_FINGER_CARPO_META_CARPAL = auto()
    LEFT_PINKY_FINGER_META_CARPO_PHALANGEAL = auto()
    LEFT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_PINKY_FINGER_TIP = auto()

