from freemocap_blender_addon.models.skeleton.body.rigid_body_abc import SimpleRigidBodyABC
from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightSideKeypoints


# thumb
class RightThumbMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value


class RightThumbProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


class RightThumbDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_THUMB_TIP.value


# index
class RightIndexMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_INDEX_META_CARPO_PHALANGEAL.value


class RightIndexProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_INDEX_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_PROXIMAL_INTER_PHALANGEAL.value


class RightIndexMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_INDEX_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_DISTAL_INTER_PHALANGEAL.value


class RightIndexDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_INDEX_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_TIP.value


# middle
class RightMiddleMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_MIDDLE_META_CARPO_PHALANGEAL.value


class RightMiddleProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_MIDDLE_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value


class RightMiddleMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_DISTAL_INTER_PHALANGEAL.value


class RightMiddleDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_MIDDLE_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_TIP.value


# ring
class RightRingMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_RING_META_CARPO_PHALANGEAL.value


class RightRingProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_RING_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_PROXIMAL_INTER_PHALANGEAL.value


class RightRingMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_RING_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_DISTAL_INTER_PHALANGEAL.value


class RightRingDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_RING_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_TIP.value


# pinky
class RightPinkyMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_PINKY_META_CARPO_PHALANGEAL.value


class RightPinkyProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_PINKY_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_PROXIMAL_INTER_PHALANGEAL.value


class RightPinkyMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_PINKY_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_DISTAL_INTER_PHALANGEAL.value


class RightPinkyDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_PINKY_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_TIP.value
