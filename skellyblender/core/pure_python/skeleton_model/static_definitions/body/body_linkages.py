from skellyblender.core.pure_python.custom_types.base_enums import LinkageEnum
from skellyblender.core.pure_python.skeleton_model.abstract_base_classes.linkage_abc import LinkageABC
from skellyblender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skellyblender.core.pure_python.skeleton_model.static_definitions.body.body_segments import BodySegments


class SkullC1Linkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    parent = BodySegments.SPINE_CERVICAL
    children = [BodySegments.SKULL_NOSE,
                BodySegments.SKULL_RIGHT_EYE_INNER,
                BodySegments.SKULL_RIGHT_EYE_CENTER,
                BodySegments.SKULL_RIGHT_EYE_OUTER,
                BodySegments.SKULL_RIGHT_EAR,
                BodySegments.SKULL_RIGHT_MOUTH,
                BodySegments.SKULL_LEFT_EYE_INNER,
                BodySegments.SKULL_LEFT_EYE_CENTER,
                BodySegments.SKULL_LEFT_EYE_OUTER,
                BodySegments.SKULL_LEFT_EAR,
                BodySegments.SKULL_LEFT_MOUTH]
    linked_keypoint = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM


class NeckC7Linkage(LinkageABC):
    parent = BodySegments.SPINE_THORACIC
    children = [BodySegments.SPINE_CERVICAL,
                BodySegments.RIGHT_CLAVICLE,
                BodySegments.LEFT_CLAVICLE]
    linked_keypoint = BodyKeypoints.SPINE_CERVICAL_ORIGIN_C7


class ChestT12Linkage(LinkageABC):
    parent = BodySegments.SPINE_SACRUM_LUMBAR
    children = [BodySegments.SPINE_THORACIC]
    linked_keypoint = BodyKeypoints.SPINE_THORACIC_ORIGIN_T12


class RightShoulderLinkage(LinkageABC):
    parent = BodySegments.RIGHT_CLAVICLE
    children = [BodySegments.RIGHT_ARM_PROXIMAL]
    linked_keypoint = BodyKeypoints.RIGHT_SHOULDER


class RightElbowLinkage(LinkageABC):
    parent = BodySegments.RIGHT_ARM_PROXIMAL
    children = [BodySegments.RIGHT_ARM_DISTAL]
    linked_keypoint = BodyKeypoints.RIGHT_ELBOW


class RightWristLinkage(LinkageABC):
    parent = BodySegments.RIGHT_ARM_DISTAL
    children = [BodySegments.RIGHT_PALM_THUMB,
                BodySegments.RIGHT_PALM_PINKY,
                BodySegments.RIGHT_PALM_INDEX]

    linked_keypoint = BodyKeypoints.RIGHT_WRIST


class RightHipLinkage(LinkageABC):
    parent = BodySegments.PELVIS_RIGHT
    children = [BodySegments.RIGHT_LEG_THIGH]
    linked_keypoint = BodyKeypoints.PELVIS_LEFT_HIP_ACETABULUM


class RightKneeLinkage(LinkageABC):
    parent = BodySegments.RIGHT_LEG_THIGH
    children = [BodySegments.RIGHT_LEG_CALF]
    linked_keypoint = BodyKeypoints.RIGHT_KNEE


class RightAnkleLinkage(LinkageABC):
    parent = BodySegments.RIGHT_LEG_CALF
    children = [BodySegments.RIGHT_FOOT_HEEL,
                BodySegments.RIGHT_FOOT_FRONT]
    linked_keypoint = BodyKeypoints.RIGHT_ANKLE

class LeftShoulderLinkage(LinkageABC):
    parent = BodySegments.LEFT_CLAVICLE
    children = [BodySegments.LEFT_ARM_PROXIMAL]
    linked_keypoint = BodyKeypoints.LEFT_SHOULDER


class LeftElbowLinkage(LinkageABC):
    parent = BodySegments.LEFT_ARM_PROXIMAL
    children = [BodySegments.LEFT_ARM_DISTAL]
    linked_keypoint = BodyKeypoints.LEFT_ELBOW


class LeftWristLinkage(LinkageABC):
    parent = BodySegments.LEFT_ARM_DISTAL
    children = [BodySegments.LEFT_PALM_THUMB,
                BodySegments.LEFT_PALM_PINKY,
                BodySegments.LEFT_PALM_INDEX]

    linked_keypoint = BodyKeypoints.LEFT_WRIST


class LeftHipLinkage(LinkageABC):
    parent = BodySegments.PELVIS_LEFT
    children = [BodySegments.LEFT_LEG_THIGH]
    linked_keypoint = BodyKeypoints.PELVIS_LEFT_HIP_ACETABULUM


class LeftKneeLinkage(LinkageABC):
    parent = BodySegments.LEFT_LEG_THIGH
    children = [BodySegments.LEFT_LEG_CALF]
    linked_keypoint = BodyKeypoints.LEFT_KNEE


class LeftAnkleLinkage(LinkageABC):
    parent = BodySegments.LEFT_LEG_CALF
    children = [BodySegments.LEFT_FOOT_HEEL,
                BodySegments.LEFT_FOOT_FRONT]
    linked_keypoint = BodyKeypoints.LEFT_ANKLE





class BodyLinkages(LinkageEnum):
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
