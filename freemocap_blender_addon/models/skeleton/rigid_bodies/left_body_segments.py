from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import KeypointABC
from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.left_side_keypoints import LeftSideKeypoints
from freemocap_blender_addon.models.skeleton.rigid_bodies.abc_rigid_body import CompositeRigidBody, SimpleRigidBody


class LeftClavicleRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.CHEST_CENTER.value
    child = LeftSideKeypoints.LEFT_RIGHT_SHOULDER.value


class LeftUpperArmRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_RIGHT_SHOULDER.value
    child = LeftSideKeypoints.LEFT_RIGHT_ELBOW.value


class LeftForearmRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_RIGHT_ELBOW.value
    child = LeftSideKeypoints.LEFT_RIGHT_WRIST.value


class LeftPalmRigidBody(CompositeRigidBody):
    parent = LeftSideKeypoints.LEFT_RIGHT_WRIST.value
    children = [
        LeftSideKeypoints.LEFT_RIGHT_THUMB_META_CARPO_PHALANGEAL.value,
        LeftSideKeypoints.LEFT_RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value,
        LeftSideKeypoints.LEFT_RIGHT_MIDDLE_FINGER_META_CARPO_PHALANGEAL.value,
        LeftSideKeypoints.LEFT_RIGHT_RING_FINGER_META_CARPO_PHALANGEAL.value,
        LeftSideKeypoints.LEFT_RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value
    ]

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_RIGHT_PINKY_FINGER_META_CARPO_PHALANGEAL.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_RIGHT_INDEX_FINGER_META_CARPO_PHALANGEAL.value)


class LeftPelvisRigidBody(SimpleRigidBody):
    parent = AxialBodyKeypoints.HIPS_CENTER.value
    child = LeftSideKeypoints.LEFT_RIGHT_HIP.value


class LeftThighRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_RIGHT_HIP.value
    child = LeftSideKeypoints.LEFT_RIGHT_KNEE.value


class LeftLegRigidBody(SimpleRigidBody):
    parent = LeftSideKeypoints.LEFT_RIGHT_KNEE.value
    child = LeftSideKeypoints.LEFT_RIGHT_ANKLE.value


class LeftFootRigidBody(CompositeRigidBody):
    parent = LeftSideKeypoints.LEFT_RIGHT_ANKLE.value
    children = [
        LeftSideKeypoints.LEFT_RIGHT_HEEL.value,
        LeftSideKeypoints.LEFT_RIGHT_HALLUX_TIP.value
    ]

    @property
    def positive_x(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_RIGHT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> KeypointABC:
        return self.get_child(LeftSideKeypoints.LEFT_RIGHT_HEEL.value)



