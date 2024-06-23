from freemocap_blender_addon.models.skeleton_model.hands.right_hand_keypoints import RightHandKeypoints

from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC


# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg

# Thumb
class RightThumbRadioCarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value


class RightThumbMetacarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_THUMB_BASAL_CARPO_METACARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value


class RightThumbProximalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


class RightThumbDistalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_THUMB_TIP.value


# Index
class RightIndexFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value


class RightIndexFingerMetacarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_INDEX_FINGER_CARPO_META_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value


class RightIndexFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightIndexFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightIndexFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_INDEX_FINGER_TIP.value


# Middle
class RightMiddleFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value


class RightMiddleFingerMetacarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_MIDDLE_FINGER_CARPO_META_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value


class RightMiddleFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightMiddleFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightMiddleFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_MIDDLE_FINGER_TIP.value


# Ring
class RightRingFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value


class RightRingFingerMetacarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RING_FINGER_CARPO_META_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value


class RightRingFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightRingFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightRingFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_RING_FINGER_TIP.value


# Pinky
class RightPinkyFingerRadioCarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RADIO_CARPAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_PINKY_FINGER_CARPO_META_CARPAL.value


class RightPinkyFingerMetacarpalSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_RADIO_CARPAL
    z_axis_reference = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value


class RightPinkyFingerProximalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightPinkyFingerMiddlePhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightPinkyFingerDistalPhalanxSegmentABC(SimpleSegmentABC):
    origin = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
    z_axis_reference = RightHandKeypoints.RIGHT_PINKY_FINGER_TIP.value
