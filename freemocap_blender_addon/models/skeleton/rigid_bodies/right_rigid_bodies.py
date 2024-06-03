from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import KeypointABC
from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightBodyKeypoints
from freemocap_blender_addon.models.skeleton.rigid_bodies.abc_rigid_body import CompositeRigidBody, SimpleRigidBody


class RightClavicleRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.CHEST_CENTER.value
    child = RightBodyKeypoints.RIGHT_SHOULDER.value


class RightUpperArmRigidBody(SimpleRigidBody):
    parent = RightBodyKeypoints.RIGHT_SHOULDER.value
    child = RightBodyKeypoints.RIGHT_ELBOW.value


class RightForearmRigidBody(SimpleRigidBody):
    parent = RightBodyKeypoints.RIGHT_ELBOW.value
    child = RightBodyKeypoints.RIGHT_WRIST.value


class RightPalmRigidBody(CompositeRigidBody):
    parent = RightBodyKeypoints.RIGHT_WRIST.value
    children = [
        RightBodyKeypoints.RIGHT_THUMB_META_CARPO_PHALANGEAL.value,
        RightBodyKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value,
        RightBodyKeypoints.RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value,
        RightBodyKeypoints.RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value,
        RightBodyKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    ]

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(RightBodyKeypoints.RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(RightBodyKeypoints.RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value)


class RightPelvisRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.HIPS_CENTER.value
    child = RightBodyKeypoints.RIGHT_HIP.value


class RightThighRigidBody(SimpleRigidBody):
    parent = RightBodyKeypoints.RIGHT_HIP.value
    child = RightBodyKeypoints.RIGHT_KNEE.value


class RightLegRigidBody(SimpleRigidBody):
    parent = RightBodyKeypoints.RIGHT_KNEE.value
    child = RightBodyKeypoints.RIGHT_ANKLE.value


class RightFootRigidBody(CompositeRigidBody):
    parent = RightBodyKeypoints.RIGHT_ANKLE.value
    children = [
        RightBodyKeypoints.RIGHT_HEEL.value,
        RightBodyKeypoints.RIGHT_HALLUX_TIP.value
    ]

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(RightBodyKeypoints.RIGHT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(RightBodyKeypoints.RIGHT_HEEL.value)



