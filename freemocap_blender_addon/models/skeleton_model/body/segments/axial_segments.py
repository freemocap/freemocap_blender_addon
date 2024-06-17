from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, SkullKeypoints
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.segments_abc import SimpleSegmentABC
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name


class CervicalSpineSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.NECK_BASE_C7
    child = SkullKeypoints.SKULL_CENTER_ATLAS_C1


class ThoracicSpineSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.CHEST_CENTER_T12
    child = AxialSkeletonKeypoints.NECK_BASE_C7


class LumbarSpineSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.PELVIS_CENTER
    child = AxialSkeletonKeypoints.CHEST_CENTER_T12


class AxialSegments(Enum):
    CERVICAL_SPINE: SimpleSegmentABC = CervicalSpineSegment
    THORACIC_SPINE: SimpleSegmentABC = ThoracicSpineSegment
    LUMBAR_SPINE: SimpleSegmentABC = LumbarSpineSegment

BlenderizedAxialSegments = Enum("BlenderizedAxialSegments", {name: blenderize_name(name) for name in list(AxialSegments.__members__.keys())})

if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in list(AxialSegments)]))

    print("Blenderized names:")
    print("\n".join([f"{rb.name}: {rb.value}" for rb in list(BlenderizedAxialSegments)]))
