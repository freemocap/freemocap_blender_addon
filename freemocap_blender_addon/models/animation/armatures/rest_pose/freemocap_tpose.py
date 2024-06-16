import math as m
from enum import Enum

from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import ROOT_BONE_PARENT_NAME, \
    BonePoseDefinition
from freemocap_blender_addon.models.skeleton_model.body.segments import SkullSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import AxialSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightBodySegments
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name

_FREEMOCAP_BODY_TPOSE_DEFINITIONS = {
    # Axial segments
    blenderize_name(AxialSegments.LUMBAR.name): BonePoseDefinition(
        rotation=(m.radians(-90), 0, 0),
        parent_bone_name=ROOT_BONE_PARENT_NAME
    ),
    blenderize_name(AxialSegments.THORACIC.name): BonePoseDefinition(
        rotation=(0, 0, 0),
        parent_bone_name=blenderize_name(AxialSegments.LUMBAR.name)
    ),
    blenderize_name(AxialSegments.CERVICAL.name): BonePoseDefinition(
        rotation=(0, 0, 0),
        parent_bone_name=blenderize_name(AxialSegments.THORACIC.name)
    ),
    blenderize_name(SkullSegments.NOSE.name): BonePoseDefinition(
        rotation=(m.radians(110), 0, 0),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.RIGHT_EYE_CENTER.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.LEFT_EYE_CENTER.name): BonePoseDefinition(
        rotation=(0, m.radians(90), 0),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),

    # Right upper limb
    blenderize_name(RightBodySegments.RIGHT_CLAVICLE.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(AxialSegments.THORACIC.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_UPPER_ARM.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_CLAVICLE.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_FOREARM.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), m.radians(1)),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_UPPER_ARM.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_WRIST_INDEX.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), m.radians(45)),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_FOREARM.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_WRIST_PINKY.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), m.radians(-45)),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_FOREARM.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_WRIST_THUMB.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_FOREARM.name)
    ),

    # Right lower limb
    blenderize_name(RightBodySegments.RIGHT_PELVIS.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(AxialSegments.LUMBAR.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_THIGH.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_PELVIS.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_CALF.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_THIGH.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_FORE_FOOT.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_CALF.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_HEEL.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_CALF.name)
    ),

    # Left upper limb
    blenderize_name(LeftBodySegments.LEFT_CLAVICLE.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(AxialSegments.THORACIC.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_UPPER_ARM.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_CLAVICLE.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_FOREARM.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), m.radians(1)),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_UPPER_ARM.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_WRIST_INDEX.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), m.radians(45)),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_FOREARM.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_WRIST_PINKY.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), m.radians(-45)),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_FOREARM.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_WRIST_THUMB.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_FOREARM.name)
    ),

    # Left lower limb
    blenderize_name(LeftBodySegments.LEFT_PELVIS.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(AxialSegments.LUMBAR.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_THIGH.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_PELVIS.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_CALF.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_THIGH.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_FORE_FOOT.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_CALF.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_HEEL.name): BonePoseDefinition(
        rotation=(0, m.radians(-90), 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_CALF.name)
    ),
}

BodySkeletonTPoseDefinition = Enum('BodySkeletonTPoseDefinition', _FREEMOCAP_BODY_TPOSE_DEFINITIONS)

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
