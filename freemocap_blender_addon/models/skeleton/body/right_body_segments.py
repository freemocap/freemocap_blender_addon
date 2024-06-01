from freemocap_blender_addon.models.skeleton.body.rigid_body_abc import CompositeRigidBodyABC, SimpleRigidBodyABC
from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.keypoints_enum import Keypoint
from freemocap_blender_addon.models.skeleton.keypoints.right_side_keypoints import RightSideKeypoints


class RightClavicleRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.CHEST_CENTER.value
    child = RightSideKeypoints.RIGHT_SHOULDER.value


class RightUpperArmRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_SHOULDER.value
    child = RightSideKeypoints.RIGHT_ELBOW.value


class RightForearmRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_ELBOW.value
    child = RightSideKeypoints.RIGHT_WRIST.value


class RightPalmRigidBody(CompositeRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_WRIST.value
    children = RightSideKeypoints.to_list(exclude=[RightSideKeypoints.RIGHT_WRIST.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(RightSideKeypoints.RIGHT_PINKY_META_CARPO_PHALANGEAL.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(RightSideKeypoints.RIGHT_INDEX_META_CARPO_PHALANGEAL.value)


class RightPelvisRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.HIPS_CENTER.value
    child = RightSideKeypoints.RIGHT_HIP.value


class RightThighRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_HIP.value
    child = RightSideKeypoints.RIGHT_KNEE.value


class RightLegRigidBody(SimpleRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_KNEE.value
    child = RightSideKeypoints.RIGHT_ANKLE.value


class RightFootRigidBody(CompositeRigidBodyABC):
    parent = RightSideKeypoints.RIGHT_ANKLE.value
    children = RightSideKeypoints.to_list(exclude=[RightSideKeypoints.RIGHT_ANKLE.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(RightSideKeypoints.RIGHT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(RightSideKeypoints.RIGHT_HEEL.value)
