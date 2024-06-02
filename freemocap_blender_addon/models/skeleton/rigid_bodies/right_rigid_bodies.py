from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import KeypointABC
from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightSideKeypoints
from freemocap_blender_addon.models.skeleton.rigid_bodies.abc_rigid_body import CompositeRigidBody, SimpleRigidBody


class RightClavicleRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.CHEST_CENTER.value
    child = RightSideKeypoints.RIGHT_SHOULDER.value


class RightUpperArmRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_SHOULDER.value
    child = RightSideKeypoints.RIGHT_ELBOW.value


class RightForearmRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_ELBOW.value
    child = RightSideKeypoints.RIGHT_WRIST.value


class RightPalmRigidBody(CompositeRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    children = [
        RightSideKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value,
        RightSideKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value,
        RightSideKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value,
        RightSideKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value,
        RightSideKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    ]

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(RightSideKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(RightSideKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value)


class RightPelvisRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.HIPS_CENTER.value
    child = RightSideKeypoints.RIGHT_HIP.value


class RightThighRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_HIP.value
    child = RightSideKeypoints.RIGHT_KNEE.value


class RightLegRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_KNEE.value
    child = RightSideKeypoints.RIGHT_ANKLE.value


class RightFootRigidBody(CompositeRigidBody):
    parent = RightSideKeypoints.RIGHT_ANKLE.value
    children = [
        RightSideKeypoints.RIGHT_HEEL.value,
        RightSideKeypoints.RIGHT_HALLUX_TIP.value
    ]

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(RightSideKeypoints.RIGHT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(RightSideKeypoints.RIGHT_HEEL.value)


# Hand

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
class RightIndexFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value


class RightIndexFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightIndexFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_INDEX_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightIndexFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_INDEX_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_INDEX_FINGER_TIP.value


# middle
class RightMiddleFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value


class RightMiddleFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightMiddleFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_MIDDLE_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightMiddleFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_MIDDLE_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_MIDDLE_FINGER_TIP.value


# ring
class RightRingFingerMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value


class RightRingFingerProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightRingFingerMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_RING_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightRingFingerDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_RING_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_RING_FINGER_TIP.value


# pinky
class RightPinkyMetacarpalRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    child = RightSideKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value


class RightPinkyProximalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value


class RightPinkyMiddlePhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_PINKY_FINGER_PROXIMAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value


class RightPinkyDistalPhalanxRigidBody(SimpleRigidBody):
    parent = RightSideKeypoints.RIGHT_PINKY_FINGER_DISTAL_INTER_PHALANGEAL.value
    child = RightSideKeypoints.RIGHT_PINKY_FINGER_TIP.value
