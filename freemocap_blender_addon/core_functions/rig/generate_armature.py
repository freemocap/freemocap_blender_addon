import bpy
import mathutils

from freemocap_blender_addon.models.animation.armatures.armature_definition import ArmatureDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose.bone_pose_definition import ROOT_BONE_NAME
from freemocap_blender_addon.models.animation.armatures.rest_pose.pose_types import PoseTypes
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes


def generate_armature(
        armature_definition: ArmatureDefinition,
) -> bpy.types.Object:

    armature = create_new_armature_and_enter_edit_mode(name=armature_definition.armature_name)

    for bone_name, bone_definition in armature_definition.bone_definitions.items():

        print(f"Creating armature bone: {bone_name}")
        # Add the new bone
        armature_bone = armature.data.edit_bones.new(name=bone_name)

        bone_vector = mathutils.Vector(
            [0, 0, bone_definition.length]
        )

        # Get the rotation matrix
        rotation_matrix = mathutils.Euler(
            mathutils.Vector(bone_definition.rest_pose.rotation),
            "XYZ",
        ).to_matrix()

        # Set the tail position
        armature_bone.tail = armature_bone.head + rotation_matrix @ bone_vector

    for bone_name, bone_definition in armature_definition.bone_definitions.items():
        armature_bone = armature.data.edit_bones[bone_name]
        # Set the bone head position relative to its parent
        armature_bone.head = armature.data.edit_bones[bone_definition.parent].tail
        if not bone_definition.is_root:
            armature_bone.parent = armature.data.edit_bones[bone_definition.parent]

        armature_bone.use_connect = bone_definition.rest_pose.is_connected

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
    # Rename default bone to `Root`
    default_bone = armature.data.edit_bones[0]
    default_bone.name = ROOT_BONE_NAME
    default_bone.tail = (0, 0, 0)
    default_bone.head = (-.1, 0, 0)
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
