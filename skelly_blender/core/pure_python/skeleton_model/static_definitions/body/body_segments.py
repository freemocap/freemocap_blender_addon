from skelly_blender.core.blender_stuff.blenderizers.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC, \
    CompoundSegmentABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints




class SkullNoseSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.SKULL_FORWARD_NOSE_TIP.name


class SkullTopSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.SKULL_TOP_BREGMA.name


class SkullRightEyeInnerSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.RIGHT_SKULL_EYE_INNER.name


class SkullRightEyeCenterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.RIGHT_SKULL_EYE_CENTER.name


class SkullRightEyeOuterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.RIGHT_SKULL_EYE_OUTER.name


class SkullRightEarTragusSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.RIGHT_SKULL_ACOUSTIC_MEATUS.name


class SkullRightMouthSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.RIGHT_SKULL_CANINE_TOOTH_TIP.name


class SkullLeftEyeInnerSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.LEFT_SKULL_EYE_INNER.name


class SkullLeftEyeCenterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.LEFT_SKULL_EYE_CENTER.name


class SkullLeftEyeOuterSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.LEFT_SKULL_EYE_OUTER.name


class SkullLeftEarTragusSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS.name


class SkullLeftMouthSegment(SimpleSegmentABC):
    parent = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    child = BodyKeypoints.LEFT_SKULL_CANINE_TOOTH_TIP.name


class CervicalSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.CERVICAL_SPINE_TOP_C1_AXIS.name
    child = BodyKeypoints.THORACIC_SPINE_TOP_T1.name



class ThoracicSpineSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_ORIGIN_T12.name
    child = BodyKeypoints.THORACIC_SPINE_TOP_T1.name


class PelvisLumbarSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_LUMBAR_ORIGIN.name
    child = BodyKeypoints.PELVIS_LUMBAR_TOP_L1.name

# Right Body
class RightClavicleSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_TOP_T1.name
    child = BodyKeypoints.RIGHT_SHOULDER.name


class RightUpperArmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_SHOULDER.name
    child = BodyKeypoints.RIGHT_ELBOW.name


class RightForearmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ELBOW.name
    child = BodyKeypoints.RIGHT_WRIST.name


class RightWristIndexSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_WRIST.name
    child = BodyKeypoints.RIGHT_INDEX_KNUCKLE.name


class RightWristPinkySegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_WRIST.name
    child = BodyKeypoints.RIGHT_PINKY_KNUCKLE.name


class RightWristThumbSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_WRIST.name
    child = BodyKeypoints.RIGHT_THUMB_KNUCKLE.name


# leg
class RightPelvisSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_LUMBAR_ORIGIN.name
    child = BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.name


class RightThighSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.name
    child = BodyKeypoints.RIGHT_KNEE.name


class RightCalfSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_KNEE.name
    child = BodyKeypoints.RIGHT_ANKLE.name


class RightFootFrontSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ANKLE.name
    child = BodyKeypoints.RIGHT_HALLUX_TIP.name


class RightHeelSegment(SimpleSegmentABC):
    parent = BodyKeypoints.RIGHT_ANKLE.name
    child = BodyKeypoints.RIGHT_HEEL.name


# Left Body

# arm
class LeftClavicleSegment(SimpleSegmentABC):
    parent = BodyKeypoints.THORACIC_SPINE_TOP_T1.name
    child = BodyKeypoints.LEFT_SHOULDER.name


class LeftUpperArmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_SHOULDER.name
    child = BodyKeypoints.LEFT_ELBOW.name


class LeftForearmSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ELBOW.name
    child = BodyKeypoints.LEFT_WRIST.name


class LeftWristIndexSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_WRIST.name
    child = BodyKeypoints.LEFT_INDEX_KNUCKLE.name


class LeftWristPinkySegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_WRIST.name
    child = BodyKeypoints.LEFT_PINKY_KNUCKLE.name


class LeftWristThumbSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_WRIST.name
    child = BodyKeypoints.LEFT_THUMB_KNUCKLE.name


# leg
class LeftPelvisSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_LUMBAR_ORIGIN.name
    child = BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.name


class LeftThighSegment(SimpleSegmentABC):
    parent = BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.name
    child = BodyKeypoints.LEFT_KNEE.name


class LeftCalfSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_KNEE.name
    child = BodyKeypoints.LEFT_ANKLE.name


class LeftFootFrontSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ANKLE.name
    child = BodyKeypoints.LEFT_HALLUX_TIP.name


class LeftHeelSegment(SimpleSegmentABC):
    parent = BodyKeypoints.LEFT_ANKLE.name
    child = BodyKeypoints.LEFT_HEEL.name

# Compound segments
class SkullCompoundSegment(CompoundSegmentABC):
    segments = [BodyKeypoints.SKULL_FORWARD_NOSE_TIP.name,
                BodyKeypoints.SKULL_TOP_BREGMA.name,
                BodyKeypoints.RIGHT_SKULL_EYE_INNER.name,
                BodyKeypoints.RIGHT_SKULL_EYE_CENTER.name,
                BodyKeypoints.RIGHT_SKULL_EYE_OUTER.name,
                BodyKeypoints.RIGHT_SKULL_ACOUSTIC_MEATUS.name,
                BodyKeypoints.RIGHT_SKULL_CANINE_TOOTH_TIP.name,
                BodyKeypoints.LEFT_SKULL_EYE_INNER.name,
                BodyKeypoints.LEFT_SKULL_EYE_CENTER.name,
                BodyKeypoints.LEFT_SKULL_EYE_OUTER.name,
                BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS.name,
                BodyKeypoints.LEFT_SKULL_CANINE_TOOTH_TIP.name]

    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    x_forward_reference = BodyKeypoints.SKULL_FORWARD_NOSE_TIP.name
    y_leftward_reference = BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS.name

class PelvisLumbarCompoundSegment(CompoundSegmentABC):
    segments = [BodyKeypoints.PELVIS_LUMBAR_TOP_L1.name,
                BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.name,
                BodyKeypoints.PELVIS_LUMBAR_LEFT_HIP_ACETABULUM.name]
    origin = BodyKeypoints.PELVIS_LUMBAR_ORIGIN.name
    z_up_reference = BodyKeypoints.PELVIS_LUMBAR_TOP_L1.name
    x_forward_reference = BodyKeypoints.PELVIS_LUMBAR_RIGHT_HIP_ACETABULUM.name


class BodySegments(BlenderizableEnum):
    SKULL: CompoundSegmentABC = SkullCompoundSegment
    PELVIS_LUMBAR: CompoundSegmentABC = PelvisLumbarCompoundSegment

    SKULL_NOSE: SimpleSegmentABC = SkullNoseSegment
    SKULL_TOP: SimpleSegmentABC = SkullTopSegment
    SKULL_RIGHT_EYE_INNER: SimpleSegmentABC = SkullRightEyeInnerSegment
    SKULL_RIGHT_EYE_CENTER: SimpleSegmentABC = SkullRightEyeCenterSegment
    SKULL_RIGHT_EYE_OUTER: SimpleSegmentABC = SkullRightEyeOuterSegment
    SKULL_RIGHT_EAR: SimpleSegmentABC = SkullRightEarTragusSegment
    SKULL_RIGHT_MOUTH: SimpleSegmentABC = SkullRightMouthSegment
    SKULL_LEFT_EYE_INNER: SimpleSegmentABC = SkullLeftEyeInnerSegment
    SKULL_LEFT_EYE_CENTER: SimpleSegmentABC = SkullLeftEyeCenterSegment
    SKULL_LEFT_EYE_OUTER: SimpleSegmentABC = SkullLeftEyeOuterSegment
    SKULL_LEFT_EAR: SimpleSegmentABC = SkullLeftEarTragusSegment
    SKULL_LEFT_MOUTH: SimpleSegmentABC = SkullLeftMouthSegment

    SPINE_CERVICAL: SimpleSegmentABC = CervicalSpineSegment
    SPINE_THORACIC: SimpleSegmentABC = ThoracicSpineSegment
    SPINE_SACRUM_LUMBAR: SimpleSegmentABC = PelvisLumbarSegment
    PELVIS_LEFT: SimpleSegmentABC = LeftPelvisSegment
    PELVIS_RIGHT: SimpleSegmentABC = RightPelvisSegment

    RIGHT_CLAVICLE: SimpleSegmentABC = RightClavicleSegment
    RIGHT_ARM_PROXIMAL: SimpleSegmentABC = RightUpperArmSegment
    RIGHT_ARM_DISTAL: SimpleSegmentABC = RightForearmSegment
    RIGHT_PALM_INDEX: SimpleSegmentABC = RightWristIndexSegment
    RIGHT_PALM_PINKY: SimpleSegmentABC = RightWristPinkySegment
    RIGHT_PALM_THUMB: SimpleSegmentABC = RightWristThumbSegment

    RIGHT_LEG_THIGH: SimpleSegmentABC = RightThighSegment
    RIGHT_LEG_CALF: SimpleSegmentABC = RightCalfSegment
    RIGHT_FOOT_FRONT: SimpleSegmentABC = RightFootFrontSegment
    RIGHT_FOOT_HEEL: SimpleSegmentABC = RightHeelSegment

    LEFT_CLAVICLE: SimpleSegmentABC = LeftClavicleSegment
    LEFT_ARM_PROXIMAL: SimpleSegmentABC = LeftUpperArmSegment
    LEFT_ARM_DISTAL: SimpleSegmentABC = LeftForearmSegment
    LEFT_PALM_INDEX: SimpleSegmentABC = LeftWristIndexSegment
    LEFT_PALM_PINKY: SimpleSegmentABC = LeftWristPinkySegment
    LEFT_PALM_THUMB: SimpleSegmentABC = LeftWristThumbSegment

    LEFT_LEG_THIGH: SimpleSegmentABC = LeftThighSegment
    LEFT_LEG_CALF: SimpleSegmentABC = LeftCalfSegment
    LEFT_FOOT_FRONT: SimpleSegmentABC = LeftFootFrontSegment
    LEFT_FOOT_HEEL: SimpleSegmentABC = LeftHeelSegment






