from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import BodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftBodySegments
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.linkage_abc import LinkageABC


class LeftShoulderLinkage(LinkageABC):
    parent = LeftBodySegments.LEFT_CLAVICLE
    children = [LeftBodySegments.LEFT_CLAVICLE,
                LeftBodySegments.LEFT_UPPER_ARM]
    linked_keypoint = BodyKeypoints.LEFT_SHOULDER


class LeftElbowLinkage(LinkageABC):
    parent = LeftBodySegments.LEFT_UPPER_ARM
    children = [LeftBodySegments.LEFT_UPPER_ARM,
                LeftBodySegments.LEFT_FOREARM]
    linked_keypoint = BodyKeypoints.LEFT_ELBOW.value


class LeftWristLinkage(LinkageABC):
    parent = LeftBodySegments.LEFT_FOREARM
    children = [LeftBodySegments.LEFT_FOREARM,
                LeftBodySegments.LEFT_WRIST_THUMB,
                LeftBodySegments.LEFT_WRIST_PINKY,
                LeftBodySegments.LEFT_WRIST_INDEX]

    linked_keypoint = BodyKeypoints.LEFT_WRIST


class LeftHipLinkage(LinkageABC):
    parent = LeftBodySegments.LEFT_PELVIS
    children = [LeftBodySegments.LEFT_PELVIS,
                LeftBodySegments.LEFT_THIGH]
    linked_keypoint = BodyKeypoints.LEFT_HIP


class LeftKneeLinkage(LinkageABC):
    parent = LeftBodySegments.LEFT_THIGH
    children = [LeftBodySegments.LEFT_THIGH,
                LeftBodySegments.LEFT_CALF]
    linked_keypoint = BodyKeypoints.LEFT_KNEE


class LeftAnkleLinkage(LinkageABC):
    parent = LeftBodySegments.LEFT_CALF
    children = [LeftBodySegments.LEFT_CALF,
                LeftBodySegments.LEFT_HEEL,
                LeftBodySegments.LEFT_FORE_FOOT]
    linked_keypoint = BodyKeypoints.LEFT_ANKLE.value
