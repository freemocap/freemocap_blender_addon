import csv
from pathlib import Path
from typing import Dict, List

import bpy

from ajc27_freemocap_blender_addon.data_models.bones.bone_constraints import get_bone_constraint_definitions


def save_bone_and_joint_angles_from_rig(rig: bpy.types.Object,
                                        bone_names: List[str],
                                        csv_save_path: str,
                                        start_frame: int,
                                        end_frame: int):
    Path(csv_save_path).parent.mkdir(parents=True, exist_ok=True)
    documentation_save_path = Path(csv_save_path).parent / "_BONE_AND_JOINT_DATA_README.md"

    if rig.type != 'ARMATURE':
        raise TypeError(f"`rig` is not an armature!")
    all_bone_data = {}
    for frame_number in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame_number)
        frame_data = {}
        all_bone_data[frame_number] = frame_data
        for bone in rig.pose.bones:
            if bone.name not in bone_names:
                continue
            frame_data[bone.name] = get_bone_data(bone)

    # Save as csv
    column_names = []
    for bone_key in all_bone_data[0].keys():
        for data_name in list(next(iter(frame_data.values())).keys()):
            column_names.append(f"{bone_key}_{data_name}")

    with open(csv_save_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writeheader()
        for frame_data in all_bone_data.values():
            row_data = []
            for bone_data in frame_data.values():
                row_data.extend(bone_data.values())
            column_data_mappping = dict(zip(column_names, row_data))
            writer.writerow(column_data_mappping)

    # Save documentation
    with open(documentation_save_path, 'w') as file:
        file.write(DOCUMENTATION_STRING)


def get_bone_data(bone: bpy.types.PoseBone) -> Dict[str, float]:
    return {
        "head_center_world_x": bone.head.x,
        "head_center_world_y": bone.head.y,
        "head_center_world_z": bone.head.z,
        "tail_center_world_x": bone.tail.x,
        "tail_center_world_y": bone.tail.y,
        "tail_center_world_z": bone.tail.z,
        "rotation_quaternion_x": bone.matrix.to_quaternion().x,
        "rotation_quaternion_y": bone.matrix.to_quaternion().y,
        "rotation_quaternion_z": bone.matrix.to_quaternion().z,
        "rotation_quaternion_w": bone.matrix.to_quaternion().w,
        "rotation_euler_x": bone.matrix.to_euler().x,
        "rotation_euler_y": bone.matrix.to_euler().y,
        "rotation_euler_z": bone.matrix.to_euler().z,
        "rotation_euler_order": bone.matrix.to_euler().order,
        "matrix_0_0": bone.matrix[0][0],
        "matrix_0_1": bone.matrix[0][1],
        "matrix_0_2": bone.matrix[0][2],
        "matrix_0_3": bone.matrix[0][3],
        "matrix_1_0": bone.matrix[1][0],
        "matrix_1_1": bone.matrix[1][1],
        "matrix_1_2": bone.matrix[1][2],
        "matrix_1_3": bone.matrix[1][3],
        "matrix_2_0": bone.matrix[2][0],
        "matrix_2_1": bone.matrix[2][1],
        "matrix_2_2": bone.matrix[2][2],
        "matrix_2_3": bone.matrix[2][3],
        "matrix_3_0": bone.matrix[3][0],
        "matrix_3_1": bone.matrix[3][1],
        "matrix_3_2": bone.matrix[3][2],
        "matrix_3_3": bone.matrix[3][3],
    }


DOCUMENTATION_STRING = """
# Bone data

This document describes the data that is saved for each bone in the rig.

All of this data is derived from a Blender Armature object based on a slightly tweaked version of the Rigify rig.

For multi-part data (e.g. XYZ location), each component of the data is saved in its own column: e.g. {bone_name}_x, {bone_name}_y, {bone_name}_z 

To access the bone data in Blender, use the following command (e.g. to get the Thigh.L bone) in the Blender python console (e.g. in the Scripting Tab): `bone = bpy.context.object["righ"].pose.bone["thigh.L"]`

Theses are the properties of the bone object that are saved:

# Bone Properties

## `bone.head` : location data - X, Y, Z (tuple of floats)
The location of the head of the bone in world space (e.g. (0.0, 0.0, 0.0))
https://docs.blender.org/api/current/bpy.types.PoseBone.html#bpy.types.PoseBone.head

## `bone.tail` : location data - X, Y, Z (tuple of floats)
The location of the tail of the bone in world space (e.g. (0.0, 0.0, 0.0))
https://docs.blender.org/api/current/bpy.types.PoseBone.html#bpy.types.PoseBone.tail


## `bone.rotation_quaternion['_x', '_y', '_z', '_w']` : quaternion - X, Y, Z, W (tuple of floats)
The rotation of the bone in quaternion space (e.g. (0.0, 0.0, 0.0, 1.0))
https://docs.blender.org/api/current/bpy.types.PoseBone.html#bpy.types.PoseBone.rotation_quaternion
https://en.wikipedia.org/wiki/Quaternion

## `bone.rotation_euler['_x', '_y', '_z']` : euler rotation - X, Y, Z (tuple of floats)
The rotation of the bone in euler space (e.g. (0.0, 0.0, 0.0))
https://docs.blender.org/api/current/bpy.types.PoseBone.html#bpy.types.PoseBone.rotation_euler
https://en.wikipedia.org/wiki/Euler_angles

## `bone.rotation_euler.order` : str
The order of the euler rotation (e.g. 'XYZ')
https://docs.blender.org/api/current/bpy.types.PoseBone.html#bpy.types.PoseBone.rotation_euler
https://en.wikipedia.org/wiki/Euler_angles

## `bone.matrix` : 4x4 matrix (tuple of tuples of floats)
The transformation matrix of the bone in world space after constraints and drivers are applied, in the armature object space
https://docs.blender.org/api/current/bpy.types.PoseBone.html#bpy.types.PoseBone.matrix
https://en.wikipedia.org/wiki/Transformation_matrix

"""
