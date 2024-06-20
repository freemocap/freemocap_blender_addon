from skelly_blender.core.blender_stuff.blenderizers.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.linkage_abc import LinkageABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_segments import BodySegments


class SkullC1Linkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    parent = BodySegments.SPINE_CERVICAL.value
    children = [BodySegments.SKULL_NOSE.value,
                BodySegments.SKULL_RIGHT_EYE_INNER.value,
                BodySegments.SKULL_RIGHT_EYE_CENTER.value,
                BodySegments.SKULL_RIGHT_EYE_OUTER.value,
                BodySegments.SKULL_RIGHT_EAR.value,
                BodySegments.SKULL_RIGHT_MOUTH.value,
                BodySegments.SKULL_LEFT_EYE_INNER.value,
                BodySegments.SKULL_LEFT_EYE_CENTER.value,
                BodySegments.SKULL_LEFT_EYE_OUTER.value,
                BodySegments.SKULL_LEFT_EAR.value,
                BodySegments.SKULL_LEFT_MOUTH.value,
                BodySegments.SKULL.value]
    linked_keypoint = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.value


class NeckC7Linkage(LinkageABC):
    parent = BodySegments.SPINE_THORACIC.value
    children = [BodySegments.SPINE_CERVICAL.value,
                BodySegments.RIGHT_CLAVICLE.value,
                BodySegments.LEFT_CLAVICLE.value]
    linked_keypoint = BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7.value


class ChestT12Linkage(LinkageABC):
    parent = BodySegments.PELVIS_LUMBAR.value
    children = [BodySegments.SPINE_THORACIC.value]
    linked_keypoint = BodyKeypoints.THORACIC_SPINE_ORIGIN_T12.value


class RightShoulderLinkage(LinkageABC):
    parent = BodySegments.RIGHT_CLAVICLE.value
    children = [BodySegments.RIGHT_ARM_PROXIMAL.value]
    linked_keypoint = BodyKeypoints.RIGHT_SHOULDER.value


class RightElbowLinkage(LinkageABC):
    parent = BodySegments.RIGHT_ARM_PROXIMAL.value
    children = [BodySegments.RIGHT_ARM_DISTAL.value]
    linked_keypoint = BodyKeypoints.RIGHT_ELBOW.value


class RightWristLinkage(LinkageABC):
    parent = BodySegments.RIGHT_ARM_DISTAL.value
    children = [BodySegments.RIGHT_PALM_THUMB.value,
                BodySegments.RIGHT_PALM_PINKY.value,
                BodySegments.RIGHT_PALM_INDEX.value]

    linked_keypoint = BodyKeypoints.RIGHT_WRIST.value


class RightHipLinkage(LinkageABC):
    parent = BodySegments.PELVIS_LEFT.value
    children = [BodySegments.RIGHT_LEG_THIGH.value]
    linked_keypoint = BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.value


class RightKneeLinkage(LinkageABC):
    parent = BodySegments.RIGHT_LEG_THIGH.value
    children = [BodySegments.RIGHT_LEG_CALF.value]
    linked_keypoint = BodyKeypoints.RIGHT_KNEE.value


class RightAnkleLinkage(LinkageABC):
    parent = BodySegments.RIGHT_LEG_CALF.value
    children = [BodySegments.RIGHT_FOOT_HEEL.value,
                BodySegments.RIGHT_FOOT_FRONT.value]
    linked_keypoint = BodyKeypoints.RIGHT_ANKLE.value

class LeftShoulderLinkage(LinkageABC):
    parent = BodySegments.LEFT_CLAVICLE.value
    children = [BodySegments.LEFT_ARM_PROXIMAL.value]
    linked_keypoint = BodyKeypoints.LEFT_SHOULDER.value


class LeftElbowLinkage(LinkageABC):
    parent = BodySegments.LEFT_ARM_PROXIMAL.value
    children = [BodySegments.LEFT_ARM_DISTAL.value]
    linked_keypoint = BodyKeypoints.LEFT_ELBOW.value


class LeftWristLinkage(LinkageABC):
    parent = BodySegments.LEFT_ARM_DISTAL.value
    children = [BodySegments.LEFT_PALM_THUMB.value,
                BodySegments.LEFT_PALM_PINKY.value,
                BodySegments.LEFT_PALM_INDEX.value]

    linked_keypoint = BodyKeypoints.LEFT_WRIST.value


class LeftHipLinkage(LinkageABC):
    parent = BodySegments.PELVIS_LEFT.value
    children = [BodySegments.LEFT_LEG_THIGH.value]
    linked_keypoint = BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.value


class LeftKneeLinkage(LinkageABC):
    parent = BodySegments.LEFT_LEG_THIGH.value
    children = [BodySegments.LEFT_LEG_CALF.value]
    linked_keypoint = BodyKeypoints.LEFT_KNEE.value


class LeftAnkleLinkage(LinkageABC):
    parent = BodySegments.LEFT_LEG_CALF.value
    children = [BodySegments.LEFT_FOOT_HEEL.value,
                BodySegments.LEFT_FOOT_FRONT.value]
    linked_keypoint = BodyKeypoints.LEFT_ANKLE.value





class BodyLinkages(BlenderizableEnum):
    SKULL_C1: LinkageABC = SkullC1Linkage
    NECK_C7: LinkageABC = NeckC7Linkage
    CHEST_T12: LinkageABC = ChestT12Linkage

    RIGHT_SHOULDER: LinkageABC = RightShoulderLinkage
    RIGHT_ELBOW: LinkageABC = RightElbowLinkage
    RIGHT_WRIST: LinkageABC = RightWristLinkage

    RIGHT_HIP: LinkageABC = RightHipLinkage
    RIGHT_KNEE: LinkageABC = RightKneeLinkage
    RIGHT_ANKLE: LinkageABC = RightAnkleLinkage

    LEFT_SHOULDER: LinkageABC = LeftShoulderLinkage
    LEFT_ELBOW: LinkageABC = LeftElbowLinkage
    LEFT_WRIST: LinkageABC = LeftWristLinkage

    LEFT_HIP: LinkageABC = LeftHipLinkage
    LEFT_KNEE: LinkageABC = LeftKneeLinkage
    LEFT_ANKLE: LinkageABC = LeftAnkleLinkage
