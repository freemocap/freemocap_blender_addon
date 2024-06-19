from enum import Enum

from skelly_blender.core.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC, \
    CompoundSegmentABC

from skelly_blender.core.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.utility_classes.blenderizable_enum import BlenderizableEnum


class SkullSegment(CompoundSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    children = [BodyKeypoints.SKULL_FORWARD_NOSE_TIP,
                BodyKeypoints.SKULL_TOP_BREGMA,
                BodyKeypoints.RIGHT_SKULL_EYE_INNER,
                BodyKeypoints.RIGHT_SKULL_EYE_CENTER,
                BodyKeypoints.RIGHT_SKULL_EYE_OUTER,
                BodyKeypoints.RIGHT_SKULL_ACOUSTIC_MEATUS,
                BodyKeypoints.RIGHT_SKULL_CANINE_TOOTH_TIP,
                BodyKeypoints.LEFT_SKULL_EYE_INNER,
                BodyKeypoints.LEFT_SKULL_EYE_CENTER,
                BodyKeypoints.LEFT_SKULL_EYE_OUTER,
                BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS,
                BodyKeypoints.LEFT_SKULL_CANINE_TOOTH_TIP]

    shared_keypoint = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    positive_x = BodyKeypoints.SKULL_FORWARD_NOSE_TIP
    approximate_positive_y = BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS


class SkullNoseSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.SKULL_FORWARD_NOSE_TIP


# class SkullTopSegment(SimpleSegmentABC):
#     parent = BodyKeypoints.SKULL_CENTER_C1
#     child = BodyKeypoints.SKULL_TOP_BREGMA


class SkullRightEyeInnerSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.RIGHT_SKULL_EYE_INNER


class SkullRightEyeCenterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.RIGHT_SKULL_EYE_CENTER


class SkullRightEyeOuterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.RIGHT_SKULL_EYE_OUTER


class SkullRightEarTragusSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.RIGHT_SKULL_ACOUSTIC_MEATUS


class SkullRightMouthSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.RIGHT_SKULL_CANINE_TOOTH_TIP


class SkullLeftEyeInnerSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.LEFT_SKULL_EYE_INNER


class SkullLeftEyeCenterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.LEFT_SKULL_EYE_CENTER


class SkullLeftEyeOuterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.LEFT_SKULL_EYE_OUTER


class SkullLeftEarTragusSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS


class SkullLeftMouthSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.LEFT_SKULL_CANINE_TOOTH_TIP


class SkullSegments(BlenderizableEnum):
    # TODO - go harder on the naming convention - https://www.sciencedirect.com/science/article/pii/S0169260721004545
    # COMPOUND: CompoundSegmentABC = SkullSegment
    NOSE: SimpleSegmentABC = SkullNoseSegment
    # TOP: SimpleSegmentABC = SkullTopSegment
    RIGHT_EYE_INNER: SimpleSegmentABC = SkullRightEyeInnerSegment
    RIGHT_EYE_CENTER: SimpleSegmentABC = SkullRightEyeCenterSegment
    RIGHT_EYE_OUTER: SimpleSegmentABC = SkullRightEyeOuterSegment
    RIGHT_EAR_TRAGUS: SimpleSegmentABC = SkullRightEarTragusSegment
    RIGHT_MOUTH: SimpleSegmentABC = SkullRightMouthSegment
    LEFT_EYE_INNER: SimpleSegmentABC = SkullLeftEyeInnerSegment
    LEFT_EYE_CENTER: SimpleSegmentABC = SkullLeftEyeCenterSegment
    LEFT_EYE_OUTER: SimpleSegmentABC = SkullLeftEyeOuterSegment
    LEFT_EAR_TRAGUS: SimpleSegmentABC = SkullLeftEarTragusSegment
    LEFT_MOUTH: SimpleSegmentABC = SkullLeftMouthSegment


# Example usage
if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}" for rb in
                     list(SkullSegments)]))

    print("Blenderized Skull Segments:")
    print("\n".join([f"{key}: {value.blenderize()}" for key, value in SkullSegments.__members__.items()]))
