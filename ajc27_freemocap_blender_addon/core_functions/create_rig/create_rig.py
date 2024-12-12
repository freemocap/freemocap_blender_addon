from typing import Dict

import bpy

from ajc27_freemocap_blender_addon.core_functions.create_rig.add_rig_by_method import add_rig_by_method
from ajc27_freemocap_blender_addon.core_functions.create_rig.add_rig_method_enum import AddRigMethods
from ajc27_freemocap_blender_addon.core_functions.create_rig.apply_bone_constraints import apply_bone_constraints
from ajc27_freemocap_blender_addon.data_models.bones.bone_constraints import Constraint
from ajc27_freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType


def create_rig(
        bone_data: Dict[str, Dict[str, float]],
        rig_name: str,
        parent_object: bpy.types.Object,
        add_rig_method: AddRigMethods = AddRigMethods.BY_BONE,
        keep_symmetry: bool = False,
        add_fingers_constraints: bool = False,
        bone_constraint_definitions=Dict[str, Constraint],
        use_limit_rotation: bool = False,
) -> bpy.types.Object:
    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    rig = add_rig_by_method(add_rig_method=add_rig_method,
                            bone_data=bone_data,
                            keep_symmetry=keep_symmetry,
                            parent_object=parent_object,
                            rig_name=rig_name)
    rig.parent = parent_object
    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # TODO: make sure this still adds constraints properly
    apply_bone_constraints(
        rig=rig,
        add_fingers_constraints=add_fingers_constraints,
        parent_object=parent_object,
        armature_definition=ArmatureType.FREEMOCAP,
        pose_definition=PoseType.FREEMOCAP_TPOSE,
        bone_constraint_definitions=bone_constraint_definitions,

        use_limit_rotation=use_limit_rotation,
    )

    ### Bake animation to the rig ###
    # Get the empties ending frame
    ending_frame = int(bpy.data.actions[0].frame_range[1])
    # Bake animation
    bpy.ops.nla.bake(frame_start=1, frame_end=ending_frame, bake_types={"POSE"})

    # Change back to Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    return rig
