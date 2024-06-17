import bpy
import mathutils

from freemocap_blender_addon.models.animation.armatures.armature_definition import ArmatureDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose import ROOT_BONE_NAME
from freemocap_blender_addon.models.animation.armatures.rest_pose import PoseTypes
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes


def generate_armature(
        armature_definition: ArmatureDefinition,
) -> bpy.types.Object:
    armature = create_new_armature_and_enter_edit_mode(name=armature_definition.armature_name)
    bones_to_make = list(armature_definition.bone_definitions.items())
    while len(bones_to_make) > 0:
        for bone_info in bones_to_make:
            bone_name, bone_definition = bone_info
            if bone_definition.parent not in armature.data.edit_bones:
                continue  # Skip this bone until its parent is created
            bones_to_make.remove(bone_info)  # Remove this bone from the list of bones to make

            print(f"Creating armature bone: {bone_name} with parent: {bone_definition.parent}")
            armature.data.edit_bones.new(name=bone_name)
            armature_bone = armature.data.edit_bones[bone_name]
            assign_bone_color(bone=armature_bone)

            bone_vector = mathutils.Vector([0, 0, bone_definition.length])

            parent_bone = armature.data.edit_bones[bone_definition.parent]

            armature_bone.head = parent_bone.tail
            armature_bone.tail = armature_bone.head + bone_definition.rest_pose.rotation_matrix @ bone_vector
            armature_bone.roll = bone_definition.rest_pose.roll
            armature_bone.parent = parent_bone
            armature_bone.use_connect = bone_definition.rest_pose.is_connected

    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")
    return armature


def assign_bone_color(bone: bpy.types.EditBone):
    # Check for .L, .R, or axial in the bone name and assign colors accordingly
    if bone.name.endswith('.L'):
        bone.color.palette = 'THEME04'  # Blue
    elif bone.name.endswith('.R'):
        bone.color.palette = 'THEME01'  # Red
    else:
        bone.color.palette = 'THEME03'  # Green


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
    default_bone.head = (0, -.1, 0)
    return armature


if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_test_recording
    from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
        calculate_rigid_body_trajectories

    recording_data = load_freemocap_test_recording()
    keypoint_trajectories_outer, segment_definitions_outer = calculate_rigid_body_trajectories(
        keypoint_trajectories=recording_data.body.map_to_keypoints(),
        skeleton_definition=SkeletonTypes.BODY_ONLY)

    armature_outer = generate_armature(
        armature_definition=ArmatureDefinition.create(
            rig_name="test_armature",
            segment_definitions=segment_definitions_outer,
            pose_definition=PoseTypes.DEFAULT_TPOSE,
        )
    )
