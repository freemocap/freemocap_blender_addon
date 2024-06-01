from freemocap_blender_addon.models.skeleton.body.rigid_body_abc import CompositeRigidBodyABC, SimpleRigidBodyABC
from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.keypoints_enum import Keypoint
from freemocap_blender_addon.models.skeleton.keypoints.left_side_keypoints import LeftSideKeypoints


class LeftClavicleRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.CHEST_CENTER.value
    child = LeftSideKeypoints.LEFT_SHOULDER.value


class LeftUpperArmRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_SHOULDER.value
    child = LeftSideKeypoints.LEFT_ELBOW.value


class LeftForearmRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_ELBOW.value
    child = LeftSideKeypoints.LEFT_WRIST.value


class LeftPalmRigidBody(CompositeRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_WRIST.value
    children = LeftSideKeypoints.to_list(exclude=[LeftSideKeypoints.LEFT_WRIST.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(LeftSideKeypoints.LEFT_PINKY_META_CARPO_PHALANGEAL.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(LeftSideKeypoints.LEFT_INDEX_META_CARPO_PHALANGEAL.value)


class LeftPelvisRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.HIPS_CENTER.value
    child = LeftSideKeypoints.LEFT_HIP.value


class LeftThighRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_HIP.value
    child = LeftSideKeypoints.LEFT_KNEE.value


class LeftLegRigidBody(SimpleRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_KNEE.value
    child = LeftSideKeypoints.LEFT_ANKLE.value


class LeftFootRigidBody(CompositeRigidBodyABC):
    parent = LeftSideKeypoints.LEFT_ANKLE.value
    children = LeftSideKeypoints.to_list(exclude=[LeftSideKeypoints.LEFT_ANKLE.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(LeftSideKeypoints.LEFT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(LeftSideKeypoints.LEFT_HEEL.value)
