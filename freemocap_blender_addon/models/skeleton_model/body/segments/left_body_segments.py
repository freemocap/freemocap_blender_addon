from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, LeftArmKeypoints, \
    LeftMittenHandKeypoints, LeftLegKeypoints
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.segments_abc import SimpleSegmentABC
from freemocap_blender_addon.utilities.blender_utilities.blenderize_name import blenderize_name


# arm
class LeftClavicleSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.CERVICAL_SPINE_ORIGIN_C7
    child = LeftArmKeypoints.LEFT_SHOULDER


class LeftUpperArmSegment(SimpleSegmentABC):
    parent = LeftArmKeypoints.LEFT_SHOULDER
    child = LeftArmKeypoints.LEFT_ELBOW


class LeftForearmSegment(SimpleSegmentABC):
    parent = LeftArmKeypoints.LEFT_ELBOW
    child = LeftArmKeypoints.LEFT_WRIST


class LeftWristIndexSegment(SimpleSegmentABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_INDEX_KNUCKLE


class LeftWristPinkySegment(SimpleSegmentABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_PINKY_KNUCKLE


class LeftWristThumbSegment(SimpleSegmentABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_THUMB_KNUCKLE


# leg
class LeftPelvisSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.PELVIS_CENTER
    child = LeftLegKeypoints.LEFT_HIP


class LeftThighSegment(SimpleSegmentABC):
    parent = LeftLegKeypoints.LEFT_HIP
    child = LeftLegKeypoints.LEFT_KNEE


class LeftCalfSegment(SimpleSegmentABC):
    parent = LeftLegKeypoints.LEFT_KNEE
    child = LeftLegKeypoints.LEFT_ANKLE


class LeftForeFootSegment(SimpleSegmentABC):
    parent = LeftLegKeypoints.LEFT_ANKLE
    child = LeftLegKeypoints.LEFT_HALLUX_TIP


class LeftHeelSegment(SimpleSegmentABC):
    parent = LeftLegKeypoints.LEFT_ANKLE
    child = LeftLegKeypoints.LEFT_HEEL


class LeftBodySegments(Enum):
    LEFT_CLAVICLE: SimpleSegmentABC = LeftClavicleSegment
    LEFT_UPPER_ARM: SimpleSegmentABC = LeftUpperArmSegment
    LEFT_FOREARM: SimpleSegmentABC = LeftForearmSegment
    LEFT_WRIST_INDEX: SimpleSegmentABC = LeftWristIndexSegment
    LEFT_WRIST_PINKY: SimpleSegmentABC = LeftWristPinkySegment
    LEFT_WRIST_THUMB: SimpleSegmentABC = LeftWristThumbSegment
    LEFT_PELVIS: SimpleSegmentABC = LeftPelvisSegment
    LEFT_THIGH: SimpleSegmentABC = LeftThighSegment
    LEFT_CALF: SimpleSegmentABC = LeftCalfSegment
    LEFT_FORE_FOOT: SimpleSegmentABC = LeftForeFootSegment
    LEFT_HEEL: SimpleSegmentABC = LeftHeelSegment


BlenderizedLeftBodySegments = Enum("BlenderizedLeftBodySegments",
                                   {name: blenderize_name(name) for name in list(LeftBodySegments.__members__.keys())})

if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}"
                     for rb in list(LeftBodySegments)]))

    print("Blenderized names:")
    print("\n".join([f"{rb.name}: {rb.value}" for rb in list(BlenderizedLeftBodySegments)]))
