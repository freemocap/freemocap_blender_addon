import bpy
import numpy as np
import math as m
from mathutils import Vector

from ajc27_freemocap_blender_addon.data_models.joint_angles.joint_angles import joint_angles


def calculate_joint_angle_info(
    joint_angle_list: list,
    markers: dict,
) -> np.ndarray:
    num_frames = len(markers[joint_angles[joint_angle_list[0]]['joint_center']]['fcurves'][0])
    num_joint_angles = len(joint_angle_list)
    angle_values = np.zeros((num_frames, num_joint_angles))
    reference_vectors = np.zeros((num_frames, num_joint_angles, 3))
    rotation_vectors = np.zeros((num_frames, num_joint_angles, 3))
    cross_products = np.zeros((num_frames, num_joint_angles, 3))

    for i, joint_angle in enumerate(joint_angle_list):
        for j in range(num_frames):
            # Get the reference marker positions
            reference_vector_origin_marker = joint_angles[joint_angle]['reference_vector']['reference_vector_origin']
            reference_vector_origin_position = [
                markers[reference_vector_origin_marker]['fcurves'][0][j],
                markers[reference_vector_origin_marker]['fcurves'][1][j],
                markers[reference_vector_origin_marker]['fcurves'][2][j],
            ]

            reference_vector_end_marker = joint_angles[joint_angle]['reference_vector']['reference_vector_end']
            reference_vector_end_position = [
                markers[reference_vector_end_marker]['fcurves'][0][j],
                markers[reference_vector_end_marker]['fcurves'][1][j],
                markers[reference_vector_end_marker]['fcurves'][2][j],
            ]

            reference_vector = Vector(reference_vector_end_position) - Vector(reference_vector_origin_position)

            # Get the rotation marker positions
            rotation_vector_origin_marker = joint_angles[joint_angle]['rotation_vector']['rotation_vector_origin']
            rotation_vector_origin_position = [
                markers[rotation_vector_origin_marker]['fcurves'][0][j],
                markers[rotation_vector_origin_marker]['fcurves'][1][j],
                markers[rotation_vector_origin_marker]['fcurves'][2][j],
            ]

            # If the rotation_vector_end is just a marker name string
            # then get the vector directly. If not, get the vector as
            # the projection on the projection plane
            if isinstance(joint_angles[joint_angle]['rotation_vector']['rotation_vector_end'], str):
                rotation_vector_end_marker = joint_angles[joint_angle]['rotation_vector']['rotation_vector_end']
                rotation_vector_end_position = [
                    markers[rotation_vector_end_marker]['fcurves'][0][j],
                    markers[rotation_vector_end_marker]['fcurves'][1][j],
                    markers[rotation_vector_end_marker]['fcurves'][2][j],
                ]
            else:
                pass

            rotation_vector = Vector(rotation_vector_end_position) - Vector(rotation_vector_origin_position)

            # Get the cross product of the reference vector and the rotation vector
            cross_product = Vector(reference_vector.cross(rotation_vector))

            # calculate the rotation needed to align the cross product with (0, 0, 1)
            rotation_quaternion = cross_product.rotation_difference(Vector((0, 0, 1)))
                
            reference_vector_xy_aligned = rotation_quaternion @ reference_vector
            rotation_vector_xy_aligned = rotation_quaternion @ rotation_vector

            reference_vector_2D = Vector(reference_vector_xy_aligned[:2])
            rotation_vector_2D = Vector(rotation_vector_xy_aligned[:2])

            print(f"Reference vector: {reference_vector}")
            print(f"Rotation vector: {rotation_vector}")
            print(f"Cross product: {cross_product}")
            print(f"Rotation quaternion: {rotation_quaternion}")
            print(f"Reference vector 2D: {reference_vector_2D}")
            print(f"Rotation vector 2D: {rotation_vector_2D}")
            
            rotation_angle = m.degrees(rotation_vector_2D.angle_signed(reference_vector_2D))

            angle_values[j, i] = rotation_angle
            reference_vectors[j, i, :] = np.array(reference_vector)
            rotation_vectors[j, i, :] = np.array(rotation_vector)
            cross_products[j, i, :] = np.array(cross_product)

    return angle_values, reference_vectors, rotation_vectors, cross_products
