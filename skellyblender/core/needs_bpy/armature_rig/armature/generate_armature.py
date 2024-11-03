import bpy
import mathutils
import numpy as np

from skellyblender.core.needs_bpy.armature_rig.armature.armature_bone_classes import ROOT_BONE_NAME
from skellyblender.core.needs_bpy.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skellyblender.core.needs_bpy.blender_type_hints import ArmatureObject
from skellyblender.core.pure_python.freemocap_data.data_paths.default_path_enums import RightLeftAxial


def generate_armature(armature_definition: ArmatureDefinition) -> ArmatureObject:
    """
    Armature: The geometric representation of a skeleton (i.e. the stick figure definition)
    """

    armature = create_new_armature_and_enter_edit_mode(name=armature_definition.armature_name)

    # loop through the bones to make and skip the ones that don't have a parent yet
    bones_to_make = list(armature_definition.bone_definitions.items())
    any_changed = True
    while len(bones_to_make) > 0:
        if not any_changed:
            raise ValueError(
                f"Infinite loop detected while armature with remaining bones to make: {[f'{bone[0]} (parent: {bone[1].parent})' for bone in bones_to_make]}")
        any_changed = False
        for bone_info in bones_to_make:
            bone_name, bone_definition = bone_info
            if bone_definition.parent not in armature.data.edit_bones:
                continue  # Skip this bone until its parent is created

            bones_to_make.remove(bone_info)  # Remove this bone from the list of bones to make
            any_changed = True

            print(f"Creating armature bone: `{bone_name}` with parent: `{bone_definition.parent}`")
            armature.data.edit_bones.new(name=bone_name)
            armature_bone = armature.data.edit_bones[bone_name]
            assign_armature_bone_color(bone=armature_bone)

            bone_vector = mathutils.Vector([0, 0, bone_definition.length])

            parent_bone = armature.data.edit_bones[bone_definition.parent]

            armature_bone.head = parent_bone.tail
            armature_bone.tail = armature_bone.head + mathutils.Vector(
                        np.array(bone_definition.rest_pose.rotation_matrix) @ np.array(bone_vector))
            armature_bone.roll = bone_definition.rest_pose.roll
            armature_bone.parent = parent_bone
            armature_bone.use_connect = bone_definition.rest_pose.is_connected

    # Change mode to object mode
    bpy.ops.object.mode_set(mode="OBJECT")
    print(f"Armature created successfully: {armature_definition}")
    return armature


def assign_armature_bone_color(bone: bpy.types.EditBone):
    # Check for .L or .R, or axial in the bone name and assign colors accordingly
    if bone.name.endswith(RightLeftAxial.LEFT.blenderize()):
        bone.color.palette = 'THEME04'  # Blue
    elif bone.name.endswith(RightLeftAxial.RIGHT.blenderize()):
        bone.color.palette = 'THEME01'  # Red
    else:
        bone.color.palette = 'THEME03'  # Green


def create_new_armature_and_enter_edit_mode(name: str) -> ArmatureObject:
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
