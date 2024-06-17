import bpy

from freemocap_blender_addon.models.animation.armatures.bones.armature_bone_constraints import \
    ArmatureBoneConstraintsTypes
from freemocap_blender_addon.models.animation.armatures.bones.bone_constraint_types import ConstraintType


def add_bone_constraints(
        armature: bpy.types.Object,
        bone_constraints: ArmatureBoneConstraintsTypes,
        parent_object: bpy.types.Object,
        use_limit_rotation: bool = False,
) -> None:
    print("Adding bone constraints...")

    # Change to pose mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    # Create each constraint
    for bone_name, constraint_definitions in bone_constraints.items():
        # If pose bone does not exist, skip it
        if bone_name not in armature.pose.bones:
            continue

        for constraint in constraint_definitions:
            # Add new constraint determined by type
            if not use_limit_rotation and constraint.type == ConstraintType.LIMIT_ROTATION:
                continue
            else:
                print(f"Adding constraint {constraint} to bone {bone_name}")
                constraint.apply_constraint(bone=armature.pose.bones[bone_name])
