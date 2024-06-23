from skelly_blender.core.pure_python.custom_types.base_enums import SegmentEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC, \
    CompoundSegmentABC
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints


class SkullNoseSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.SKULL_FORWARD_NOSE_TIP.name


class SkullTopSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.SKULL_TOP_BREGMA.name


class SkullRightEyeInnerSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.RIGHT_SKULL_EYE_INNER.name


class SkullRightEyeCenterSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.RIGHT_SKULL_EYE_CENTER.name


class SkullRightEyeOuterSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.RIGHT_SKULL_EYE_OUTER.name


class SkullRightEarTragusSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.RIGHT_SKULL_ACOUSTIC_MEATUS.name


class SkullRightMouthSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.RIGHT_SKULL_CANINE_TOOTH_TIP.name


class SkullLeftEyeInnerSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.LEFT_SKULL_EYE_INNER.name


class SkullLeftEyeCenterSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.LEFT_SKULL_EYE_CENTER.name


class SkullLeftEyeOuterSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.LEFT_SKULL_EYE_OUTER.name


class SkullLeftEarTragusSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS.name


class SkullLeftMouthSegment(SimpleSegmentABC):
    origin = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name
    z_axis_reference = BodyKeypoints.LEFT_SKULL_CANINE_TOOTH_TIP.name


class CervicalSpineSegment(SimpleSegmentABC):
    origin = BodyKeypoints.CERVICAL_SPINE_TOP_C1_AXIS.name
    z_axis_reference = BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name


class ThoracicSpineSegment(SimpleSegmentABC):
    origin = BodyKeypoints.THORACIC_SPINE_ORIGIN_T12.name
    z_axis_reference = BodyKeypoints.THORACIC_SPINE_TOP_T1.name


class SpineSacrumLumbar(SimpleSegmentABC):
    origin = BodyKeypoints.PELVIS_SPINE_SACRUM_ORIGIN.name
    z_axis_reference = BodyKeypoints.SPINE_LUMBAR_TOP_L1.name


# Right Body
class RightClavicleSegment(SimpleSegmentABC):
    origin = BodyKeypoints.THORACIC_SPINE_TOP_T1.name
    z_axis_reference = BodyKeypoints.RIGHT_SHOULDER.name


class RightUpperArmSegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_SHOULDER.name
    z_axis_reference = BodyKeypoints.RIGHT_ELBOW.name


class RightForearmSegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_ELBOW.name
    z_axis_reference = BodyKeypoints.RIGHT_WRIST.name


class RightWristIndexSegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_WRIST.name
    z_axis_reference = BodyKeypoints.RIGHT_INDEX_KNUCKLE.name


class RightWristPinkySegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_WRIST.name
    z_axis_reference = BodyKeypoints.RIGHT_PINKY_KNUCKLE.name


class RightWristThumbSegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_WRIST.name
    z_axis_reference = BodyKeypoints.RIGHT_THUMB_KNUCKLE.name


# leg
class RightPelvisSegment(SimpleSegmentABC):
    origin = BodyKeypoints.PELVIS_SPINE_SACRUM_ORIGIN.name
    z_axis_reference = BodyKeypoints.PELVIS_RIGHT_HIP_ACETABULUM.name


class RightThighSegment(SimpleSegmentABC):
    origin = BodyKeypoints.PELVIS_RIGHT_HIP_ACETABULUM.name
    z_axis_reference = BodyKeypoints.RIGHT_KNEE.name


class RightCalfSegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_KNEE.name
    z_axis_reference = BodyKeypoints.RIGHT_ANKLE.name


class RightFootFrontSegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_ANKLE.name
    z_axis_reference = BodyKeypoints.RIGHT_HALLUX_TIP.name


class RightHeelSegment(SimpleSegmentABC):
    origin = BodyKeypoints.RIGHT_ANKLE.name
    z_axis_reference = BodyKeypoints.RIGHT_HEEL.name


# Left Body

# arm
class LeftClavicleSegment(SimpleSegmentABC):
    origin = BodyKeypoints.THORACIC_SPINE_TOP_T1.name
    z_axis_reference = BodyKeypoints.LEFT_SHOULDER.name


class LeftUpperArmSegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_SHOULDER.name
    z_axis_reference = BodyKeypoints.LEFT_ELBOW.name


class LeftForearmSegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_ELBOW.name
    z_axis_reference = BodyKeypoints.LEFT_WRIST.name


class LeftWristIndexSegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_WRIST.name
    z_axis_reference = BodyKeypoints.LEFT_INDEX_KNUCKLE.name


class LeftWristPinkySegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_WRIST.name
    z_axis_reference = BodyKeypoints.LEFT_PINKY_KNUCKLE.name


class LeftWristThumbSegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_WRIST.name
    z_axis_reference = BodyKeypoints.LEFT_THUMB_KNUCKLE.name


# leg
class LeftPelvisSegment(SimpleSegmentABC):
    origin = BodyKeypoints.PELVIS_SPINE_SACRUM_ORIGIN.name
    z_axis_reference = BodyKeypoints.PELVIS_LEFT_HIP_ACETABULUM.name


class LeftThighSegment(SimpleSegmentABC):
    origin = BodyKeypoints.PELVIS_LEFT_HIP_ACETABULUM.name
    z_axis_reference = BodyKeypoints.LEFT_KNEE.name


class LeftCalfSegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_KNEE.name
    z_axis_reference = BodyKeypoints.LEFT_ANKLE.name


class LeftFootFrontSegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_ANKLE.name
    z_axis_reference = BodyKeypoints.LEFT_HALLUX_TIP.name


class LeftHeelSegment(SimpleSegmentABC):
    origin = BodyKeypoints.LEFT_ANKLE.name
    z_axis_reference = BodyKeypoints.LEFT_HEEL.name


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
    x_axis_reference = BodyKeypoints.SKULL_FORWARD_NOSE_TIP.name
    y_axis_reference = BodyKeypoints.LEFT_SKULL_ACOUSTIC_MEATUS.name


class PelvisLumbarCompoundSegment(CompoundSegmentABC):
    segments = [BodyKeypoints.SPINE_LUMBAR_TOP_L1.name,
                BodyKeypoints.PELVIS_RIGHT_HIP_ACETABULUM.name,
                BodyKeypoints.PELVIS_LEFT_HIP_ACETABULUM.name]
    origin = BodyKeypoints.PELVIS_SPINE_SACRUM_ORIGIN.name
    z_axis_reference = BodyKeypoints.SPINE_LUMBAR_TOP_L1.name
    x_axis_reference = BodyKeypoints.PELVIS_RIGHT_HIP_ACETABULUM.name


class BodyCompoundSegments(SegmentEnum):
    SKULL: CompoundSegmentABC = SkullCompoundSegment
    SPINE_PELVIS_LUMBAR: CompoundSegmentABC = PelvisLumbarCompoundSegment


class BodySegments(SegmentEnum):
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
    SPINE_SACRUM_LUMBAR: SimpleSegmentABC = SpineSacrumLumbar
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

if __name__ == "__main__":
    print("\n".join([f"{key}: origin={value.value.origin}, z_axis_reference={value.value.z_axis_reference}" for key, value in BodySegments.__members__.items()]))

