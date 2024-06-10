from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, SkullKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import CervicalSegment, \
    LumbarSegment, ThoracicSegment
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftClavicleSegment
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightClavicleSegment
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_segments import SkullLeftMouthSegment, SkullLeftEarTragusSegment, SkullLeftEyeOuterSegment, SkullLeftEyeCenterSegment, \
    SkullLeftEyeInnerSegment, SkullRightMouthSegment, SkullRightEarTragusSegment, SkullRightEyeOuterSegment, \
    SkullRightEyeCenterSegment, SkullRightEyeInnerSegment, SkullNoseSegment
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.linkage_abc import LinkageABC


class SkullC1Linkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    parent = CervicalSegment
    children = [SkullNoseSegment,
                # SkullTopSegment,
                SkullRightEyeInnerSegment,
                SkullRightEyeCenterSegment,
                SkullRightEyeOuterSegment,
                SkullRightEarTragusSegment,
                SkullRightMouthSegment,
                SkullLeftEyeInnerSegment,
                SkullLeftEyeCenterSegment,
                SkullLeftEyeOuterSegment,
                SkullLeftEarTragusSegment,
                SkullLeftMouthSegment]
    linked_keypoint = SkullKeypoints.SKULL_CENTER_ATLAS_C1


class NeckC7Linkage(LinkageABC):
    parent = ThoracicSegment
    children = [CervicalSegment,
                RightClavicleSegment,
                LeftClavicleSegment
                ]
    linked_keypoint = AxialSkeletonKeypoints.NECK_BASE_C7


class ChestT12Linkage(LinkageABC):
    parent = LumbarSegment
    children = [LumbarSegment, ThoracicSegment]
    linked_keypoint = AxialSkeletonKeypoints.CHEST_CENTER_T12
