from enum import Enum

from skelly_blender.core.blender_stuff.armature_rig.armatures.armature_bone_classes import BoneRestPoseDefinition, \
    ROOT_BONE_NAME
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.segments.axial_segments import AxialSegments
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.segments.left_body_segments import \
    LeftBodySegments
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.segments.right_body_segments import \
    RightBodySegments
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.segments.skull_segments import SkullSegments

_BODY_ARMATURE_TPOSE_DEFINITIION = {
    # Axial segments
    AxialSegments.PELVIS_LUMBAR.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    AxialSegments.THORACIC_SPINE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=AxialSegments.PELVIS_LUMBAR.blenderize()
    ),
    AxialSegments.CERVICAL_SPINE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=AxialSegments.THORACIC_SPINE.blenderize()
    ),

    # Skull segments
    SkullSegments.NOSE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-100, 0, 0),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    # right face
    SkullSegments.RIGHT_EYE_INNER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -20),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.RIGHT_EYE_CENTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -30),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.RIGHT_EYE_OUTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -40),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.RIGHT_EAR_TRAGUS.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, -90),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.RIGHT_MOUTH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-120, -20, 0),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    # left face
    SkullSegments.LEFT_EYE_INNER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 20),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.LEFT_EYE_CENTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 30),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.LEFT_EYE_OUTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 40),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.LEFT_EAR_TRAGUS.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, 90),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),
    SkullSegments.LEFT_MOUTH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-120, 20, 0),
        parent_bone_name=AxialSegments.CERVICAL_SPINE.blenderize()
    ),

    # Right upper limb
    RightBodySegments.RIGHT_CLAVICLE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),

        parent_bone_name=AxialSegments.THORACIC_SPINE.blenderize()
    ),
    RightBodySegments.RIGHT_UPPER_ARM.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=RightBodySegments.RIGHT_CLAVICLE.blenderize()
    ),
    RightBodySegments.RIGHT_FOREARM.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 1),
        parent_bone_name=RightBodySegments.RIGHT_UPPER_ARM.blenderize()
    ),
    RightBodySegments.RIGHT_WRIST_INDEX.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=RightBodySegments.RIGHT_FOREARM.blenderize()
    ),
    RightBodySegments.RIGHT_WRIST_PINKY.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 45),
        parent_bone_name=RightBodySegments.RIGHT_FOREARM.blenderize()
    ),
    RightBodySegments.RIGHT_WRIST_THUMB.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, -45),
        parent_bone_name=RightBodySegments.RIGHT_FOREARM.blenderize()
    ),

    # Right lower limb
    RightBodySegments.RIGHT_PELVIS.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    RightBodySegments.RIGHT_THIGH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=RightBodySegments.RIGHT_PELVIS.blenderize()
    ),
    RightBodySegments.RIGHT_CALF.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=RightBodySegments.RIGHT_THIGH.blenderize()
    ),
    RightBodySegments.RIGHT_FORE_FOOT.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=RightBodySegments.RIGHT_CALF.blenderize()
    ),
    RightBodySegments.RIGHT_HEEL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(70, 170, 0),
        parent_bone_name=RightBodySegments.RIGHT_CALF.blenderize()
    ),

    # Left upper limb
    LeftBodySegments.LEFT_CLAVICLE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=AxialSegments.THORACIC_SPINE.blenderize()
    ),
    LeftBodySegments.LEFT_UPPER_ARM.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=LeftBodySegments.LEFT_CLAVICLE.blenderize()
    ),
    LeftBodySegments.LEFT_FOREARM.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 1),
        parent_bone_name=LeftBodySegments.LEFT_UPPER_ARM.blenderize()
    ),
    LeftBodySegments.LEFT_WRIST_INDEX.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=LeftBodySegments.LEFT_FOREARM.blenderize()
    ),
    LeftBodySegments.LEFT_WRIST_PINKY.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 45),
        parent_bone_name=LeftBodySegments.LEFT_FOREARM.blenderize()
    ),
    LeftBodySegments.LEFT_WRIST_THUMB.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, -45),
        parent_bone_name=LeftBodySegments.LEFT_FOREARM.blenderize()
    ),

    # Left lower limb
    LeftBodySegments.LEFT_PELVIS.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    LeftBodySegments.LEFT_THIGH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=LeftBodySegments.LEFT_PELVIS.blenderize()
    ),
    LeftBodySegments.LEFT_CALF.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=LeftBodySegments.LEFT_THIGH.blenderize()
    ),
    LeftBodySegments.LEFT_FORE_FOOT.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=LeftBodySegments.LEFT_CALF.blenderize()
    ),
    LeftBodySegments.LEFT_HEEL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(70, 190, 0),
        parent_bone_name=LeftBodySegments.LEFT_CALF.blenderize()
    ),
}

BodyArmatureTPoseDefinition = Enum('BodyArmatureTPoseDefinition', _BODY_ARMATURE_TPOSE_DEFINITIION)

if __name__ == "__main__":
    for name, member in BodyArmatureTPoseDefinition.__members__.items():
        print(f"{name}: {member.blenderize()}")

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
