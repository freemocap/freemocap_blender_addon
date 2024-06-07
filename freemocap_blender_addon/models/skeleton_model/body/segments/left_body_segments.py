from enum import Enum

from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import AxialSkeletonKeypoints, LeftArmKeypoints, \
    LeftMittenHandKeypoints, LeftLegKeypoints
from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import CompoundSegmentABC, \
    SimpleSegmentABC


# arm
class LeftClavicleSegment(SimpleSegmentABC):
    parent = AxialSkeletonKeypoints.CHEST_CENTER_T12
    child = LeftArmKeypoints.LEFT_SHOULDER


class LeftUpperArmSegment(SimpleSegmentABC):
    parent = LeftArmKeypoints.LEFT_SHOULDER
    child = LeftArmKeypoints.LEFT_ELBOW


class LeftForearmSegment(SimpleSegmentABC):
    parent = LeftArmKeypoints.LEFT_ELBOW
    child = LeftArmKeypoints.LEFT_WRIST


class LeftWristIndexSegment(CompoundSegmentABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_INDEX_KNUCKLE


class LeftWristPinkySegment(CompoundSegmentABC):
    parent = LeftArmKeypoints.LEFT_WRIST
    child = LeftMittenHandKeypoints.LEFT_PINKY_KNUCKLE


class LeftThumbSegment(SimpleSegmentABC):
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


class LeftFootSegment(SimpleSegmentABC):
    parent = LeftLegKeypoints.LEFT_ANKLE
    child = LeftLegKeypoints.LEFT_HALLUX_TIP


class LeftHeelSegment(SimpleSegmentABC):
    parent = LeftLegKeypoints.LEFT_ANKLE
    child = LeftLegKeypoints.LEFT_HALLUX_TIP


class LeftBodySegments(Enum):
    LEFT_CLAVICLE: SimpleSegmentABC = LeftClavicleSegment
    LEFT_UPPER_ARM: SimpleSegmentABC = LeftUpperArmSegment
    LEFT_FOREARM: SimpleSegmentABC = LeftForearmSegment
    LEFT_WRIST_INDEX: CompoundSegmentABC = LeftWristIndexSegment
    LEFT_WRIST_PINKY: CompoundSegmentABC = LeftWristPinkySegment
    LEFT_THUMB: SimpleSegmentABC = LeftThumbSegment
    LEFT_PELVIS: SimpleSegmentABC = LeftPelvisSegment
    LEFT_THIGH: SimpleSegmentABC = LeftThighSegment
    LEFT_CALF: SimpleSegmentABC = LeftCalfSegment
    LEFT_FOOT: SimpleSegmentABC = LeftFootSegment
    LEFT_HEEL: SimpleSegmentABC = LeftHeelSegment


if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}"
                     for rb in list(LeftBodySegments)]))
