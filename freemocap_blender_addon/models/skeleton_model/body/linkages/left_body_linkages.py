from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import LinkageABC
from freemocap_blender_addon.models.skeleton_model.body.a_keypoints.left_body_keypoints import LeftBodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftThumbSegment, \
    LeftClavicleSegment, LeftUpperArmSegment, LeftForearmSegment, LeftPalmSegment, LeftFootSegment, \
    LeftThighSegment, LeftPelvisSegment, LeftCalfSegment


class LeftShoulderLinkage(LinkageABC):
    bodies = [LeftClavicleSegment,
              LeftUpperArmSegment]
    linked_keypoint = LeftBodyKeypoints.LEFT_SHOULDER.value


class LeftElbowLinkage(LinkageABC):
    bodies = [LeftUpperArmSegment,
              LeftForearmSegment]
    linked_keypoint = LeftBodyKeypoints.LEFT_ELBOW.value


class LeftWristLinkage(LinkageABC):
    bodies = [LeftForearmSegment,
              LeftPalmSegment,
              LeftThumbSegment,
              ]
    linked_keypoint = LeftBodyKeypoints.LEFT_WRIST.value


class LeftHipLinkage(LinkageABC):
    bodies = [LeftPelvisSegment,
              LeftThighSegment]
    linked_keypoint = LeftBodyKeypoints.LEFT_HIP.value


class LeftKneeLinkage(LinkageABC):
    bodies = [LeftThighSegment,
              LeftCalfSegment]
    linked_keypoint = LeftBodyKeypoints.LEFT_KNEE.value


class LeftAnkleLinkage(LinkageABC):
    bodies = [LeftCalfSegment,
              LeftFootSegment]
    linked_keypoint = LeftBodyKeypoints.LEFT_ANKLE.value
