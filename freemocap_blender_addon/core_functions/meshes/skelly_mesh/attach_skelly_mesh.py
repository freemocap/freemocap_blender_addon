import traceback
from pathlib import Path
from typing import Dict

import bpy
from mathutils import Vector, Matrix, Euler

from freemocap_blender_addon import PACKAGE_ROOT_PATH
from freemocap_blender_addon.models.animation.armatures import (
    bone_name_map,
)
from freemocap_blender_addon.models.animation.meshes.skelly_bones import SKELLY_BONES

SKELLY_BONE_MESHES_PATH = str(Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones")


def attach_skelly_bone_meshes(rig: bpy.types.Object) -> None:
    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    #  Set the rig as active object
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig

    # Change to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    #  Iterate through the skelly bones dictionary and update the
    #  default origin, length and normalized direction
    for mesh in SKELLY_BONES:
        SKELLY_BONES[mesh].bones_origin = Vector(
            rig.data.edit_bones[bone_name_map[rig.name][SKELLY_BONES[mesh].bones[0]]].head)
        SKELLY_BONES[mesh].bones_end = Vector(
            rig.data.edit_bones[bone_name_map[rig.name][SKELLY_BONES[mesh].bones[-1]]].tail)
        SKELLY_BONES[mesh].bones_length = (SKELLY_BONES[mesh].bones_end - SKELLY_BONES[mesh].bones_origin).length

    # Change to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Define the list that will contain the different Skelly meshes
    skelly_meshes = []

    # Iterate through the skelly bones dictionary and add the correspondent skelly mesh
    for mesh in SKELLY_BONES:
        print("Adding Skelly_" + mesh + " mesh...")
        try:
            # Import the skelly mesh
            mesh_path = SKELLY_BONE_MESHES_PATH + '/Skelly_' + mesh + '.fbx'
            if not Path(mesh_path).is_file():
                raise FileNotFoundError(f"Could not find skelly mesh at {mesh_path}")
            bpy.ops.import_scene.fbx(filepath=str(mesh_path))

        except Exception as e:
            print(f"Error while importing skelly mesh: {e}")
            print(traceback.format_exc())
            continue

        skelly_meshes.append(bpy.data.objects['Skelly_' + mesh])

        # Get reference to the imported mesh
        skelly_mesh = bpy.data.objects['Skelly_' + mesh]

        # Get the rotation matrix
        if mesh == 'head':
            rotation_matrix = Matrix.Identity(4)
        else:
            rotation_matrix = Euler(
                Vector(pose[bone_name_map[rig.name][mesh]].rotation),
                'XYZ',
            ).to_matrix()

        # Move the Skelly part to the equivalent bone's head location
        skelly_mesh.location = (SKELLY_BONES[mesh].bones_origin
                                + rotation_matrix @ Vector(SKELLY_BONES[mesh].position_offset)
                                )

        # Rotate the part mesh with the rotation matrix
        skelly_mesh.rotation_euler = rotation_matrix.to_euler('XYZ')

        # Get the bone length
        if SKELLY_BONES[mesh].adjust_rotation:
            bone_length = (SKELLY_BONES[mesh].bones_end - (SKELLY_BONES[mesh].bones_origin + (
                    rotation_matrix @ Vector(SKELLY_BONES[mesh].position_offset)))).length
        elif mesh == 'head':
            # bone_length = rig.data.edit_bones[bone_name_map[armature_name][SKELLY_BONES[mesh]['bones'][0]]].length
            bone_length = SKELLY_BONES['spine'].bones_length / 3.123  # Head length to spine length ratio
        else:
            bone_length = SKELLY_BONES[mesh].bones_length

        # Get the mesh length
        mesh_length = SKELLY_BONES[mesh].mesh_length

        # Resize the Skelly part to match the bone length
        skelly_mesh.scale = (bone_length / mesh_length, bone_length / mesh_length, bone_length / mesh_length)

        # Adjust rotation if necessary
        if SKELLY_BONES[mesh].adjust_rotation:
            # Save the Skelly part's original location
            part_location = Vector(skelly_mesh.location)

            # Get the direction vector
            bone_vector = SKELLY_BONES[mesh].bones_end - SKELLY_BONES[mesh].bones_origin
            # Get new bone vector after applying the position offset
            new_bone_vector = SKELLY_BONES[mesh].bones_end - part_location

            # Apply the rotations to the Skelly part
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

            # Get the angle between the two vectors
            rotation_quaternion = bone_vector.rotation_difference(new_bone_vector)
            # Change the rotation mode
            skelly_mesh.rotation_mode = 'QUATERNION'
            # Rotate the Skelly part
            skelly_mesh.rotation_quaternion = rotation_quaternion

        # Apply the transformations to the Skelly part
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Rename the first mesh to skelly_mesh
    skelly_meshes[0].name = "skelly_mesh"

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select all body meshes
    for skelly_mesh in skelly_meshes:
        skelly_mesh.select_set(True)

    # Set skelly_mesh as active
    bpy.context.view_layer.objects.active = skelly_meshes[0]

    # Join the body meshes
    bpy.ops.object.join()

    # Select the rig
    rig.select_set(True)
    # Set rig as active
    bpy.context.view_layer.objects.active = rig
    # Parent the mesh and the rig with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')


