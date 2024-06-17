from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import BodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightBodySegments
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.linkage_abc import LinkageABC


class RightShoulderLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_CLAVICLE
    children = [RightBodySegments.RIGHT_CLAVICLE,
                RightBodySegments.RIGHT_UPPER_ARM]
    linked_keypoint = BodyKeypoints.RIGHT_SHOULDER


class RightElbowLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_UPPER_ARM
    children = [RightBodySegments.RIGHT_UPPER_ARM,
                RightBodySegments.RIGHT_FOREARM]
    linked_keypoint = BodyKeypoints.RIGHT_ELBOW.value


class RightWristLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_FOREARM
    children = [RightBodySegments.RIGHT_FOREARM,
                RightBodySegments.RIGHT_WRIST_THUMB,
                RightBodySegments.RIGHT_WRIST_PINKY,
                RightBodySegments.RIGHT_WRIST_INDEX]

    linked_keypoint = BodyKeypoints.RIGHT_WRIST


class RightHipLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_PELVIS
    children = [RightBodySegments.RIGHT_PELVIS,
                RightBodySegments.RIGHT_THIGH]
    linked_keypoint = BodyKeypoints.RIGHT_HIP


class RightKneeLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_THIGH
    children = [RightBodySegments.RIGHT_THIGH,
                RightBodySegments.RIGHT_CALF]
    linked_keypoint = BodyKeypoints.RIGHT_KNEE


class RightAnkleLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_CALF
    children = [RightBodySegments.RIGHT_CALF,
                RightBodySegments.RIGHT_HEEL,
                RightBodySegments.RIGHT_FORE_FOOT]
    linked_keypoint = BodyKeypoints.RIGHT_ANKLE.value
