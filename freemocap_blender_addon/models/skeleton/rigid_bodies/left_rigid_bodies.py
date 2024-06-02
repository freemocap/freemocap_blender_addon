from freemocap_blender_addon.models.skeleton.rigid_bodies.abc_rigid_body import CompositeRigidBody, SimpleRigidBody
from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import KeypointABC
from freemocap_blender_addon.models.skeleton.keypoints.left_side_keypoints import LeftSideKeypoints


class LeftClavicleRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.CHEST_CENTER.value
    child = LeftSideKeypoints.LEFT_SHOULDER.value


class LeftUpperArmRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_SHOULDER.value
    child = LeftSideKeypoints.LEFT_ELBOW.value


class LeftForearmRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_ELBOW.value
    child = LeftSideKeypoints.LEFT_WRIST.value


class LeftPalmRigidBody(CompositeRigidBody):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    children = LeftSideKeypoints.to_list(exclude=[LeftSideKeypoints.LEFT_WRIST.value])

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_PINKY_META_CARPO_PHALANGEAL.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_INDEX_META_CARPO_PHALANGEAL.value)


class LeftPelvisRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.HIPS_CENTER.value
    child = LeftSideKeypoints.LEFT_HIP.value


class LeftThighRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_HIP.value
    child = LeftSideKeypoints.LEFT_KNEE.value


class LeftLegRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_KNEE.value
    child = LeftSideKeypoints.LEFT_ANKLE.value


class LeftFootRigidBody(CompositeRigidBody):
    parent = LeftSideKeypoints.LEFT_ANKLE.value
    children = LeftSideKeypoints.to_list(exclude=[LeftSideKeypoints.LEFT_ANKLE.value])

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_HEEL.value)


# Hand


# thumb
class LeftThumbMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_THUMB_META_CARPO_PHALANGEAL.value


class LeftThumbProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_THUMB_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_THUMB_INTER_PHALANGEAL.value


class LeftThumbDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_THUMB_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_THUMB_TIP.value


# index
class LeftIndexMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_INDEX_META_CARPO_PHALANGEAL.value


class LeftIndexProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_INDEX_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_INDEX_PROXIMAL_INTER_PHALANGEAL.value


class LeftIndexMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_INDEX_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_INDEX_DISTAL_INTER_PHALANGEAL.value


class LeftIndexDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_INDEX_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_INDEX_TIP.value


# middle
class LeftMiddleMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_MIDDLE_META_CARPO_PHALANGEAL.value


class LeftMiddleProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_MIDDLE_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value


class LeftMiddleMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_MIDDLE_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_MIDDLE_DISTAL_INTER_PHALANGEAL.value


class LeftMiddleDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_MIDDLE_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_MIDDLE_TIP.value


# ring
class LeftRingMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_RING_META_CARPO_PHALANGEAL.value


class LeftRingProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_RING_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_RING_PROXIMAL_INTER_PHALANGEAL.value


class LeftRingMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_RING_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_RING_DISTAL_INTER_PHALANGEAL.value


class LeftRingDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_RING_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_RING_TIP.value


# pinky
class LeftPinkyMetacarpalRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    child = LeftSideKeypoints.LEFT_PINKY_META_CARPO_PHALANGEAL.value


class LeftPinkyProximalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_PINKY_META_CARPO_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_PINKY_PROXIMAL_INTER_PHALANGEAL.value


class LeftPinkyMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_PINKY_PROXIMAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_PINKY_DISTAL_INTER_PHALANGEAL.value


class LeftPinkyDistalPhalanxRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_PINKY_DISTAL_INTER_PHALANGEAL.value
    child = LeftSideKeypoints.LEFT_PINKY_TIP.value
