import re
from typing import List, Optional

import bpy

from freemocap_blender_addon.core_functions.rig.generate_armature import generate_armature
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.models.animation.armatures.armature_definition import ArmatureDefinition
from freemocap_blender_addon.models.animation.armatures.rest_pose.pose_types import PoseTypes
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import AddRigConfig


def generate_rig(
        rig_name: str,
        segment_definitions: RigidSegmentDefinitions,
        pose_definition: PoseTypes,
        parent_object: bpy.types.Object,
        config: AddRigConfig,
) -> bpy.types.Object:
    """
    Armature - bone lengths and rest pose definitions which define the basic structure of the skeleton
    Rig - Armature + constraints, IK, drivers, etc
    """
    # Deselect all objects
    deselect_all_bpy_objects()

    print("Generating armature from segment legnths and rest pose defintions...")
    armature = generate_armature(armature_definition=ArmatureDefinition.create(
        rig_name=rig_name,
        segment_definitions=segment_definitions,
        pose_definition=pose_definition,
    ))

    # add_ik_constraints_to_rig(rig)

    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # add_constraints(
    #     rig=rig,
    #     add_fingers_constraints=config.add_fingers_constraints,
    #     parent_object=parent_object,
    #     armature=config.armature_type,
    #     pose=config.pose_type,
    #     use_limit_rotation=config.use_limit_rotation,
    # )

    ### Bake animation to the rig ###
    # Get the empties ending frame
    ending_frame = int(bpy.data.actions[0].frame_range[1])
    # Bake animation
    bpy.ops.nla.bake(frame_start=1, frame_end=ending_frame, bake_types={"POSE"})

    # Change back to Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    # return rig


def deselect_all_bpy_objects():
    for object in bpy.data.objects:
        object.select_set(False)


def get_appended_number_from_blender_object(base_name: str) -> Optional[str]:
    pattern = r"\.0[0-9]{2}$"
    match = re.search(pattern, base_name)
    return match.group() if match else None


def get_actual_empty_target_name(empty_names: List[str], base_target_name: str) -> str:
    """
    Get the actual empty target name based on the constraint target name,
    this is mostly to give us the ability to load multiple recorings, because
    blender will append `.001`, `.002`  the names of emtpies of the 2nd, 3rd, etc to avoid name collisions

    So basically, if the base_target name is `hips_center` this will look for empties named `hips_center`,
      `hips_center.001`, `hips_center.002`, etc in the provided `empty_names` list and return that
    """

    actual_target_name = None
    for empty_name in empty_names:
        if base_target_name in empty_name:
            actual_target_name = empty_name
            break

    if actual_target_name is None:
        raise ValueError(f"Could not find empty target for {base_target_name}")

    return actual_target_name
