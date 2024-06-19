import re
from typing import List, Optional, Tuple

import bpy
from freemocap_blender_addon.core_functions.rig.apply_bone_constraints import add_bone_constraints
from freemocap_blender_addon.core_functions.rig.appy_ik_constraints import add_ik_constraints_to_armature
from freemocap_blender_addon.models.animation.armatures.armature_definition import ArmatureDefinition
from freemocap_blender_addon.models.animation.armatures.bones.bone_constraint_types import ConstraintType
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import AddRigConfig

from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints


def generate_rig(
        armature: bpy.types.Object,
        config: AddRigConfig,
) -> Tuple[bpy.types.Object, ArmatureDefinition]:
    """
    Rig: An armature with constraints, drivers, IK, etc
    """
    # Deselect all objects
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")

    root_constraint = armature.constraints.new(type=ConstraintType.COPY_LOCATION.value)
    root_constraint.target = bpy.data.objects[BodyKeypoints.PELVIS_ORIGIN.blenderize()]

    add_bone_constraints(
        armature=armature,
        bone_constraints=config.bone_constraints,
        use_limit_rotation=config.use_limit_rotation,
    )

    if config.add_ik_constraints:
        add_ik_constraints_to_armature(armature=armature)

    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")



    # TODO - I don't really know what the effect of the following code is. Running it returns `Info: Nothing to bake`
    # ### Bake animation to the rig ###
    # # Get the empties ending frame
    # ending_frame = int(bpy.data.actions[0].frame_range[1])
    # # Bake animation
    # bpy.ops.nla.bake(frame_start=0, frame_end=ending_frame, bake_types={"POSE"})

    # Change back to Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    return armature


def deselect_all_bpy_objects():
    for scene_object in bpy.data.objects:
        scene_object.select_set(False)


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
