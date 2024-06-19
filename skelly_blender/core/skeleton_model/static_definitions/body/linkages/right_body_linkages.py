from skelly_blender.core.skeleton_model.abstract_base_classes.linkage_abc import LinkageABC
from skelly_blender.core.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.skeleton_model.static_definitions.body.segments.right_body_segments import RightBodySegments


class RightShoulderLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_CLAVICLE
    children = [RightBodySegments.RIGHT_CLAVICLE,
                RightBodySegments.RIGHT_UPPER_ARM]
    linked_keypoint = BodyKeypoints.RIGHT_SHOULDER


class RightElbowLinkage(LinkageABC):
    parent = RightBodySegments.RIGHT_UPPER_ARM
    children = [RightBodySegments.RIGHT_UPPER_ARM,
                RightBodySegments.RIGHT_FOREARM]
    linked_keypoint = BodyKeypoints.RIGHT_ELBOW


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
    linked_keypoint = BodyKeypoints.RIGHT_PELVIS_HIP_ACETABULUM


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
    linked_keypoint = BodyKeypoints.RIGHT_ANKLE
