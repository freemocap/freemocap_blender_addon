import math as m
from enum import Enum

from freemocap_blender_addon.models.animation.poses.pose_element import PoseElement
from freemocap_blender_addon.models.skeleton_model.body.segments import SkullSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import AxialSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightBodySegments

_FREEMOCAP_BODY_TPOSE_DEFINTIONS = {
    # Axial segments
    AxialSegments.LUMBAR.name: PoseElement(
        rotation=(m.radians(-90), 0, 0),
    ),
    AxialSegments.THORACIC.name: PoseElement(
        rotation=(0, 0, 0),
    ),
    AxialSegments.CERVICAL.name: PoseElement(
        rotation=(0, 0, 0),
    ),
    SkullSegments.NOSE.name: PoseElement(
        rotation=(m.radians(110), 0, 0),
    ),
    SkullSegments.RIGHT_EYE_CENTER.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    SkullSegments.LEFT_EYE_CENTER.name: PoseElement(
        rotation=(0, m.radians(90), 0),
    ),

    # Right upper limb
    RightBodySegments.RIGHT_CLAVICLE.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    RightBodySegments.RIGHT_UPPER_ARM.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    RightBodySegments.RIGHT_FOREARM.name: PoseElement(
        rotation=(0, m.radians(-90), m.radians(1)),
    ),
    RightBodySegments.RIGHT_WRIST_INDEX.name: PoseElement(
        rotation=(0, m.radians(-90), m.radians(45)),
    ),
    RightBodySegments.RIGHT_WRIST_PINKY.name: PoseElement(
        rotation=(0, m.radians(-90), m.radians(-45)),
    ),
    RightBodySegments.RIGHT_WRIST_THUMB.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),

    # Right lower limb
    RightBodySegments.RIGHT_PELVIS.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    RightBodySegments.RIGHT_THIGH.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    RightBodySegments.RIGHT_CALF.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    RightBodySegments.RIGHT_FORE_FOOT.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    RightBodySegments.RIGHT_HEEL.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),

    # Left upper limb
    LeftBodySegments.LEFT_CLAVICLE.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    LeftBodySegments.LEFT_UPPER_ARM.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    LeftBodySegments.LEFT_FOREARM.name: PoseElement(
        rotation=(0, m.radians(-90), m.radians(1)),
    ),
    LeftBodySegments.LEFT_WRIST_INDEX.name: PoseElement(
        rotation=(0, m.radians(-90), m.radians(45)),
    ),
    LeftBodySegments.LEFT_WRIST_PINKY.name: PoseElement(
        rotation=(0, m.radians(-90), m.radians(-45)),
    ),
    LeftBodySegments.LEFT_WRIST_THUMB.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),

    # Left lower limb
    LeftBodySegments.LEFT_PELVIS.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    LeftBodySegments.LEFT_THIGH.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    LeftBodySegments.LEFT_CALF.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    LeftBodySegments.LEFT_FORE_FOOT.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
    LeftBodySegments.LEFT_HEEL.name: PoseElement(
        rotation=(0, m.radians(-90), 0),
    ),
}

BodySkeletonTPoseDefinition = Enum('BodySkeletonTPoseDefinition', _FREEMOCAP_BODY_TPOSE_DEFINTIONS)


if __name__ == "__main__":
    for name, member in BodySkeletonTPoseDefinition.__members__.items():
        print(f"{name}: {member.value}")

#
# "thumb.carpal.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(45)),
# ),
# "thumb.carpal.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(-45)),
# ),
# "thumb.01.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(45)),
# ),
# "thumb.01.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(-45)),
# ),
# "thumb.02.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(45)),
# ),
# "thumb.02.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(-45)),
# ),
# "thumb.03.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(45)),
# ),
# "thumb.03.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(-45)),
# ),
# "palm.01.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(17)),
# ),
# "palm.01.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(-17)),
# ),
# "f_index.01.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_index.01.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_index.02.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_index.02.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_index.03.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_index.03.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "palm.02.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(5.5)),
# ),
# "palm.02.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(-5.5)),
# ),
# "f_middle.01.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_middle.01.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_middle.02.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_middle.02.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_middle.03.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_middle.03.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "palm.03.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(-7.3)),
# ),
# "palm.03.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(7.3)),
# ),
# "f_ring.01.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_ring.01.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_ring.02.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_ring.02.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_ring.03.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_ring.03.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "palm.04.R": PoseElement(
#     rotation=(0, m.radians(-90), m.radians(-19)),
# ),
# "palm.04.L": PoseElement(
#     rotation=(0, m.radians(90), m.radians(19)),
# ),
# "f_pinky.01.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_pinky.01.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_pinky.02.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_pinky.02.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
# "f_pinky.03.R": PoseElement(
#     rotation=(0, m.radians(-90), 0),
# ),
# "f_pinky.03.L": PoseElement(
#     rotation=(0, m.radians(90), 0),
# ),
