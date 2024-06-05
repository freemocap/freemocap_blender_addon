from enum import Enum

from freemocap_blender_addon.models.skeleton.body.a_keypoints.axial_body_keypoints import AxialBodyKeypoints
from freemocap_blender_addon.models.skeleton.keypoint_rigidbody_linkage_chain_abc import CompoundRigidBodyABC, \
    SimpleRigidBodyABC


class SkullRigidBody(CompoundRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    children = [AxialBodyKeypoints.NOSE.value,
                AxialBodyKeypoints.SKULL_BREGMA.value,
                AxialBodyKeypoints.RIGHT_EYE_INNER.value,
                AxialBodyKeypoints.RIGHT_EYE_CENTER.value,
                AxialBodyKeypoints.RIGHT_EYE_OUTER.value,
                AxialBodyKeypoints.RIGHT_EAR_TRAGUS.value,
                AxialBodyKeypoints.RIGHT_MOUTH.value,
                AxialBodyKeypoints.LEFT_EYE_INNER.value,
                AxialBodyKeypoints.LEFT_EYE_CENTER.value,
                AxialBodyKeypoints.LEFT_EYE_OUTER.value,
                AxialBodyKeypoints.LEFT_EAR_TRAGUS.value,
                AxialBodyKeypoints.LEFT_MOUTH.value]

    shared_keypoint = AxialBodyKeypoints.SKULL_C1.value
    positive_x = AxialBodyKeypoints.NOSE.value
    approximate_positive_y = AxialBodyKeypoints.LEFT_EAR_TRAGUS.value


class SkullNoseRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.NOSE.value


class SkullBregmaRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.SKULL_BREGMA.value


class SkullRightEyeInnerRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.RIGHT_EYE_INNER.value


class SkullRightEyeCenterRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.RIGHT_EYE_CENTER.value


class SkullRightEyeOuterRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.RIGHT_EYE_OUTER.value


class SkullRightEarTragusRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.RIGHT_EAR_TRAGUS.value


class SkullRightMouthRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.RIGHT_MOUTH.value


class SkullLeftEyeInnerRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.LEFT_EYE_INNER.value


class SkullLeftEyeCenterRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.LEFT_EYE_CENTER.value


class SkullLeftEyeOuterRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.LEFT_EYE_OUTER.value


class SkullLeftEarTragusRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.LEFT_EAR_TRAGUS.value


class SkullLeftMouthRigidBody(SimpleRigidBodyABC):
    parent = AxialBodyKeypoints.SKULL_C1.value
    child = AxialBodyKeypoints.LEFT_MOUTH.value


class SkullRigidBodies(Enum):
    # TODO - go harder on the naming convention - https://www.sciencedirect.com/science/article/pii/S0169260721004545
    COMPOUND: CompoundRigidBodyABC = SkullRigidBody
    NOSE: SimpleRigidBodyABC = SkullNoseRigidBody
    BREGMA: SimpleRigidBodyABC = SkullBregmaRigidBody
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
