from skelly_blender.core.blender_stuff.blenderizers.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC, \
    CompoundSegmentABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints




class SkullNoseSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.SKULL_FORWARD_NOSE_TIP


class SkullTopSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    child = BodyKeypoints.SKULL_TOP_BREGMA


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


class CervicalSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.CERVICAL_SPINE_TOP_C1_AXIS
    child = BodyKeypoints.THORACIC_SPINE_TOP_T1



class ThoracicSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_ORIGIN_T12
    child = BodyKeypoints.THORACIC_SPINE_TOP_T1


class PelvisLumbarSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_ORIGIN
    child = BodyKeypoints.PELVIS_LUMBAR_TOP_L1

# Right Body
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


class RightFootFrontSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ANKLE
    child = BodyKeypoints.RIGHT_HALLUX_TIP


class RightHeelSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ANKLE
    child = BodyKeypoints.RIGHT_HEEL


# Left Body

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


class LeftFootFrontSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ANKLE
    child = BodyKeypoints.LEFT_HALLUX_TIP


class LeftHeelSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ANKLE
    child = BodyKeypoints.LEFT_HEEL

# Compound segments
class SkullSegment(CompoundSegmentABC):
    segments = [BodyKeypoints.SKULL_FORWARD_NOSE_TIP,
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

    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM
    positive_x = BodyKeypoints.SKULL_FORWARD_NOSE_TIP
    approximate_positive_y = BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS

class BodySegments(BlenderizableEnum):
    AXIAL_CERVICAL_SPINE: SimpleSegmentABC = CervicalSpineSegment
    AXIAL_THORACIC_SPINE: SimpleSegmentABC = ThoracicSpineSegment
    AXIAL_PELVIS_LUMBAR: SimpleSegmentABC = PelvisLumbarSegment
    AXIAL_PELVIS_LEFT: SimpleSegmentABC = LeftPelvisSegment
    AXIAL_PELVIS_RIGHT: SimpleSegmentABC = RightPelvisSegment

    RIGHT_ARM_CLAVICLE: SimpleSegmentABC = RightClavicleSegment
    RIGHT_ARM_UPPER: SimpleSegmentABC = RightUpperArmSegment
    RIGHT_ARM_FOREARM: SimpleSegmentABC = RightForearmSegment
    RIGHT_PALM_INDEX: SimpleSegmentABC = RightWristIndexSegment
    RIGHT_PALM_PINKY: SimpleSegmentABC = RightWristPinkySegment
    RIGHT_PALM_THUMB: SimpleSegmentABC = RightWristThumbSegment

    RIGHT_LEG_THIGH: SimpleSegmentABC = RightThighSegment
    RIGHT_LEG_CALF: SimpleSegmentABC = RightCalfSegment
    RIGHT_FOOT_FRONT: SimpleSegmentABC = RightFootFrontSegment
    RIGHT_FOOT_HEEL: SimpleSegmentABC = RightHeelSegment

    LEFT_ARM_CLAVICLE: SimpleSegmentABC = LeftClavicleSegment
    LEFT_ARM_UPPER: SimpleSegmentABC = LeftUpperArmSegment
    LEFT_ARM_FOREARM: SimpleSegmentABC = LeftForearmSegment
    LEFT_PALM_INDEX: SimpleSegmentABC = LeftWristIndexSegment
    LEFT_PALM_PINKY: SimpleSegmentABC = LeftWristPinkySegment
    LEFT_PALM_THUMB: SimpleSegmentABC = LeftWristThumbSegment

    LEFT_LEG_THIGH: SimpleSegmentABC = LeftThighSegment
    LEFT_LEG_CALF: SimpleSegmentABC = LeftCalfSegment
    LEFT_FOOT_FRONT: SimpleSegmentABC = LeftFootFrontSegment
    LEFT_FOOT_HEEL: SimpleSegmentABC = LeftHeelSegment






