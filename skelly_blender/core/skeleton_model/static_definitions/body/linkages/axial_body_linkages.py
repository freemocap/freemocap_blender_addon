from skelly_blender.core.skeleton_model.abstract_base_classes.linkage_abc import LinkageABC
from skelly_blender.core.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.skeleton_model.static_definitions.body.segments.axial_segments import AxialSegments
from skelly_blender.core.skeleton_model.static_definitions.body.segments.left_body_segments import LeftBodySegments
from skelly_blender.core.skeleton_model.static_definitions.body.segments.right_body_segments import RightBodySegments
from skelly_blender.core.skeleton_model.static_definitions.body.segments.skull_segments import SkullSegments


class SkullC1Linkage(LinkageABC):  # "Atlas" is another name for the first cervical vertebra (C1)
    parent = AxialSegments.CERVICAL_SPINE
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
    linked_keypoint = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM


class NeckC7Linkage(LinkageABC):
    parent = AxialSegments.THORACIC_SPINE
    children = [AxialSegments.CERVICAL_SPINE,
                RightBodySegments.RIGHT_CLAVICLE,
                LeftBodySegments.LEFT_CLAVICLE]
    linked_keypoint = BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7


class ChestT12Linkage(LinkageABC):
    parent = AxialSegments.PELVIS_LUMBAR
    children = [AxialSegments.PELVIS_LUMBAR,
                AxialSegments.THORACIC_SPINE]
    linked_keypoint = BodyKeypoints.THORACIC_SPINE_ORIGIN_T12
