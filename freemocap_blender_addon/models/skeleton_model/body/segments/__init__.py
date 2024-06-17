from enum import Enum
from typing import Type

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import combine_enums, LeftLegKeypoints, \
    LeftMittenHandKeypoints, LeftArmKeypoints, RightLegKeypoints, RightMittenHandKeypoints, RightArmKeypoints, \
    AxialSkeletonKeypoints
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_segments import SkullSegments
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.segments_abc import SegmentABC


class SegmentEnum(Enum):
    """An Enum that can hold different types of Segments."""

    def __new__(cls, value: Type[SegmentABC]):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


BodySegments = Enum('BodySegments', combine_enums(

    SkullSegments,
    AxialSkeletonKeypoints,

    # right
    RightArmKeypoints,
    RightMittenHandKeypoints,
    RightLegKeypoints,

    # left
    LeftArmKeypoints,
    LeftMittenHandKeypoints,
    LeftLegKeypoints,

))

# Example usage
if __name__ == "__main__":
    print("\n".join([f"{kp.name}: {kp.value}" for kp in list(BodySegments)]))
