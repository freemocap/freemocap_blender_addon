from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, RightArmKeypoints, \
    RightMittenHandKeypoints, RightLegKeypoints
from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import CompoundRigidBodyABC, \
    SimpleRigidBodyABC


# arm
class RightClavicleRigidBody(SimpleRigidBodyABC):
    parent = AxialSkeletonKeypoints.CHEST_CENTER_T1
    child = RightArmKeypoints.RIGHT_SHOULDER


class RightUpperArmRigidBody(SimpleRigidBodyABC):
    parent = RightArmKeypoints.RIGHT_SHOULDER
    child = RightArmKeypoints.RIGHT_ELBOW


class RightForearmRigidBody(SimpleRigidBodyABC):
    parent = RightArmKeypoints.RIGHT_ELBOW
    child = RightArmKeypoints.RIGHT_WRIST


class RightWristIndexRigidBody(CompoundRigidBodyABC):
    parent = RightArmKeypoints.RIGHT_WRIST
    child = RightMittenHandKeypoints.RIGHT_INDEX_KNUCKLE


class RightWristPinkyRigidBody(CompoundRigidBodyABC):
    parent = RightArmKeypoints.RIGHT_WRIST
    child = RightMittenHandKeypoints.RIGHT_PINKY_KNUCKLE


class RightThumbRigidBody(SimpleRigidBodyABC):
    parent = RightArmKeypoints.RIGHT_WRIST
    child = RightMittenHandKeypoints.RIGHT_THUMB_KNUCKLE


# leg
class RightPelvisRigidBody(SimpleRigidBodyABC):
    parent = AxialSkeletonKeypoints.PELVIS_CENTER
    child = RightLegKeypoints.RIGHT_HIP


class RightThighRigidBody(SimpleRigidBodyABC):
    parent = RightLegKeypoints.RIGHT_HIP
    child = RightLegKeypoints.RIGHT_KNEE


class RightCalfRigidBody(SimpleRigidBodyABC):
    parent = RightLegKeypoints.RIGHT_KNEE
    child = RightLegKeypoints.RIGHT_ANKLE


class RightFootRigidBody(SimpleRigidBodyABC):
    parent = RightLegKeypoints.RIGHT_ANKLE
    child = RightLegKeypoints.RIGHT_HALLUX_TIP


class RightHeelRigidBody(SimpleRigidBodyABC):
    parent = RightLegKeypoints.RIGHT_ANKLE
    child = RightLegKeypoints.RIGHT_HALLUX_TIP


class RightBodyRigidBodies(Enum):
    RIGHT_CLAVICLE: SimpleRigidBodyABC = RightClavicleRigidBody
    RIGHT_UPPER_ARM: SimpleRigidBodyABC = RightUpperArmRigidBody
    RIGHT_FOREARM: SimpleRigidBodyABC = RightForearmRigidBody
    RIGHT_WRIST_INDEX: CompoundRigidBodyABC = RightWristIndexRigidBody
    RIGHT_WRIST_PINKY: CompoundRigidBodyABC = RightWristPinkyRigidBody
    RIGHT_THUMB: SimpleRigidBodyABC = RightThumbRigidBody
    RIGHT_PELVIS: SimpleRigidBodyABC = RightPelvisRigidBody
    RIGHT_THIGH: SimpleRigidBodyABC = RightThighRigidBody
    RIGHT_CALF: SimpleRigidBodyABC = RightCalfRigidBody
    RIGHT_FOOT: SimpleRigidBodyABC = RightFootRigidBody
    RIGHT_HEEL: SimpleRigidBodyABC = RightHeelRigidBody


if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}"
                     for rb in list(RightBodyRigidBodies)]))
