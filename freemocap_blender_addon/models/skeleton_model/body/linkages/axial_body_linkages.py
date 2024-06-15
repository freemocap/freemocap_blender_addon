from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, SkullKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import AxialSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_segments import SkullSegments
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.linkage_abc import LinkageABC


class SkullC1Linkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    parent = AxialSegments.CERVICAL
    children = [SkullSegments.NOSE,
                SkullSegments.RIGHT_EYE_INNER,
                SkullSegments.RIGHT_EYE_CENTER,
                SkullSegments.RIGHT_EYE_OUTER,
                SkullSegments.RIGHT_EAR_TRAGUS,
                SkullSegments.RIGHT_MOUTH,
                SkullSegments.LEFT_EYE_INNER,
                SkullSegments.LEFT_EYE_CENTER,
                SkullSegments.LEFT_EYE_OUTER,
                SkullSegments.LEFT_EAR_TRAGUS,
                SkullSegments.LEFT_MOUTH]
    linked_keypoint = SkullKeypoints.SKULL_CENTER_ATLAS_C1


class NeckC7Linkage(LinkageABC):
    parent = AxialSegments.THORACIC
    children = [AxialSegments.CERVICAL,
                RightBodySegments.RIGHT_CLAVICLE,
                LeftBodySegments.LEFT_CLAVICLE]
    linked_keypoint = AxialSkeletonKeypoints.NECK_BASE_C7


class ChestT12Linkage(LinkageABC):
    parent = AxialSegments.LUMBAR
    children = [AxialSegments.LUMBAR,
                AxialSegments.THORACIC]
    linked_keypoint = AxialSkeletonKeypoints.CHEST_CENTER_T12
