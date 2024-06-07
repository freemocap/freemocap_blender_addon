from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints
from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import SimpleRigidBodyABC


class CervicalRigidBody(SimpleRigidBodyABC):
    parent = AxialSkeletonKeypoints.NECK_BASE_C7
    child = AxialSkeletonKeypoints.NECK_TOP_C1_ATLAS


class ThoracicRigidBody(SimpleRigidBodyABC):
    parent = AxialSkeletonKeypoints.CHEST_CENTER_T1
    child = AxialSkeletonKeypoints.NECK_BASE_C7


class LumbarRigidBody(SimpleRigidBodyABC):
    parent = AxialSkeletonKeypoints.PELVIS_CENTER
    child = AxialSkeletonKeypoints.CHEST_CENTER_T1


class AxialRigidBodies(Enum):
    CERVICAL: SimpleRigidBodyABC = CervicalRigidBody
    THORACIC: SimpleRigidBodyABC = ThoracicRigidBody
    LUMBAR: SimpleRigidBodyABC = LumbarRigidBody

if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in list(AxialRigidBodies)]))
