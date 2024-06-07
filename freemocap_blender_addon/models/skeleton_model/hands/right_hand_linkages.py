from freemocap_blender_addon.models.skeleton_model.hands.right_hand_keypoints import RightHandKeypoints
from freemocap_blender_addon.models.skeleton_model.body.linkages import LinkageABC
from freemocap_blender_addon.models.skeleton_model.hands.b_rigid_bodies.right_hand_rigid_bodies import RightThumbMetacarpalSegmentABC, \
    RightThumbProximalPhalanxSegmentABC, RightThumbDistalPhalanxSegmentABC, RightIndexFingerMetacarpalSegmentABC, \
    RightIndexFingerProximalPhalanxSegmentABC, RightIndexFingerMiddlePhalanxSegmentABC, \
    RightIndexFingerDistalPhalanxSegmentABC, RightMiddleFingerMetacarpalSegmentABC, \
    RightMiddleFingerProximalPhalanxSegmentABC, RightMiddleFingerMiddlePhalanxSegmentABC, \
    RightMiddleFingerDistalPhalanxSegmentABC, RightRingFingerMetacarpalSegmentABC, \
    RightRingFingerProximalPhalanxSegmentABC, RightRingFingerMiddlePhalanxSegmentABC, \
    RightRingFingerDistalPhalanxSegmentABC, RightPinkyFingerMetacarpalSegmentABC, \
    RightPinkyFingerProximalPhalanxSegmentABC, RightPinkyFingerMiddlePhalanxSegmentABC, \
    RightPinkyFingerDistalPhalanxSegmentABC

# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg


# Thumb
class RightThumbKnuckleLinkage(LinkageABC):
    bodies = [RightThumbMetacarpalSegmentABC, RightThumbProximalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value

class RightThumbJointLinkage(LinkageABC):
    bodies = [RightThumbProximalPhalanxSegmentABC, RightThumbDistalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


# Index
class RightIndexFingerKnuckleLinkage(LinkageABC):
    bodies = [RightIndexFingerMetacarpalSegmentABC, RightIndexFingerProximalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value

class RightIndexFingerProximalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerProximalPhalanxSegmentABC, RightIndexFingerMiddlePhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightIndexFingerDistalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerMiddlePhalanxSegmentABC, RightIndexFingerDistalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

# Middle
class RightMiddleFingerKnuckleLinkage(LinkageABC):
    bodies = [RightMiddleFingerMetacarpalSegmentABC, RightMiddleFingerProximalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value

class RightMiddleFingerProximalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerProximalPhalanxSegmentABC, RightMiddleFingerMiddlePhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightMiddleFingerDistalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerMiddlePhalanxSegmentABC, RightMiddleFingerDistalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value

# Ring
class RightRingFingerKnuckleLinkage(LinkageABC):
    bodies = [RightRingFingerMetacarpalSegmentABC, RightRingFingerProximalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value

class RightRingFingerProximalJointLinkage(LinkageABC):
    bodies = [RightRingFingerProximalPhalanxSegmentABC, RightRingFingerMiddlePhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightRingFingerDistalJointLinkage(LinkageABC):
    bodies = [RightRingFingerMiddlePhalanxSegmentABC, RightRingFingerDistalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value

# Pinky
class RightPinkyFingerKnuckleLinkage(LinkageABC):
    bodies = [RightPinkyFingerMetacarpalSegmentABC, RightPinkyFingerProximalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value

class RightPinkyFingerProximalJointLinkage(LinkageABC):
    bodies = [RightPinkyFingerProximalPhalanxSegmentABC, RightPinkyFingerMiddlePhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightPinkyFingerDistalJointLinkage(LinkageABC):
    bodies = [RightPinkyFingerMiddlePhalanxSegmentABC, RightPinkyFingerDistalPhalanxSegmentABC]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
