from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import LinkageABC
from freemocap_blender_addon.models.skeleton_model.body.a_keypoints.right_body_keypoints import RightBodyKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightUpperArmSegment, \
    RightClavicleSegment, RightForearmSegment, RightPalmSegment, RightThumbSegment, RightPelvisSegment, \
    RightThighSegment, RightCalfSegment, RightFootSegment


class RightShoulderLinkage(LinkageABC):
    bodies = [RightClavicleSegment,
              RightUpperArmSegment]
    linked_keypoint = RightBodyKeypoints.RIGHT_SHOULDER.value


class RightElbowLinkage(LinkageABC):
    bodies = [RightUpperArmSegment,
              RightForearmSegment]
    linked_keypoint = RightBodyKeypoints.RIGHT_ELBOW.value


class RightWristLinkage(LinkageABC):
    bodies = [RightForearmSegment,
              RightPalmSegment,
              RightThumbSegment,
              ]
    linked_keypoint = RightBodyKeypoints.RIGHT_WRIST.value

class RightHipLinkage(LinkageABC):
    bodies = [RightPelvisSegment,
              RightThighSegment]
    linked_keypoint = RightBodyKeypoints.RIGHT_HIP.value

class RightKneeLinkage(LinkageABC):
    bodies = [RightThighSegment,
              RightCalfSegment]
    linked_keypoint = RightBodyKeypoints.RIGHT_KNEE.value

class RightAnkleLinkage(LinkageABC):
    bodies = [RightCalfSegment,
              RightFootSegment]
    linked_keypoint = RightBodyKeypoints.RIGHT_ANKLE.value