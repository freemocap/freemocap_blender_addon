from skelly_blender.core.blender_stuff.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints


class RightClavicleSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_TOP_T1
    child = BodyKeypoints.RIGHT_SHOULDER


class RightUpperArmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_SHOULDER
    child = BodyKeypoints.RIGHT_ELBOW


class RightForearmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ELBOW
    child = BodyKeypoints.RIGHT_WRIST


class RightWristIndexSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_WRIST
    child = BodyKeypoints.RIGHT_INDEX_KNUCKLE


class RightWristPinkySegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_WRIST
    child = BodyKeypoints.RIGHT_PINKY_KNUCKLE


class RightWristThumbSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_WRIST
    child = BodyKeypoints.RIGHT_THUMB_KNUCKLE


# leg
class RightPelvisSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_ORIGIN
    child = BodyKeypoints.RIGHT_PELVIS_HIP_ACETABULUM


class RightThighSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_PELVIS_HIP_ACETABULUM
    child = BodyKeypoints.RIGHT_KNEE


class RightCalfSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_KNEE
    child = BodyKeypoints.RIGHT_ANKLE


class RightFootSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ANKLE
    child = BodyKeypoints.RIGHT_HALLUX_TIP


class RightHeelSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ANKLE
    child = BodyKeypoints.RIGHT_HEEL


class RightBodySegments(BlenderizableEnum):
    RIGHT_CLAVICLE: SimpleSegmentABC = RightClavicleSegment
    RIGHT_UPPER_ARM: SimpleSegmentABC = RightUpperArmSegment
    RIGHT_FOREARM: SimpleSegmentABC = RightForearmSegment
    RIGHT_WRIST_INDEX: SimpleSegmentABC = RightWristIndexSegment
    RIGHT_WRIST_PINKY: SimpleSegmentABC = RightWristPinkySegment
    RIGHT_WRIST_THUMB: SimpleSegmentABC = RightWristThumbSegment
    RIGHT_PELVIS: SimpleSegmentABC = RightPelvisSegment
    RIGHT_THIGH: SimpleSegmentABC = RightThighSegment
    RIGHT_CALF: SimpleSegmentABC = RightCalfSegment
    RIGHT_FORE_FOOT: SimpleSegmentABC = RightFootSegment
    RIGHT_HEEL: SimpleSegmentABC = RightHeelSegment



if __name__ == "__main__":
    print("\n".join([f"{rb.name}: Parent - {rb.value.parent.name}, Child - {rb.value.child.name}"
                     for rb in list(RightBodySegments)]))
    print("Blenderized names:")
    print("\n".join([f"{value.blenderize()}" for key, value in RightBodySegments.__members__.items()])
          )
