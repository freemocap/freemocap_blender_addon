from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import LeftHandKeypoints
from freemocap_blender_addon.models.skeleton.linkages.abc_linkage import LinkageABC
from freemocap_blender_addon.models.skeleton.rigid_bodies.left_hand_rigid_bodies import LeftThumbMetacarpalRigidBody, \
    LeftThumbProximalPhalanxRigidBody, LeftThumbDistalPhalanxRigidBody, LeftIndexFingerMetacarpalRigidBody, \
    LeftIndexFingerProximalPhalanxRigidBody, LeftIndexFingerMiddlePhalanxRigidBody, \
    LeftIndexFingerDistalPhalanxRigidBody, LeftMiddleFingerMetacarpalRigidBody, \
    LeftMiddleFingerProximalPhalanxRigidBody, LeftMiddleFingerMiddlePhalanxRigidBody, \
    LeftMiddleFingerDistalPhalanxRigidBody, LeftRingFingerMetacarpalRigidBody, \
    LeftRingFingerProximalPhalanxRigidBody, LeftRingFingerMiddlePhalanxRigidBody, \
    LeftRingFingerDistalPhalanxRigidBody, LeftPinkyFingerMetacarpalRigidBody, \
    LeftPinkyFingerProximalPhalanxRigidBody, LeftPinkyFingerMiddlePhalanxRigidBody, \
    LeftPinkyFingerDistalPhalanxRigidBody

# hand
# https://www.assh.org/handcare/safety/joints
# https://en.wikipedia.org/wiki/Hand#/media/File:814_Radiograph_of_Hand.jpg


# Thumb
class LeftThumbKnuckleLinkage(LinkageABC):
    bodies = [LeftThumbMetacarpalRigidBody, LeftThumbProximalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value

class LeftThumbJointLinkage(LinkageABC):
    bodies = [LeftThumbProximalPhalanxRigidBody, LeftThumbDistalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


# Index
class LeftIndexFingerKnuckleLinkage(LinkageABC):
    bodies = [LeftIndexFingerMetacarpalRigidBody, LeftIndexFingerProximalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value

class LeftIndexFingerProximalJointLinkage(LinkageABC):
    bodies = [LeftIndexFingerProximalPhalanxRigidBody, LeftIndexFingerMiddlePhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class LeftIndexFingerDistalJointLinkage(LinkageABC):
    bodies = [LeftIndexFingerMiddlePhalanxRigidBody, LeftIndexFingerDistalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

# Middle
class LeftMiddleFingerKnuckleLinkage(LinkageABC):
    bodies = [LeftMiddleFingerMetacarpalRigidBody, LeftMiddleFingerProximalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value

class LeftMiddleFingerProximalJointLinkage(LinkageABC):
    bodies = [LeftMiddleFingerProximalPhalanxRigidBody, LeftMiddleFingerMiddlePhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class LeftMiddleFingerDistalJointLinkage(LinkageABC):
    bodies = [LeftMiddleFingerMiddlePhalanxRigidBody, LeftMiddleFingerDistalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value

# Ring
class LeftRingFingerKnuckleLinkage(LinkageABC):
    bodies = [LeftRingFingerMetacarpalRigidBody, LeftRingFingerProximalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value

class LeftRingFingerProximalJointLinkage(LinkageABC):
    bodies = [LeftRingFingerProximalPhalanxRigidBody, LeftRingFingerMiddlePhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class LeftRingFingerDistalJointLinkage(LinkageABC):
    bodies = [LeftRingFingerMiddlePhalanxRigidBody, LeftRingFingerDistalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value

# Pinky
class LeftPinkyFingerKnuckleLinkage(LinkageABC):
    bodies = [LeftPinkyFingerMetacarpalRigidBody, LeftPinkyFingerProximalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value

class LeftPinkyFingerProximalJointLinkage(LinkageABC):
    bodies = [LeftPinkyFingerProximalPhalanxRigidBody, LeftPinkyFingerMiddlePhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class LeftPinkyFingerDistalJointLinkage(LinkageABC):
    bodies = [LeftPinkyFingerMiddlePhalanxRigidBody, LeftPinkyFingerDistalPhalanxRigidBody]
    linked_keypoint = LeftHandKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
