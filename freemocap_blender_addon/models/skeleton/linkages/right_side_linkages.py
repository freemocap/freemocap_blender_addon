from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightSideKeypoints
from freemocap_blender_addon.models.skeleton.linkages.abc_linkage import LinkageABC
from freemocap_blender_addon.models.skeleton.rigid_bodies.right_rigid_bodies import RightUpperArmRigidBody, \
    RightClavicleRigidBody, RightForearmRigidBody, RightPalmRigidBody, RightThumbMetacarpalRigidBody, \
    RightPinkyMetacarpalRigidBody, RightRingMetacarpalRigidBody, RightMiddleFingerMetacarpalRigidBody, \
    RightIndexFingerMetacarpalRigidBody, RightThumbProximalPhalanxRigidBody, RightThumbDistalPhalanxRigidBody, \
    RightIndexFingerProximalPhalanxRigidBody, RightIndexFingerMiddlePhalanxRigidBody, \
    RightIndexFingerDistalPhalanxRigidBody, RightMiddleFingerDistalPhalanxRigidBody, \
    RightMiddleFingerMiddlePhalanxRigidBody, RightMiddleFingerProximalPhalanxRigidBody, \
    RightRingFingerDistalPhalanxRigidBody, RightRingFingerMiddlePhalanxRigidBody, \
    RightRingFingerProximalPhalanxRigidBody


class RightShoulderLinkage(LinkageABC):
    bodies = [RightClavicleRigidBody, RightUpperArmRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_SHOULDER.value


class RightElbowLinkage(LinkageABC):
    bodies = [RightUpperArmRigidBody, RightForearmRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_ELBOW.value


class RightWristLinkage(LinkageABC):
    # TODO - handle this differently... sholdn't connect all the metacarpals to the wrist, they should, like, lie on the sruface of a fixed elipse or something?
    bodies = [RightForearmRigidBody,
              RightPalmRigidBody,
              RightThumbMetacarpalRigidBody,
              RightIndexFingerMetacarpalRigidBody,
              RightMiddleFingerMetacarpalRigidBody,
              RightRingMetacarpalRigidBody,
              RightPinkyMetacarpalRigidBody,
              ]
    linked_keypoint = RightSideKeypoints.RIGHT_WRIST.value

# Thumb
class RightThumbKnuckleLinkage(LinkageABC):
    bodies = [RightThumbMetacarpalRigidBody, RightThumbProximalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value

class RightThumbJointLinkage(LinkageABC):
    bodies = [RightThumbProximalPhalanxRigidBody, RightThumbDistalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


# Index
class RightIndexFingerKnuckleLinkage(LinkageABC):
    bodies = [RightIndexFingerMetacarpalRigidBody, RightIndexFingerProximalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value

class RightIndexFingerProximalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerProximalPhalanxRigidBody, RightIndexFingerMiddlePhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightIndexFingerDistalJointLinkage(LinkageABC):
    bodies = [RightIndexFingerMiddlePhalanxRigidBody, RightIndexFingerDistalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value

# Middle
class RightMiddleFingerKnuckleLinkage(LinkageABC):
    bodies = [RightMiddleFingerMetacarpalRigidBody, RightMiddleFingerProximalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value

class RightMiddleFingerProximalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerProximalPhalanxRigidBody, RightMiddleFingerMiddlePhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightMiddleFingerDistalJointLinkage(LinkageABC):
    bodies = [RightMiddleFingerMiddlePhalanxRigidBody, RightMiddleFingerDistalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value

# Ring
class RightRingFingerKnuckleLinkage(LinkageABC):
    bodies = [RightRingMetacarpalRigidBody, RightRingFingerProximalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value

class RightRingFingerProximalJointLinkage(LinkageABC):
    bodies = [RightRingFingerProximalPhalanxRigidBody, RightRingFingerMiddlePhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value

class RightRingFingerDistalJointLinkage(LinkageABC):
    bodies = [RightRingFingerMiddlePhalanxRigidBody, RightRingFingerDistalPhalanxRigidBody]
    linked_keypoint = RightSideKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value