from skelly_blender.core.blender_stuff.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints


class CervicalSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.CERVICAL_SPINE_TOP_C1_AXIS
    child = BodyKeypoints.THORACIC_SPINE_TOP_T1




class ThoracicSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_ORIGIN_T12
    child = BodyKeypoints.THORACIC_SPINE_TOP_T1


class PelvisLumbarSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_ORIGIN
    child = BodyKeypoints.PELVIS_LUMBAR_TOP_L1


class AxialSegments(BlenderizableEnum):
    CERVICAL_SPINE: SimpleSegmentABC = CervicalSpineSegment
    THORACIC_SPINE: SimpleSegmentABC = ThoracicSpineSegment
    PELVIS_LUMBAR: SimpleSegmentABC = PelvisLumbarSegment




if __name__ == "__main__":
    print("\n".join(
        [f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in list(AxialSegments)]))

    print("Blenderized names:")
    print("\n".join([value.blenderize() for value in AxialSegments.__members__.values()]))
