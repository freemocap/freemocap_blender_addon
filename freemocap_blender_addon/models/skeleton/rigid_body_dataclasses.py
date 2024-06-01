from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import HeadKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.lower_limb_keypoints import LeftFootKeypoints, RightFootKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.upper_limb_keypoints import RightPalmKeypoints, \
    LeftPalmKeypoints
from freemocap_blender_addon.models.skeleton.keypoints_enum import Keypoint
from freemocap_blender_addon.models.skeleton.rigid_body_abc import CompositeRigidBodyABC


class HeadRigidBody(CompositeRigidBodyABC):
    parent = HeadKeypoints.HEAD_CENTER.value
    children = HeadKeypoints.to_list(exclude=[HeadKeypoints.HEAD_CENTER.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(HeadKeypoints.NOSE.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(HeadKeypoints.LEFT_EAR_TRAGUS.value)


class RightPalmRigidBody(CompositeRigidBodyABC):
    parent = RightPalmKeypoints.RIGHT_WRIST.value
    children = RightPalmKeypoints.to_list(exclude=[RightPalmKeypoints.RIGHT_WRIST.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(RightPalmKeypoints.RIGHT_PINKY_KNUCKLE.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(RightPalmKeypoints.RIGHT_INDEX_KNUCKLE.value)


class RightFootRigidBody(CompositeRigidBodyABC):
    parent = RightFootKeypoints.RIGHT_ANKLE.value
    children = RightFootKeypoints.to_list(exclude=[RightFootKeypoints.RIGHT_ANKLE.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(RightFootKeypoints.RIGHT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(RightFootKeypoints.RIGHT_HEEL.value)


class LeftPalmRigidBody(CompositeRigidBodyABC):
    parent = LeftPalmKeypoints.LEFT_WRIST.value
    children = LeftPalmKeypoints.to_list(exclude=[LeftPalmKeypoints.LEFT_WRIST.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(LeftPalmKeypoints.LEFT_PINKY_KNUCKLE.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(LeftPalmKeypoints.LEFT_INDEX_KNUCKLE.value)


class LeftFootRigidBody(CompositeRigidBodyABC):
    parent = LeftFootKeypoints.LEFT_ANKLE.value
    children = LeftFootKeypoints.to_list(exclude=[LeftFootKeypoints.LEFT_ANKLE.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(LeftFootKeypoints.LEFT_HALLUX_TIP.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(LeftFootKeypoints.LEFT_HEEL.value)
