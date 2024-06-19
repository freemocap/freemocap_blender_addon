from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.blender_stuff.blenderizable_enum import BlenderizableEnum


# arm
class LeftClavicleSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_TOP_T1
    child = BodyKeypoints.LEFT_SHOULDER


class LeftUpperArmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_SHOULDER
    child = BodyKeypoints.LEFT_ELBOW


class LeftForearmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ELBOW
    child = BodyKeypoints.LEFT_WRIST


class LeftWristIndexSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_WRIST
    child = BodyKeypoints.LEFT_INDEX_KNUCKLE


class LeftWristPinkySegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_WRIST
    child = BodyKeypoints.LEFT_PINKY_KNUCKLE


class LeftWristThumbSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_WRIST
    child = BodyKeypoints.LEFT_THUMB_KNUCKLE


# leg
class LeftPelvisSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_ORIGIN
    child = BodyKeypoints.LEFT_PELVIS_HIP_ACETABULUM


class LeftThighSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_PELVIS_HIP_ACETABULUM
    child = BodyKeypoints.LEFT_KNEE


class LeftCalfSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_KNEE
    child = BodyKeypoints.LEFT_ANKLE


class LeftForeFootSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ANKLE
    child = BodyKeypoints.LEFT_HALLUX_TIP


class LeftHeelSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ANKLE
    child = BodyKeypoints.LEFT_HEEL


class LeftBodySegments(BlenderizableEnum):
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


if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}"
                     for rb in list(LeftBodySegments)]))

    print("Blenderized names:")
    print("\n".join([f"{key}: {value.blenderize()}" for key, value in LeftBodySegments.__members__.items()]))
