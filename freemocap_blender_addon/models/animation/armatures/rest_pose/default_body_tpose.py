from enum import Enum

from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import BoneRestPoseDefinition, \
    ROOT_BONE_NAME
from freemocap_blender_addon.models.skeleton_model.body.segments.axial_segments import BlenderizedAxialSegments
from freemocap_blender_addon.models.skeleton_model.body.segments.left_body_segments import BlenderizedLeftBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.right_body_segments import BlenderizedRightBodySegments
from freemocap_blender_addon.models.skeleton_model.body.segments.skull_segments import BlenderizedSkullSegments

_BODY_ARMATURE_TPOSE_DEFINITIION = {
    # Axial segments
    BlenderizedAxialSegments.LUMBAR_SPINE.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    BlenderizedAxialSegments.THORACIC_SPINE.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=BlenderizedAxialSegments.LUMBAR_SPINE.value
    ),
    BlenderizedAxialSegments.CERVICAL_SPINE.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 0, 0),
        parent_bone_name=BlenderizedAxialSegments.THORACIC_SPINE.value
    ),

    # Skull segments
    BlenderizedSkullSegments.NOSE.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-100, 0, 0),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    # right face
    BlenderizedSkullSegments.RIGHT_SKULL_EYE_INNER.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -20),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.RIGHT_SKULL_EYE_CENTER.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -30),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.RIGHT_SKULL_EYE_OUTER.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, -40),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.RIGHT_SKULL_ACOUSTIC_MEATUS.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, -90),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.RIGHT_SKULL_CANINE_TOOTH_TIP.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-120, -20, 0),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    # left face
    BlenderizedSkullSegments.LEFT_SKULL_EYE_INNER.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 20),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.LEFT_SKULL_EYE_CENTER.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 30),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.LEFT_SKULL_EYE_OUTER.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-80, 0, 40),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.LEFT_SKULL_LEFTWARD_ACOUSTIC_MEATUS.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-90, 0, 90),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),
    BlenderizedSkullSegments.LEFT_SKULL_CANINE_TOOTH_TIP.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-120, 20, 0),
        parent_bone_name=BlenderizedAxialSegments.CERVICAL_SPINE.value
    ),

    # Right upper limb
    BlenderizedRightBodySegments.RIGHT_CLAVICLE.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),

        parent_bone_name=BlenderizedAxialSegments.THORACIC_SPINE.value
    ),
    BlenderizedRightBodySegments.RIGHT_UPPER_ARM.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_CLAVICLE.value
    ),
    BlenderizedRightBodySegments.RIGHT_FOREARM.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 1),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_UPPER_ARM.value
    ),
    BlenderizedRightBodySegments.RIGHT_WRIST_INDEX.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_FOREARM.value
    ),
    BlenderizedRightBodySegments.RIGHT_WRIST_PINKY.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 45),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_FOREARM.value
    ),
    BlenderizedRightBodySegments.RIGHT_WRIST_THUMB.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, -45),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_FOREARM.value
    ),

    # Right lower limb
    BlenderizedRightBodySegments.RIGHT_PELVIS.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    BlenderizedRightBodySegments.RIGHT_THIGH.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_PELVIS.value
    ),
    BlenderizedRightBodySegments.RIGHT_CALF.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_THIGH.value
    ),
    BlenderizedRightBodySegments.RIGHT_FORE_FOOT.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_CALF.value
    ),
    BlenderizedRightBodySegments.RIGHT_HEEL.value: BoneRestPoseDefinition(
        world_rotation_degrees=(70, 170, 0),
        parent_bone_name=BlenderizedRightBodySegments.RIGHT_CALF.value
    ),

    # Left upper limb
    BlenderizedLeftBodySegments.LEFT_CLAVICLE.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=BlenderizedAxialSegments.THORACIC_SPINE.value
    ),
    BlenderizedLeftBodySegments.LEFT_UPPER_ARM.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_CLAVICLE.value
    ),
    BlenderizedLeftBodySegments.LEFT_FOREARM.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 1),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_UPPER_ARM.value
    ),
    BlenderizedLeftBodySegments.LEFT_WRIST_INDEX.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_FOREARM.value
    ),
    BlenderizedLeftBodySegments.LEFT_WRIST_PINKY.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 45),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_FOREARM.value
    ),
    BlenderizedLeftBodySegments.LEFT_WRIST_THUMB.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, -45),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_FOREARM.value
    ),

    # Left lower limb
    BlenderizedLeftBodySegments.LEFT_PELVIS.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, -90, 0),
        parent_bone_name=ROOT_BONE_NAME
    ),
    BlenderizedLeftBodySegments.LEFT_THIGH.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_PELVIS.value
    ),
    BlenderizedLeftBodySegments.LEFT_CALF.value: BoneRestPoseDefinition(
        world_rotation_degrees=(0, 180, 0),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_THIGH.value
    ),
    BlenderizedLeftBodySegments.LEFT_FORE_FOOT.value: BoneRestPoseDefinition(
        world_rotation_degrees=(-70, 170, 0),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_CALF.value
    ),
    BlenderizedLeftBodySegments.LEFT_HEEL.value: BoneRestPoseDefinition(
        world_rotation_degrees=(70, 190, 0),
        parent_bone_name=BlenderizedLeftBodySegments.LEFT_CALF.value
    ),
}

BodyArmatureTPoseDefinition = Enum('BodyArmatureTPoseDefinition', _BODY_ARMATURE_TPOSE_DEFINITIION)

if __name__ == "__main__":
    for name, member in BodyArmatureTPoseDefinition.__members__.items():
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
