from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import BodyKeypoints
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.segments_abc import SimpleSegmentABC
from freemocap_blender_addon.utilities.blender_utilities.blenderize_name import blenderize_name


class CervicalSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.CERVICAL_SPINE_TOP_C1_AXIS
    child = BodyKeypoints.CERVICAL_SPINE_ORIGIN_C7


class ThoracicSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_ORIGIN_T12
    child = BodyKeypoints.THORACIC_SPINE_TOP_T1


class LumbarSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_ORIGIN
    child = BodyKeypoints.LUMBAR_SPINE_TOP_L1


class AxialSegments(Enum):
    CERVICAL_SPINE: SimpleSegmentABC = CervicalSpineSegment
    THORACIC_SPINE: SimpleSegmentABC = ThoracicSpineSegment
    LUMBAR_SPINE: SimpleSegmentABC = LumbarSpineSegment


BlenderizedAxialSegments = Enum("BlenderizedAxialSegments",
                                {name: blenderize_name(name) for name in list(AxialSegments.__members__.keys())})

if __name__ == "__main__":
    print("\n".join(
        [f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in list(AxialSegments)]))

    print("Blenderized names:")
    print("\n".join([f"{rb.name}: {rb.value}" for rb in list(BlenderizedAxialSegments)]))
