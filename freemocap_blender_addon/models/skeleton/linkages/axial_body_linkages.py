from freemocap_blender_addon.models.skeleton.keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.linkages.abc_linkage import LinkageABC
from freemocap_blender_addon.models.skeleton.rigid_bodies.axial_rigid_bodies import LumbarRigidBody, CervicalRigidBody, \
    SkullRigidBody, ThoracicRigidBody
from freemocap_blender_addon.models.skeleton.rigid_bodies.left_rigid_bodies import LeftPelvisRigidBody, \
    LeftClavicleRigidBody

from freemocap_blender_addon.models.skeleton.rigid_bodies.right_rigid_bodies import RightPelvisRigidBody, \
    RightClavicleRigidBody


class AtlasLinkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    bodies = [CervicalRigidBody, SkullRigidBody]
    linked_keypoint = AxialBodyKeypoints.SKULL_CENTER.value


class CervicalSpineLinkage(LinkageABC):
    bodies = [LumbarRigidBody, CervicalRigidBody]
    linked_keypoint = AxialBodyKeypoints.NECK_C7.value


class ClavicleLinkage(LinkageABC):
    bodies = [CervicalRigidBody, ThoracicRigidBody, RightClavicleRigidBody, LeftClavicleRigidBody]
    linked_keypoint = AxialBodyKeypoints.NECK_C1.value


class AbdomenLinkage(LinkageABC):
    bodies = [LumbarRigidBody]
    linked_keypoint = AxialBodyKeypoints.CHEST_CENTER.value


class PelvisLinkage(LinkageABC):
    """
    Note - this is a 'fixed' linkage, meaning the distance between all keypoints stays fixed.
    It really should be a CompositeRigidBody, but we don't have sufficient geometry to define it because
    the outer keypoints are linked via a virtual marker defined by keypoints within the linkage
    """
    bodies = [LeftPelvisRigidBody, RightPelvisRigidBody, LumbarRigidBody]
    linked_keypoint = AxialBodyKeypoints.HIPS_CENTER.value
