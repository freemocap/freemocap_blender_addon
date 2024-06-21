from freemocap_blender_addon.models.skeleton_model.hands.right_hand_keypoints import RightHandKeypoints

from skelly_blender.core.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC


# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg

# Thumb
class RightThumbRadioCarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value


class RightThumbMetacarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value
    child = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value


class RightThumbProximalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


class RightThumbDistalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_THUMB_TIP.value


# Index
class RightIndexFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value


class RightIndexFingerMetacarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value


class RightIndexFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightIndexFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightIndexFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_INDEX_FINGER_TIP.value


# Middle
class RightMiddleFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value


class RightMiddleFingerMetacarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value


class RightMiddleFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightMiddleFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightMiddleFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_MIDDLE_FINGER_TIP.value


# Ring
class RightRingFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value


class RightRingFingerMetacarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value


class RightRingFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightRingFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightRingFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_RING_FINGER_TIP.value


# Pinky
class RightPinkyFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_CARPO_META_CARPAL.value


class RightPinkyFingerMetacarpalSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_RADIO_CARPAL
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value


class RightPinkyFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightPinkyFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightPinkyFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    parent = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightHandKeypoints.RIGHT_PINKY_FINGER_TIP.value
