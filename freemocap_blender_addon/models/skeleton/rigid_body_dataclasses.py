from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import HeadKeypoints
from freemocap_blender_addon.models.skeleton.keypoint_rigid_body_abc import CompositeRigidBodyABC


class HeadRigidBody(CompositeRigidBodyABC):
    parent = HeadKeypoints.HEAD_CENTER
    children = [