import bpy
import mathutils

from freemocap_blender_addon.models.animation.armatures.armature_definition import ArmatureDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose.pose_types import PoseTypes
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes


def generate_armature(
        armature_definition: ArmatureDefinition,
) -> bpy.types.Object:

    armature = create_new_armature_and_enter_edit_mode(name=armature_definition.armature_name)

    while not list(armature_definition.bone_definitions.keys()) <= list(
            armature.data.edit_bones.keys()):  # check if all bones are in the rig, iterate until all bones are in the rig
        for bone_name, bone_definition in armature_definition.bone_definitions.items():

            if bone_name in armature.data.edit_bones.keys():
                # If the bone already exists, we can skip it
                continue

            if bone_definition.parent not in armature.data.edit_bones.keys() and not bone_definition.is_root:
                # If the parent bone does not exist, we skip this bone and come back to itwhen the parent bone is created
                continue

            # Add the new bone
            rig_bone = armature.data.edit_bones.new(name=bone_name)

            if bone_definition.is_root:
                rig_bone.head = mathutils.Vector([0, 0, 0])
            else:
                # Set the bone head position relative to its parent
                rig_bone.head = armature.data.edit_bones[bone_definition.parent].tail

            bone_vector = mathutils.Vector(
                [0, 0, bone_definition.length]
            )

            # Get the rotation matrix
            rotation_matrix = mathutils.Euler(
                mathutils.Vector(bone_definition.rest_pose.rotation),
                "XYZ",
            ).to_matrix()

            # Set the tail position
            rig_bone.tail = rig_bone.head + rotation_matrix @ bone_vector

            if not bone_definition.is_root:
                rig_bone.parent = armature.data.edit_bones[bone_definition.parent]

            rig_bone.use_connect = bone_definition.rest_pose.is_connected

    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")
    return armature


def create_new_armature_and_enter_edit_mode(name: str) -> bpy.types.Object:
    # Add the armature
    bpy.ops.object.armature_add(
        enter_editmode=True,
        align="WORLD",
        location=(0, 0, 0),
    )
    # Rename the armature
    bpy.data.armatures[0].name = name
    # Get the armature object
    armature = bpy.data.objects["Armature"]
    # Rename the armature object
    armature.name = name
    # Remove the default bone
    armature.data.edit_bones.remove(armature.data.edit_bones["Bone"])
    return armature


if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_test_recording
    from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
        calculate_rigid_body_trajectories

    recording_data = load_freemocap_test_recording()
    keypoint_trajectories_outer, segment_definitions_outer = calculate_rigid_body_trajectories(
        keypoint_trajectories=recording_data.body.map_to_keypoints(),
        skeleton_definition=SkeletonTypes.BODY_ONLY)

    armature = generate_armature(
        armature_definition=ArmatureDefinition.create(
            rig_name="rig",
            segment_definitions=segment_definitions_outer,
            pose_definition=PoseTypes.DEFAULT_TPOSE,
        )
    )
