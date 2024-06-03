from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightHandKeypoints
from freemocap_blender_addon.models.skeleton.linkages.abc_linkage import LinkageABC
from freemocap_blender_addon.models.skeleton.rigid_bodies.right_hand_rigid_bodies import RightThumbMetacarpalRigidBody, \
    RightThumbProximalPhalanxRigidBody, RightThumbDistalPhalanxRigidBody, RightIndexFingerMetacarpalRigidBody, \
    RightIndexFingerProximalPhalanxRigidBody, RightIndexFingerMiddlePhalanxRigidBody, \
    RightIndexFingerDistalPhalanxRigidBody, RightMiddleFingerMetacarpalRigidBody, \
    RightMiddleFingerProximalPhalanxRigidBody, RightMiddleFingerMiddlePhalanxRigidBody, \
    RightMiddleFingerDistalPhalanxRigidBody, RightRingFingerMetacarpalRigidBody, \
    RightRingFingerProximalPhalanxRigidBody, RightRingFingerMiddlePhalanxRigidBody, \
    RightRingFingerDistalPhalanxRigidBody, RightPinkyFingerMetacarpalRigidBody, \
    RightPinkyFingerProximalPhalanxRigidBody, RightPinkyFingerMiddlePhalanxRigidBody, \
    RightPinkyFingerDistalPhalanxRigidBody

# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg


# Thumb
class RightThumbKnuckleLinkage(LinkageABC):
    bodies = [RightThumbMetacarpalRigidBody, RightThumbProximalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value

class RightThumbJointLinkage(LinkageABC):
    bodies = [RightThumbProximalPhalanxRigidBody, RightThumbDistalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


# Index
class RightIndexFingerKnuckleLinkage(LinkageABC):
    bodies = [RightIndexFingerMetacarpalRigidBody, RightIndexFingerProximalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value

class RightIndexFingerProximalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerProximalPhalanxRigidBody, RightIndexFingerMiddlePhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightIndexFingerDistalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerMiddlePhalanxRigidBody, RightIndexFingerDistalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

# Middle
class RightMiddleFingerKnuckleLinkage(LinkageABC):
    bodies = [RightMiddleFingerMetacarpalRigidBody, RightMiddleFingerProximalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value

class RightMiddleFingerProximalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerProximalPhalanxRigidBody, RightMiddleFingerMiddlePhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightMiddleFingerDistalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerMiddlePhalanxRigidBody, RightMiddleFingerDistalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value

# Ring
class RightRingFingerKnuckleLinkage(LinkageABC):
    bodies = [RightRingFingerMetacarpalRigidBody, RightRingFingerProximalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value

class RightRingFingerProximalJointLinkage(LinkageABC):
    bodies = [RightRingFingerProximalPhalanxRigidBody, RightRingFingerMiddlePhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightRingFingerDistalJointLinkage(LinkageABC):
    bodies = [RightRingFingerMiddlePhalanxRigidBody, RightRingFingerDistalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value

# Pinky
class RightPinkyFingerKnuckleLinkage(LinkageABC):
    bodies = [RightPinkyFingerMetacarpalRigidBody, RightPinkyFingerProximalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value

class RightPinkyFingerProximalJointLinkage(LinkageABC):
    bodies = [RightPinkyFingerProximalPhalanxRigidBody, RightPinkyFingerMiddlePhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightPinkyFingerDistalJointLinkage(LinkageABC):
    bodies = [RightPinkyFingerMiddlePhalanxRigidBody, RightPinkyFingerDistalPhalanxRigidBody]
    linked_keypoint = RightHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
