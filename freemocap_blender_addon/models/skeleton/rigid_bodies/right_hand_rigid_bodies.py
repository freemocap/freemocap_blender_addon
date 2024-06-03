from freemocap_blender_addon.models.skeleton.abstract_base_classes import SimpleRigidBody
from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightHandKeypoints

# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg

#Thumb
class RightThumbRadioCarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value


class RightThumbMetacarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value
    child = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value


class RightThumbProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


class RightThumbDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_THUMB_TIP.value

# Index
class RightIndexFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value


class RightIndexFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value


class RightIndexFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightIndexFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightIndexFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_TIP.value

#Middle
class RightMiddleFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value


class RightMiddleFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value


class RightMiddleFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightMiddleFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightMiddleFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_TIP.value

# Ring
class RightRingFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value


class RightRingFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value


class RightRingFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightRingFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightRingFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_TIP.value

# Pinky
class RightPinkyFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_CARPO_META_CARPAL.value


class RightPinkyFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value


class RightPinkyFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightPinkyFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightPinkyFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_TIP.value
