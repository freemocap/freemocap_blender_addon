from freemocap_blender_addon.models.skeleton.keypoints.left_side_keypoints import LeftHandKeypoints
from freemocap_blender_addon.models.skeleton.rigid_bodies.abc_rigid_body import SimpleRigidBody


# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg

# Thumb
class LeftThumbRadioCarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RADIO_CARPAL.value
    child = LeftHandKeypoints.LEFT_THUMB_BASAL_CARPO_METACARPAL.value


class LeftThumbMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_THUMB_BASAL_CARPO_METACARPAL.value
    child = LeftHandKeypoints.LEFT_THUMB_META_CARPO_PHALANGEAL.value


class LeftThumbProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_THUMB_META_CARPO_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_THUMB_INTER_PHALANGEAL.value


class LeftThumbDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_THUMB_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_THUMB_TIP.value


# Index
class LeftIndexFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RADIO_CARPAL.value
    child = LeftHandKeypoints.LEFT_INDEX_FINGER_CARPO_META_CARPAL.value


class LeftIndexFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_INDEX_FINGER_CARPO_META_CARPAL.value
    child = LeftHandKeypoints.LEFT_INDEX_FINGER_META_CARPO_PHALANGEAL.value


class LeftIndexFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_INDEX_FINGER_META_CARPO_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class LeftIndexFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value


class LeftIndexFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_INDEX_FINGER_TIP.value


# Middle
class LeftMiddleFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RADIO_CARPAL.value
    child = LeftHandKeypoints.LEFT_MIDDLE_FINGER_CARPO_META_CARPAL.value


class LeftMiddleFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_MIDDLE_FINGER_CARPO_META_CARPAL.value
    child = LeftHandKeypoints.LEFT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value


class LeftMiddleFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class LeftMiddleFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value


class LeftMiddleFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_MIDDLE_FINGER_TIP.value


# Ring
class LeftRingFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RADIO_CARPAL.value
    child = LeftHandKeypoints.LEFT_RING_FINGER_CARPO_META_CARPAL.value


class LeftRingFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RING_FINGER_CARPO_META_CARPAL.value
    child = LeftHandKeypoints.LEFT_RING_FINGER_META_CARPO_PHALANGEAL.value


class LeftRingFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RING_FINGER_META_CARPO_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class LeftRingFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value


class LeftRingFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_RING_FINGER_TIP.value


# Pinky
class LeftPinkyFingerRadioCarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RADIO_CARPAL.value
    child = LeftHandKeypoints.LEFT_PINKY_FINGER_CARPO_META_CARPAL.value


class LeftPinkyFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_RADIO_CARPAL
    child = LeftHandKeypoints.LEFT_PINKY_FINGER_META_CARPO_PHALANGEAL.value


class LeftPinkyFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class LeftPinkyFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value


class LeftPinkyFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftHandKeypoints.LEFT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = LeftHandKeypoints.LEFT_PINKY_FINGER_TIP.value
