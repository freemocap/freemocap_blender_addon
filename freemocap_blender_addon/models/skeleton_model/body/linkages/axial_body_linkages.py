from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, SkullKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import CervicalSegment, \
    LumbarSegment, ThoracicSegment
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftClavicleSegment, \
    LeftPelvisSegment
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightClavicleSegment, \
    RightPelvisSegment
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_rigid_segments import SkullSegment
from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import LinkageABC


class SkullC1Linkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    bodies = [CervicalSegment, SkullSegment]
    linked_keypoint = SkullKeypoints.SKULL_CENTER_C1


class NeckC7Linkage(LinkageABC):
    bodies = [CervicalSegment,
              ThoracicSegment,
              RightClavicleSegment,
              LeftClavicleSegment
              ]
    linked_keypoint = AxialSkeletonKeypoints.NECK_BASE_C7


class ChestT12Linkage(LinkageABC):
    bodies = [LumbarSegment, ThoracicSegment]
    linked_keypoint = AxialSkeletonKeypoints.CHEST_CENTER_T12


class PelvisSacrumLinkage(LinkageABC):
    """
    Note - this is a 'fixed' linkage, meaning the distance between all keypoints stays fixed.
    It really should be a CompoundSegment, but we don't have sufficient geometry to define it because
    the outer keypoints are linked via a virtual marker defined by keypoints within the linkage
    """
    bodies = [LumbarSegment,
              RightPelvisSegment,
              LeftPelvisSegment,
              ]
    linked_keypoint = AxialSkeletonKeypoints.PELVIS_CENTER
