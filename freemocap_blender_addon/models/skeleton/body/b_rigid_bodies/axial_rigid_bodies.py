from freemocap_blender_addon.models.skeleton.body.a_keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import SimpleRigidBodyABC


class CervicalRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.NECK_C7.value
    child = AxialBodyKeypoints.NECK_C1.value


class ThoracicRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.CHEST_T1_CENTER.value
    child = AxialBodyKeypoints.NECK_C7.value


class LumbarRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.PELVIS_SACRUM.value
    child = AxialBodyKeypoints.CHEST_T1_CENTER.value

class AxialSkeletonRigidBodies:
    CERVICAL: SimpleRigidBodyABC = CervicalRigidBody
    THORACIC: SimpleRigidBodyABC = ThoracicRigidBody
    LUMBAR: SimpleRigidBodyABC = LumbarRigidBody