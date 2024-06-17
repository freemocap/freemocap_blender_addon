import math as m
from enum import Enum

from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import BoneRestPoseDefinition, \
    ROOT_BONE_NAME
from freemocap_blender_addon.models.skeleton_model.body.segments import SkullSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import AxialSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import LeftBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import RightBodySegments
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name


_FREEMOCAP_BODY_TPOSE_DEFINITIONS = {
    # Axial segments
    blenderize_name(AxialSegments.LUMBAR.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    blenderize_name(AxialSegments.THORACIC.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=blenderize_name(AxialSegments.LUMBAR.name)
    ),
    blenderize_name(AxialSegments.CERVICAL.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=blenderize_name(AxialSegments.THORACIC.name)
    ),

    # Skull segments
    blenderize_name(SkullSegments.NOSE.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-100, 0, 0),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    #right face
    blenderize_name(SkullSegments.RIGHT_EYE_INNER.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -20),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.RIGHT_EYE_CENTER.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -30),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.RIGHT_EYE_OUTER.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -40),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.RIGHT_EAR_TRAGUS.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, -90),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.RIGHT_MOUTH.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-120, -20,0),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    #left face
    blenderize_name(SkullSegments.LEFT_EYE_INNER.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 20),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.LEFT_EYE_CENTER.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 30),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.LEFT_EYE_OUTER.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 40),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.LEFT_EAR_TRAGUS.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, 90),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),
    blenderize_name(SkullSegments.LEFT_MOUTH.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-120, 20, 0),
        parent_bone_name=blenderize_name(AxialSegments.CERVICAL.name)
    ),


    # Right upper limb
    blenderize_name(RightBodySegments.RIGHT_CLAVICLE.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),

        parent_bone_name=blenderize_name(AxialSegments.THORACIC.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_UPPER_ARM.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_CLAVICLE.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_FOREARM.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 1),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_UPPER_ARM.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_WRIST_INDEX.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_FOREARM.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_WRIST_PINKY.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 45),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_FOREARM.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_WRIST_THUMB.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, -45),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_FOREARM.name)
    ),

    # Right lower limb
    blenderize_name(RightBodySegments.RIGHT_PELVIS.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    blenderize_name(RightBodySegments.RIGHT_THIGH.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_PELVIS.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_CALF.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_THIGH.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_FORE_FOOT.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_CALF.name)
    ),
    blenderize_name(RightBodySegments.RIGHT_HEEL.name): BoneRestPoseDefinition(
        world_rotation_degrees=(70, 170, 0),
        parent_bone_name=blenderize_name(RightBodySegments.RIGHT_CALF.name)
    ),

    # Left upper limb
    blenderize_name(LeftBodySegments.LEFT_CLAVICLE.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=blenderize_name(AxialSegments.THORACIC.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_UPPER_ARM.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_CLAVICLE.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_FOREARM.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 1),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_UPPER_ARM.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_WRIST_INDEX.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_FOREARM.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_WRIST_PINKY.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 45),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_FOREARM.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_WRIST_THUMB.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, -45),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_FOREARM.name)
    ),

    # Left lower limb
    blenderize_name(LeftBodySegments.LEFT_PELVIS.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    blenderize_name(LeftBodySegments.LEFT_THIGH.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_PELVIS.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_CALF.name): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_THIGH.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_FORE_FOOT.name): BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_CALF.name)
    ),
    blenderize_name(LeftBodySegments.LEFT_HEEL.name): BoneRestPoseDefinition(
        world_rotation_degrees=(70, 190, 0),
        parent_bone_name=blenderize_name(LeftBodySegments.LEFT_CALF.name)
    ),
}

BodySkeletonTPoseDefinition = Enum('BodySkeletonTPoseDefinition', _FREEMOCAP_BODY_TPOSE_DEFINITIONS)

if __name__ == "__main__":
    for name, member in BodySkeletonTPoseDefinition.__members__.items():
        print(f"{name}: {member.value}")

#
# "thumb.carpal.R": PoseElement(
#     local_rotation_degrees=(0, -90, 45),
# ),
# "thumb.carpal.L": PoseElement(
#     local_rotation_degrees=(0, 90, -45),
# ),
# "thumb.01.R": PoseElement(
#     local_rotation_degrees=(0, -90, 45),
# ),
# "thumb.01.L": PoseElement(
#     local_rotation_degrees=(0, 90, -45),
# ),
# "thumb.02.R": PoseElement(
#     local_rotation_degrees=(0, -90, 45),
# ),
# "thumb.02.L": PoseElement(
#     local_rotation_degrees=(0, 90, -45),
# ),
# "thumb.03.R": PoseElement(
#     local_rotation_degrees=(0, -90, 45),
# ),
# "thumb.03.L": PoseElement(
#     local_rotation_degrees=(0, 90, -45),
# ),
# "palm.01.R": PoseElement(
#     local_rotation_degrees=(0, -90, 17),
# ),
# "palm.01.L": PoseElement(
#     local_rotation_degrees=(0, 90, -17),
# ),
# "f_index.01.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_index.01.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_index.02.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_index.02.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_index.03.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_index.03.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "palm.02.R": PoseElement(
#     local_rotation_degrees=(0, -90, 5.5),
# ),
# "palm.02.L": PoseElement(
#     local_rotation_degrees=(0, 90, -5.5),
# ),
# "f_middle.01.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_middle.01.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_middle.02.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_middle.02.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_middle.03.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_middle.03.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "palm.03.R": PoseElement(
#     local_rotation_degrees=(0, -90, -7.3)),
# ),
# "palm.03.L": PoseElement(
#     local_rotation_degrees=(0, 90, 7.3)),
# ),
# "f_ring.01.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_ring.01.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_ring.02.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_ring.02.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_ring.03.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_ring.03.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "palm.04.R": PoseElement(
#     local_rotation_degrees=(0, -90, -19)),
# ),
# "palm.04.L": PoseElement(
#     local_rotation_degrees=(0, 90, 19)),
# ),
# "f_pinky.01.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_pinky.01.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_pinky.02.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_pinky.02.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
# "f_pinky.03.R": PoseElement(
#     local_rotation_degrees=(0, -90, 0),
# ),
# "f_pinky.03.L": PoseElement(
#     local_rotation_degrees=(0, 90, 0),
# ),
