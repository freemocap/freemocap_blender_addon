from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import SimpleRigidBodyABC
from freemocap_blender_addon.models.skeleton.hands.right_hand_keypoints import RightHandKeypoints

# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg

#Thumb
class RightThumbRadioCarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value


class RightThumbMetacarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value
    child = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value


class RightThumbProximalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


class RightThumbDistalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_THUMB_TIP.value

# Index
class RightIndexFingerRadioCarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value


class RightIndexFingerMetacarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value


class RightIndexFingerProximalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightIndexFingerMiddlePhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightIndexFingerDistalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_TIP.value

#Middle
class RightMiddleFingerRadioCarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value


class RightMiddleFingerMetacarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value


class RightMiddleFingerProximalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightMiddleFingerMiddlePhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightMiddleFingerDistalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_TIP.value

# Ring
class RightRingFingerRadioCarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value


class RightRingFingerMetacarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value


class RightRingFingerProximalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightRingFingerMiddlePhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightRingFingerDistalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_TIP.value

# Pinky
class RightPinkyFingerRadioCarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_CARPO_META_CARPAL.value


class RightPinkyFingerMetacarpalRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value


class RightPinkyFingerProximalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightPinkyFingerMiddlePhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightPinkyFingerDistalPhalanxRigidBodyABC(SimpleRigidBodyABC):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_TIP.value
