from freemocap_blender_addon.models.skeleton_model.hands.right_hand_keypoints import RightHandKeypoints
from freemocap_blender_addon.models.skeleton_model.body.c_linkages import LinkageABC
from freemocap_blender_addon.models.skeleton_model.hands.b_rigid_bodies.right_hand_rigid_bodies import RightThumbMetacarpalRigidBodyABC, \
    RightThumbProximalPhalanxRigidBodyABC, RightThumbDistalPhalanxRigidBodyABC, RightIndexFingerMetacarpalRigidBodyABC, \
    RightIndexFingerProximalPhalanxRigidBodyABC, RightIndexFingerMiddlePhalanxRigidBodyABC, \
    RightIndexFingerDistalPhalanxRigidBodyABC, RightMiddleFingerMetacarpalRigidBodyABC, \
    RightMiddleFingerProximalPhalanxRigidBodyABC, RightMiddleFingerMiddlePhalanxRigidBodyABC, \
    RightMiddleFingerDistalPhalanxRigidBodyABC, RightRingFingerMetacarpalRigidBodyABC, \
    RightRingFingerProximalPhalanxRigidBodyABC, RightRingFingerMiddlePhalanxRigidBodyABC, \
    RightRingFingerDistalPhalanxRigidBodyABC, RightPinkyFingerMetacarpalRigidBodyABC, \
    RightPinkyFingerProximalPhalanxRigidBodyABC, RightPinkyFingerMiddlePhalanxRigidBodyABC, \
    RightPinkyFingerDistalPhalanxRigidBodyABC

# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg


# Thumb
class RightThumbKnuckleLinkage(LinkageABC):
    bodies = [RightThumbMetacarpalRigidBodyABC, RightThumbProximalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value

class RightThumbJointLinkage(LinkageABC):
    bodies = [RightThumbProximalPhalanxRigidBodyABC, RightThumbDistalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


# Index
class RightIndexFingerKnuckleLinkage(LinkageABC):
    bodies = [RightIndexFingerMetacarpalRigidBodyABC, RightIndexFingerProximalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value

class RightIndexFingerProximalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerProximalPhalanxRigidBodyABC, RightIndexFingerMiddlePhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightIndexFingerDistalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerMiddlePhalanxRigidBodyABC, RightIndexFingerDistalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

# Middle
class RightMiddleFingerKnuckleLinkage(LinkageABC):
    bodies = [RightMiddleFingerMetacarpalRigidBodyABC, RightMiddleFingerProximalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value

class RightMiddleFingerProximalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerProximalPhalanxRigidBodyABC, RightMiddleFingerMiddlePhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightMiddleFingerDistalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerMiddlePhalanxRigidBodyABC, RightMiddleFingerDistalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value

# Ring
class RightRingFingerKnuckleLinkage(LinkageABC):
    bodies = [RightRingFingerMetacarpalRigidBodyABC, RightRingFingerProximalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value

class RightRingFingerProximalJointLinkage(LinkageABC):
    bodies = [RightRingFingerProximalPhalanxRigidBodyABC, RightRingFingerMiddlePhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightRingFingerDistalJointLinkage(LinkageABC):
    bodies = [RightRingFingerMiddlePhalanxRigidBodyABC, RightRingFingerDistalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value

# Pinky
class RightPinkyFingerKnuckleLinkage(LinkageABC):
    bodies = [RightPinkyFingerMetacarpalRigidBodyABC, RightPinkyFingerProximalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value

class RightPinkyFingerProximalJointLinkage(LinkageABC):
    bodies = [RightPinkyFingerProximalPhalanxRigidBodyABC, RightPinkyFingerMiddlePhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightPinkyFingerDistalJointLinkage(LinkageABC):
    bodies = [RightPinkyFingerMiddlePhalanxRigidBodyABC, RightPinkyFingerDistalPhalanxRigidBodyABC]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
