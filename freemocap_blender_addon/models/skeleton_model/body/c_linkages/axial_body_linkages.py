from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import LinkageABC
from freemocap_blender_addon.models.skeleton_model.body.a_keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.b_rigid_bodies.axial_rigid_bodies import CervicalRigidBody, \
    LumbarRigidBody, ThoracicRigidBody
from freemocap_blender_addon.models.skeleton_model.body.b_rigid_bodies.skull_rigid_bodies import SkullRigidBody
from freemocap_blender_addon.models.skeleton_model.body.b_rigid_bodies.right_body_rigid_bodies import RightClavicleRigidBody, \
    RightPelvisRigidBody


class SkullC1Linkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    bodies = [CervicalRigidBody, SkullRigidBody]
    linked_keypoint = AxialBodyKeypoints.SKULL_C1.value


class NeckC7Linkage(LinkageABC):
    bodies = [LumbarRigidBody, CervicalRigidBody]
    linked_keypoint = AxialBodyKeypoints.NECK_C7.value


class NeckC1Linkage(LinkageABC):
    bodies = [CervicalRigidBody,
              ThoracicRigidBody,
              RightClavicleRigidBody,
              # LeftClavicleRigidBody
              ]
    linked_keypoint = AxialBodyKeypoints.NECK_C1.value


class ChestT1Linkage(LinkageABC):
    bodies = [LumbarRigidBody, ThoracicRigidBody]
    linked_keypoint = AxialBodyKeypoints.CHEST_T1_CENTER.value


class PelvisSacrumLinkage(LinkageABC):
    """
    Note - this is a 'fixed' linkage, meaning the distance between all keypoints stays fixed.
    It really should be a CompoundRigidBody, but we don't have sufficient geometry to define it because
    the outer keypoints are linked via a virtual marker defined by keypoints within the linkage
    """
    bodies = [LumbarRigidBody,
              RightPelvisRigidBody,
              # LeftPelvisRigidBody,
              ]
    linked_keypoint = AxialBodyKeypoints.PELVIS_SACRUM.value
