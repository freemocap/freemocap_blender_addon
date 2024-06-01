from freemocap_blender_addon.models.skeleton.body.rigid_body_abc import SimpleRigidBodyABC
from freemocap_blender_addon.models.skeleton.keypoints.left_side_keypoints import LeftSideKeypoints


# thumb
class LeftThumbMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_THUMB_META_CARPO_PHALANGEAL.value


class LeftThumbProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_THUMB_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_THUMB_INTER_PHALANGEAL.value


class LeftThumbDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_THUMB_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_THUMB_TIP.value


# index
class LeftIndexMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_INDEX_META_CARPO_PHALANGEAL.value


class LeftIndexProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_INDEX_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_INDEX_PROXIMAL_INTER_PHALANGEAL.value


class LeftIndexMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_INDEX_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_INDEX_DISTAL_INTER_PHALANGEAL.value


class LeftIndexDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_INDEX_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_INDEX_TIP.value


# middle
class LeftMiddleMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_MIDDLE_META_CARPO_PHALANGEAL.value


class LeftMiddleProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_MIDDLE_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value


class LeftMiddleMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_MIDDLE_DISTAL_INTER_PHALANGEAL.value


class LeftMiddleDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_MIDDLE_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_MIDDLE_TIP.value


# ring
class LeftRingMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_RING_META_CARPO_PHALANGEAL.value


class LeftRingProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_RING_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_RING_PROXIMAL_INTER_PHALANGEAL.value


class LeftRingMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_RING_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_RING_DISTAL_INTER_PHALANGEAL.value


class LeftRingDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_RING_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_RING_TIP.value


# pinky
class LeftPinkyMetacarpalRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_PINKY_META_CARPO_PHALANGEAL.value


class LeftPinkyProximalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_PINKY_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_PINKY_PROXIMAL_INTER_PHALANGEAL.value


class LeftPinkyMiddlePhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_PINKY_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_PINKY_DISTAL_INTER_PHALANGEAL.value


class LeftPinkyDistalPhalanxRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_PINKY_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_PINKY_TIP.value
