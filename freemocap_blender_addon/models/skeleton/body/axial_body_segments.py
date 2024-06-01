from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import HeadKeypoints, TorsoKeypoints
from freemocap_blender_addon.models.skeleton.keypoints.keypoints_enum import Keypoint
from freemocap_blender_addon.models.skeleton.body.rigid_body_abc import CompositeRigidBodyABC, \
    SimpleRigidBodyABC


class HeadRigidBody(CompositeRigidBodyABC):
    parent = HeadKeypoints.HEAD_CENTER.value
    children = HeadKeypoints.to_list(exclude=[HeadKeypoints.HEAD_CENTER.value])

    @property
    def positive_x(self) -> Keypoint:
        return self.get_child(HeadKeypoints.NOSE.value)

    @property
    def approximate_positive_y(self) -> Keypoint:
        return self.get_child(HeadKeypoints.LEFT_EAR_TRAGUS.value)


class NeckRigidBody(SimpleRigidBodyABC):
    parent = TorsoKeypoints.NECK_C7.value
    child = TorsoKeypoints.NECK_C1.value


class ChestRigidBody(SimpleRigidBodyABC):
    parent = TorsoKeypoints.CHEST_CENTER.value
    child = TorsoKeypoints.NECK_C7.value


class AbdomenRigidBody(SimpleRigidBodyABC):
    parent = TorsoKeypoints.HIPS_CENTER.value
    child = TorsoKeypoints.CHEST_CENTER.value
