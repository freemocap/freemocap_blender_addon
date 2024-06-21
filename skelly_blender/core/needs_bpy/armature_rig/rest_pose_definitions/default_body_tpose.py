from enum import Enum

from skelly_blender.core.needs_bpy.armature_rig.armature.armature_bone_classes import BoneRestPoseDefinition, \
    ROOT_BONE_NAME
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_segments import BodySegments


_BODY_ARMATURE_TPOSE_DEFINITIION = {
    # Axial segments
    BodySegments.PELVIS_LUMBAR.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    BodySegments.SPINE_THORACIC.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=BodySegments.PELVIS_LUMBAR.blenderize()
    ),
    BodySegments.SPINE_CERVICAL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=BodySegments.SPINE_THORACIC.blenderize()
    ),

    # Skull segments
    BodySegments.SKULL_NOSE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-100, 0, 0),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    # right face
    BodySegments.SKULL_RIGHT_EYE_INNER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -20),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_RIGHT_EYE_CENTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -30),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_RIGHT_EYE_OUTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -40),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_RIGHT_EAR.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, -90),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_RIGHT_MOUTH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-120, -20, 0),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    # left face
    BodySegments.SKULL_LEFT_EYE_INNER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 20),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_LEFT_EYE_CENTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 30),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_LEFT_EYE_OUTER.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 40),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_LEFT_EAR.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, 90),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),
    BodySegments.SKULL_LEFT_MOUTH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-120, 20, 0),
        parent_bone_name=BodySegments.SPINE_CERVICAL.blenderize()
    ),

    # Right upper limb
    BodySegments.RIGHT_CLAVICLE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),

        parent_bone_name=BodySegments.SPINE_THORACIC.blenderize()
    ),
    BodySegments.RIGHT_ARM_PROXIMAL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=BodySegments.RIGHT_CLAVICLE.blenderize()
    ),
    BodySegments.RIGHT_ARM_DISTAL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 1),
        parent_bone_name=BodySegments.RIGHT_ARM_PROXIMAL.blenderize()
    ),
    BodySegments.RIGHT_PALM_INDEX.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=BodySegments.RIGHT_ARM_DISTAL.blenderize()
    ),
    BodySegments.RIGHT_PALM_PINKY.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 45),
        parent_bone_name=BodySegments.RIGHT_ARM_DISTAL.blenderize()
    ),
    BodySegments.RIGHT_PALM_THUMB.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, -45),
        parent_bone_name=BodySegments.RIGHT_ARM_DISTAL.blenderize()
    ),

    # Right lower limb
    BodySegments.PELVIS_RIGHT.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    BodySegments.RIGHT_LEG_THIGH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BodySegments.PELVIS_RIGHT.blenderize()
    ),
    BodySegments.RIGHT_LEG_CALF.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BodySegments.RIGHT_LEG_THIGH.blenderize()
    ),
    BodySegments.RIGHT_FOOT_FRONT.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=BodySegments.RIGHT_LEG_CALF.blenderize()
    ),
    BodySegments.RIGHT_FOOT_HEEL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(70, 170, 0),
        parent_bone_name=BodySegments.RIGHT_LEG_CALF.blenderize()
    ),

    # Left upper limb
    BodySegments.LEFT_CLAVICLE.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=BodySegments.SPINE_THORACIC.blenderize()
    ),
    BodySegments.LEFT_ARM_PROXIMAL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=BodySegments.LEFT_CLAVICLE.blenderize()
    ),
    BodySegments.LEFT_ARM_DISTAL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 1),
        parent_bone_name=BodySegments.LEFT_ARM_PROXIMAL.blenderize()
    ),
    BodySegments.LEFT_PALM_INDEX.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=BodySegments.LEFT_ARM_DISTAL.blenderize()
    ),
    BodySegments.LEFT_PALM_PINKY.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 45),
        parent_bone_name=BodySegments.LEFT_ARM_DISTAL.blenderize()
    ),
    BodySegments.LEFT_PALM_THUMB.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, -45),
        parent_bone_name=BodySegments.LEFT_ARM_DISTAL.blenderize()
    ),

    # Left lower limb
    BodySegments.PELVIS_LEFT.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    BodySegments.LEFT_LEG_THIGH.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BodySegments.PELVIS_LEFT.blenderize()
    ),
    BodySegments.LEFT_LEG_CALF.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BodySegments.LEFT_LEG_THIGH.blenderize()
    ),
    BodySegments.LEFT_FOOT_FRONT.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=BodySegments.LEFT_LEG_CALF.blenderize()
    ),
    BodySegments.LEFT_FOOT_HEEL.blenderize(): BoneRestPoseDefinition(
        world_rotation_degrees=(70, 190, 0),
        parent_bone_name=BodySegments.LEFT_LEG_CALF.blenderize()
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
