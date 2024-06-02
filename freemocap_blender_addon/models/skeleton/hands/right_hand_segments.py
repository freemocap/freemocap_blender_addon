from freemocap_blender_addon.models.skeleton.body.rigid_body_abc import SimpleRigidBody
from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightSideKeypoints


# thumb
class RightThumbMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value


class RightThumbProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value


class RightThumbDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_THUMB_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_THUMB_TIP.value


# index
class RightIndexMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_INDEX_META_CARPO_PHALANGEAL.value


class RightIndexProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_INDEX_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_PROXIMAL_INTER_PHALANGEAL.value


class RightIndexMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_INDEX_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_DISTAL_INTER_PHALANGEAL.value


class RightIndexDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_INDEX_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_TIP.value


# middle
class RightMiddleMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_MIDDLE_META_CARPO_PHALANGEAL.value


class RightMiddleProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_MIDDLE_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value


class RightMiddleMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_DISTAL_INTER_PHALANGEAL.value


class RightMiddleDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_MIDDLE_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_TIP.value


# ring
class RightRingMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_RING_META_CARPO_PHALANGEAL.value


class RightRingProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_RING_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_PROXIMAL_INTER_PHALANGEAL.value


class RightRingMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_RING_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_DISTAL_INTER_PHALANGEAL.value


class RightRingDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_RING_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_TIP.value


# pinky
class RightPinkyMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_PINKY_META_CARPO_PHALANGEAL.value


class RightPinkyProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_PINKY_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_PROXIMAL_INTER_PHALANGEAL.value


class RightPinkyMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_PINKY_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_DISTAL_INTER_PHALANGEAL.value


class RightPinkyDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_PINKY_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_TIP.value
