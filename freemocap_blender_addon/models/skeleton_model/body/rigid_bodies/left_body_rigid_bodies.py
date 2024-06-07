from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, LeftArmKeypoints, \
    LeftMittenHandKeypoints, LeftLegKeypoints
from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import CompoundRigidBodyABC, \
    SimpleRigidBodyABC


# arm
class LeftClavicleRigidBody(SimpleRigidBodyABC):
    parent = AxialSkeletonKeypoints.CHEST_CENTER_T1
    child = LeftArmKeypoints.LEFT_SHOULDER


class LeftUpperArmRigidBody(SimpleRigidBodyABC):
    parent = LeftArmKeypoints.LEFT_SHOULDER
    child = LeftArmKeypoints.LEFT_ELBOW


class LeftForearmRigidBody(SimpleRigidBodyABC):
    parent = LeftArmKeypoints.LEFT_ELBOW
    child = LeftArmKeypoints.LEFT_WRIST


class LeftWristIndexRigidBody(CompoundRigidBodyABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_INDEX_KNUCKLE


class LeftWristPinkyRigidBody(CompoundRigidBodyABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_PINKY_KNUCKLE


class LeftThumbRigidBody(SimpleRigidBodyABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_THUMB_KNUCKLE


# leg
class LeftPelvisRigidBody(SimpleRigidBodyABC):
    parent = AxialSkeletonKeypoints.PELVIS_CENTER
    child = LeftLegKeypoints.LEFT_HIP


class LeftThighRigidBody(SimpleRigidBodyABC):
    parent = LeftLegKeypoints.LEFT_HIP
    child = LeftLegKeypoints.LEFT_KNEE


class LeftCalfRigidBody(SimpleRigidBodyABC):
    parent = LeftLegKeypoints.LEFT_KNEE
    child = LeftLegKeypoints.LEFT_ANKLE


class LeftFootRigidBody(SimpleRigidBodyABC):
    parent = LeftLegKeypoints.LEFT_ANKLE
    child = LeftLegKeypoints.LEFT_HALLUX_TIP


class LeftHeelRigidBody(SimpleRigidBodyABC):
    parent = LeftLegKeypoints.LEFT_ANKLE
    child = LeftLegKeypoints.LEFT_HALLUX_TIP


class LeftBodyRigidBodies(Enum):
    LEFT_CLAVICLE: SimpleRigidBodyABC = LeftClavicleRigidBody
    LEFT_UPPER_ARM: SimpleRigidBodyABC = LeftUpperArmRigidBody
    LEFT_FOREARM: SimpleRigidBodyABC = LeftForearmRigidBody
    LEFT_WRIST_INDEX: CompoundRigidBodyABC = LeftWristIndexRigidBody
    LEFT_WRIST_PINKY: CompoundRigidBodyABC = LeftWristPinkyRigidBody
    LEFT_THUMB: SimpleRigidBodyABC = LeftThumbRigidBody
    LEFT_PELVIS: SimpleRigidBodyABC = LeftPelvisRigidBody
    LEFT_THIGH: SimpleRigidBodyABC = LeftThighRigidBody
    LEFT_CALF: SimpleRigidBodyABC = LeftCalfRigidBody
    LEFT_FOOT: SimpleRigidBodyABC = LeftFootRigidBody
    LEFT_HEEL: SimpleRigidBodyABC = LeftHeelRigidBody


if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}"
                     for rb in list(LeftBodyRigidBodies)]))
