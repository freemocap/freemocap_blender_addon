from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import SkullKeypoints
from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import CompoundRigidBodyABC, \
    SimpleRigidBodyABC


class SkullRigidBody(CompoundRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1,
    children = [SkullKeypoints.NOSE_TIP,
                SkullKeypoints.SKULL_TOP_BREGMA,
                SkullKeypoints.RIGHT_EYE_INNER,
                SkullKeypoints.RIGHT_EYE_CENTER,
                SkullKeypoints.RIGHT_EYE_OUTER,
                SkullKeypoints.RIGHT_EAR_TRAGUS,
                SkullKeypoints.RIGHT_MOUTH,
                SkullKeypoints.LEFT_EYE_INNER,
                SkullKeypoints.LEFT_EYE_CENTER,
                SkullKeypoints.LEFT_EYE_OUTER,
                SkullKeypoints.LEFT_EAR_TRAGUS,
                SkullKeypoints.LEFT_MOUTH]

    shared_keypoint = SkullKeypoints.SKULL_CENTER_C1
    positive_x = SkullKeypoints.NOSE_TIP
    approximate_positive_y = SkullKeypoints.LEFT_EAR_TRAGUS


class SkullNoseRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.NOSE_TIP


class SkullTopRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.SKULL_TOP_BREGMA


class SkullRightEyeInnerRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.RIGHT_EYE_INNER


class SkullRightEyeCenterRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.RIGHT_EYE_CENTER


class SkullRightEyeOuterRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.RIGHT_EYE_OUTER


class SkullRightEarTragusRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.RIGHT_EAR_TRAGUS


class SkullRightMouthRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.RIGHT_MOUTH


class SkullLeftEyeInnerRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.LEFT_EYE_INNER


class SkullLeftEyeCenterRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.LEFT_EYE_CENTER


class SkullLeftEyeOuterRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.LEFT_EYE_OUTER


class SkullLeftEarTragusRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.LEFT_EAR_TRAGUS


class SkullLeftMouthRigidBody(SimpleRigidBodyABC):
    parent = SkullKeypoints.SKULL_CENTER_C1
    child = SkullKeypoints.LEFT_MOUTH


class SkullRigidBodies(Enum):
    # TODO - go harder on the naming convention - https://www.sciencedirect.com/science/article/pii/S0169260721004545
    # COMPOUND: CompoundRigidBodyABC = SkullRigidBody
    NOSE: SimpleRigidBodyABC = SkullNoseRigidBody
    TOP: SimpleRigidBodyABC = SkullTopRigidBody
    RIGHT_EYE_INNER: SimpleRigidBodyABC = SkullRightEyeInnerRigidBody
    RIGHT_EYE_CENTER: SimpleRigidBodyABC = SkullRightEyeCenterRigidBody
    RIGHT_EYE_OUTER: SimpleRigidBodyABC = SkullRightEyeOuterRigidBody
    RIGHT_EAR_TRAGUS: SimpleRigidBodyABC = SkullRightEarTragusRigidBody
    RIGHT_MOUTH: SimpleRigidBodyABC = SkullRightMouthRigidBody
    LEFT_EYE_INNER: SimpleRigidBodyABC = SkullLeftEyeInnerRigidBody
    LEFT_EYE_CENTER: SimpleRigidBodyABC = SkullLeftEyeCenterRigidBody
    LEFT_EYE_OUTER: SimpleRigidBodyABC = SkullLeftEyeOuterRigidBody
    LEFT_EAR_TRAGUS: SimpleRigidBodyABC = SkullLeftEarTragusRigidBody
    LEFT_MOUTH: SimpleRigidBodyABC = SkullLeftMouthRigidBody


# Example usage
if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in
                     list(SkullRigidBodies)]))

