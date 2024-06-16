import bpy
import mathutils

from freemocap_blender_addon.core_functions.rig.appy_ik_to_rig import add_ik_constraints_to_rig
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.models.animation.armatures.rest_pose import PoseTypes
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name


def add_rig_by_bone(
        rig_name: str,
        segment_definitions: RigidSegmentDefinitions,
        pose_definition: PoseTypes,
        skeleton_definition: SkeletonTypes,
        add_ik_constraints: bool,
) -> bpy.types.Object:
    print("Adding rig to scene bone by bone...")

    rig = create_new_armature_rig(name=rig_name, enter_edit_mode=True)
    while not armature_bone_names <= list(rig.data.edit_bones.keys()):  # check if all bones are in the rig, iterate until all bones are in the rig
        for segment_name, segment in segment_definitions.items():

            if blenderize_name(segment_name) in rig.data.edit_bones.keys():
                # If the bone already exists, we can skip it
                continue

            if blenderize_name(segment_name) not in pose_definition.value.__members__.keys():
                continue

            if blenderize_name(segment.parent) not in rig.data.edit_bones.keys():
                #TODO - this is bonkers. I am certainly doing something wrong with the enums and whatnot here lol
                if not pose_definition.value.__members__[blenderize_name(segment_name)].value.is_root:
                    # If the parent bone does not exist yet, skip this iteration
                    continue

            # Add the new bone
            rig_bone = rig.data.edit_bones.new(blenderize_name(segment_name))

            if pose_definition.value.__members__[blenderize_name(segment_name)].value.is_root:
                rig_bone.head = mathutils.Vector([0, 0, 0])
            else:
                # Set the bone head position relative to its parent
                rig_bone.head = rig.data.edit_bones[blenderize_name(segment.parent)].tail

            bone_vector = mathutils.Vector(
                [0, 0, segment_definitions[blenderize_name(segment_name)].length]
            )

            # Get the rotation matrix
            rotation_matrix = mathutils.Euler(
                mathutils.Vector(pose_definition.value.__members__[blenderize_name(segment_name)].value.rotation),
                "XYZ",
            ).to_matrix()

            # Set the tail position
            rig_bone.tail = rig_bone.head + rotation_matrix @ bone_vector

            rig_bone.parent = rig.data.edit_bones[blenderize_name(segment.parent)]
            rig_bone.use_connect = pose_definition.value.__members__[blenderize_name(segment_name)].value.is_connected

    # Add the ik bones if specified
    if add_ik_constraints:
        add_ik_constraints_to_rig(rig)

    return rig


def create_new_armature_rig(name: str, enter_edit_mode:bool=True) -> bpy.types.Object:
    # Add the armature
    bpy.ops.object.armature_add(
        enter_editmode=enter_edit_mode,
        align="WORLD",
        location=(0, 0, 0),
    )
    # Rename the armature
    bpy.data.armatures[0].name = name
    # Get the armature object
    rig = bpy.data.objects["Armature"]
    # Rename the armature object
    rig.name = name
    # Remove the default bone
    rig.data.edit_bones.remove(rig.data.edit_bones["Bone"])
    return rig

if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_test_recording
    from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
        calculate_rigid_body_trajectories

    recording_data = load_freemocap_test_recording()
    keypoint_trajectories_outer, segment_definitions_outer = calculate_rigid_body_trajectories(
        keypoint_trajectories=recording_data.body.map_to_keypoints(),
        skeleton_definition=SkeletonTypes.BODY_ONLY)
    add_rig_by_bone(
        rig_name="test_rig",
        segment_definitions=segment_definitions_outer,
        pose_definition=PoseTypes.FREEMOCAP_TPOSE,
        skeleton_definition=SkeletonTypes.BODY_ONLY,
        add_ik_constraints=True,
    )
