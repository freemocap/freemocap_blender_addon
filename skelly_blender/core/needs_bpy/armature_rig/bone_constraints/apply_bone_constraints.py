from typing import Tuple

import bpy

from skelly_blender.core.needs_bpy.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skelly_blender.core.needs_bpy.armature_rig.bone_constraints.armature_bone_constraints_types import \
    ArmatureBoneConstraintsTypes
from skelly_blender.core.needs_bpy.armature_rig.bone_constraints.bone_constraint_types import ConstraintType
from skelly_blender.core.needs_bpy.blenderizers.blenderized_skeleton_data import parentify_name
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.pipelines.blender_pipeline_config import AddRigConfig


def apply_bone_constraints(
        armature: bpy.types.Object,
        config: AddRigConfig,
        parent_name: str,
) -> Tuple[bpy.types.Object, ArmatureDefinition]:
    """
    Rig: An armature with constraints, drivers, IK, etc
    """
    # Deselect all objects
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")

    root_constraint = armature.constraints.new(type=ConstraintType.COPY_LOCATION.value)
    root_constraint.target = bpy.data.objects[parentify_name(name=BodyKeypoints.PELVIS_SPINE_SACRUM_ORIGIN.blenderize(),
                                                             parent_name=parent_name)]

    add_bone_constraints(
        armature=armature,
        bone_constraints=config.bone_constraints,
        use_limit_rotation=config.use_limit_rotation,
    )

    if config.add_ik_constraints:
        raise NotImplementedError("IK constraints are not implemented yet")
        # from old.freemocap_blender_addon.core_functions.rig.appy_ik_constraints import add_ik_constraints_to_armature
        # add_ik_constraints_to_armature(armature=armature)

    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # TODO - I don't really know what 'baking animation to rig' does, so I don't know if the following code is necessary. Running it returns a warning `Info: Nothing to bake` which doesn't seem to affect the anything?
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


def add_bone_constraints(
        armature: bpy.types.Object,
        bone_constraints: ArmatureBoneConstraintsTypes,
        use_limit_rotation: bool = False,
) -> None:
    print("Adding bone constraints...")

    # Change to pose mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    # Create each constraint
    for bone_name, constraint_definitions in bone_constraints.value.__members__.items():
        # If pose bone does not exist, skip it
        if bone_name not in armature.pose.bones:
            continue

        print(f"\nAdding constraints to bone `{bone_name}`")
        for constraint in constraint_definitions.value:
            # Add new constraint determined by type
            if not use_limit_rotation and constraint.type == ConstraintType.LIMIT_ROTATION.value:
                continue
            else:
                print(f"\t-> {constraint}")
                constraint.apply_constraint(bone=armature.pose.bones[bone_name])
