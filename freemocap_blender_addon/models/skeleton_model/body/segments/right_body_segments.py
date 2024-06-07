from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, RightArmKeypoints, \
    RightMittenHandKeypoints, RightLegKeypoints
from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import CompoundSegmentABC, \
    SimpleSegmentABC


# arm
class RightClavicleSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.CHEST_CENTER_T12
    child = RightArmKeypoints.RIGHT_SHOULDER


class RightUpperArmSegment(SimpleSegmentABC):
    parent = RightArmKeypoints.RIGHT_SHOULDER
    child = RightArmKeypoints.RIGHT_ELBOW


class RightForearmSegment(SimpleSegmentABC):
    parent = RightArmKeypoints.RIGHT_ELBOW
    child = RightArmKeypoints.RIGHT_WRIST


class RightWristIndexSegment(CompoundSegmentABC):
    parent = RightArmKeypoints.RIGHT_WRIST
    child = RightMittenHandKeypoints.RIGHT_INDEX_KNUCKLE


class RightWristPinkySegment(CompoundSegmentABC):
    parent = RightArmKeypoints.RIGHT_WRIST
    child = RightMittenHandKeypoints.RIGHT_PINKY_KNUCKLE


class RightThumbSegment(SimpleSegmentABC):
    parent = RightArmKeypoints.RIGHT_WRIST
    child = RightMittenHandKeypoints.RIGHT_THUMB_KNUCKLE


# leg
class RightPelvisSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.PELVIS_CENTER
    child = RightLegKeypoints.RIGHT_HIP


class RightThighSegment(SimpleSegmentABC):
    parent = RightLegKeypoints.RIGHT_HIP
    child = RightLegKeypoints.RIGHT_KNEE


class RightCalfSegment(SimpleSegmentABC):
    parent = RightLegKeypoints.RIGHT_KNEE
    child = RightLegKeypoints.RIGHT_ANKLE


class RightFootSegment(SimpleSegmentABC):
    parent = RightLegKeypoints.RIGHT_ANKLE
    child = RightLegKeypoints.RIGHT_HALLUX_TIP


class RightHeelSegment(SimpleSegmentABC):
    parent = RightLegKeypoints.RIGHT_ANKLE
    child = RightLegKeypoints.RIGHT_HALLUX_TIP


class RightBodySegments(Enum):
    RIGHT_CLAVICLE: SimpleSegmentABC = RightClavicleSegment
    RIGHT_UPPER_ARM: SimpleSegmentABC = RightUpperArmSegment
    RIGHT_FOREARM: SimpleSegmentABC = RightForearmSegment
    RIGHT_WRIST_INDEX: CompoundSegmentABC = RightWristIndexSegment
    RIGHT_WRIST_PINKY: CompoundSegmentABC = RightWristPinkySegment
    RIGHT_THUMB: SimpleSegmentABC = RightThumbSegment
    RIGHT_PELVIS: SimpleSegmentABC = RightPelvisSegment
    RIGHT_THIGH: SimpleSegmentABC = RightThighSegment
    RIGHT_CALF: SimpleSegmentABC = RightCalfSegment
    RIGHT_FOOT: SimpleSegmentABC = RightFootSegment
    RIGHT_HEEL: SimpleSegmentABC = RightHeelSegment


if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}"
                     for rb in list(RightBodySegments)]))
