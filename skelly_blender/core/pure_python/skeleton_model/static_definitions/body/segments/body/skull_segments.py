from skelly_blender.core.blender_stuff.blenderizers.blenderizable_enum import BlenderizableEnum

from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC, \
    CompoundSegmentABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints



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
