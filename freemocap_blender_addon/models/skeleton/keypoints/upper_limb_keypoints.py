from enum import auto

from freemocap_blender_addon.models.skeleton.keypoints_enum import Keypoints


class RightArmKeypoints(Keypoints):
    RIGHT_SHOULDER = auto()
    RIGHT_ELBOW = auto()
    RIGHT_WRIST = auto()
    RIGHT_MIDDLE_KNUCKLE = auto()

class RightPalmKeypoints(Keypoints):
    """
    A simplified hand model, like the one used in the Mediapipe body pose estimation model.
    See `FullyHandKeypointEnumABC` for a more detailed hand model.
    """
    RIGHT_WRIST = auto()
    RIGHT_PINKY_KNUCKLE = auto()
    RIGHT_INDEX_KNUCKLE = auto()


class LeftArmKeypoints(Keypoints):
    LEFT_SHOULDER = auto()
    LEFT_ELBOW = auto()
    LEFT_WRIST = auto()
    LEFT_MIDDLE_KNUCKLE = auto()

class LeftPalmKeypoints(Keypoints):
    """
    A simplified hand model, like the one used in the Mediapipe body pose estimation model.
    See `FullyHandKeypointEnumABC` for a more detailed hand model.
    """
    LEFT_WRIST = auto()
    LEFT_PINKY_KNUCKLE = auto()
    LEFT_INDEX_KNUCKLE = auto()


class RightIndexFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    RIGHT_WRIST = auto()
    RIGHT_INDEX_CARPO_META_CARPAL = auto()
    RIGHT_INDEX_META_CARPO_PHALANGEAL = auto()
    RIGHT_INDEX_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_INDEX_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_INDEX_TIP = auto()

class RightMiddleFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    RIGHT_WRIST = auto()
    RIGHT_MIDDLE_CARPO_META_CARPAL = auto()
    RIGHT_MIDDLE_META_CARPO_PHALANGEAL = auto()
    RIGHT_MIDDLE_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_MIDDLE_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_MIDDLE_TIP = auto()

class RightRingFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    RIGHT_WRIST = auto()
    RIGHT_RING_CARPO_META_CARPAL = auto()
    RIGHT_RING_META_CARPO_PHALANGEAL = auto()
    RIGHT_RING_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_RING_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_RING_TIP = auto()

class RightPinkyFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    RIGHT_WRIST = auto()
    RIGHT_PINKY_CARPO_META_CARPAL = auto()
    RIGHT_PINKY_META_CARPO_PHALANGEAL = auto()
    RIGHT_PINKY_PROXIMAL_INTER_PHALANGEAL = auto()
    RIGHT_PINKY_DISTAL_INTER_PHALANGEAL = auto()
    RIGHT_PINKY_TIP = auto()


class RightThumbKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    Right_WRIST = auto()
    RIGHT_BASAL_CARPO_METACARPAL = auto()
    RIGHT_META_CARPO_PHALANGEAL = auto()
    RIGHT_INTER_PHALANGEAL = auto()
    RIGHT_TIP = auto()

class LeftIndexFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    LEFT_WRIST = auto()
    LEFT_INDEX_CARPO_META_CARPAL = auto()
    LEFT_INDEX_META_CARPO_PHALANGEAL = auto()
    LEFT_INDEX_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_INDEX_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_INDEX_TIP = auto()

class LeftMiddleFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    LEFT_WRIST = auto()
    LEFT_MIDDLE_CARPO_META_CARPAL = auto()
    LEFT_MIDDLE_META_CARPO_PHALANGEAL = auto()
    LEFT_MIDDLE_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_MIDDLE_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_MIDDLE_TIP = auto()

class LeftRingFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    LEFT_WRIST = auto()
    LEFT_RING_CARPO_META_CARPAL = auto()
    LEFT_RING_META_CARPO_PHALANGEAL = auto()
    LEFT_RING_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_RING_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_RING_TIP = auto()

class LeftPinkyFingerKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    LEFT_WRIST = auto()
    LEFT_PINKY_CARPO_META_CARPAL = auto()
    LEFT_PINKY_META_CARPO_PHALANGEAL = auto()
    LEFT_PINKY_PROXIMAL_INTER_PHALANGEAL = auto()
    LEFT_PINKY_DISTAL_INTER_PHALANGEAL = auto()
    LEFT_PINKY_TIP = auto()


class LeftThumbKeypoints(Keypoints):
    # https://www.assh.org/handcare/safety/joints
    LEFT_WRIST = auto()
    LEFT_BASAL_CARPO_METACARPAL = auto()
    LEFT_META_CARPO_PHALANGEAL = auto()
    LEFT_INTER_PHALANGEAL = auto()
    LEFT_TIP = auto()
