import bpy
import numpy as np
import math as m
from mathutils import Vector

from ajc27_freemocap_blender_addon.data_models.joint_angles.joint_angles import joint_angles

# TODO: Add multicapture support. Change the joint_angles dict to have the correct scope marker names (left_elbow.001, etc.)
def calculate_joint_angle_info(
    joint_angle_list: list,
    markers: dict,
) -> np.ndarray:
    num_frames = len(markers[joint_angles[joint_angle_list[0]]['joint_center']]['fcurves'][0])
    num_joint_angles = len(joint_angle_list)
    angle_values = np.zeros((num_frames, num_joint_angles))
    reference_vectors = np.zeros((num_frames, num_joint_angles, 3))
    rotation_vectors = np.zeros((num_frames, num_joint_angles, 3))
    rotation_plane_normals = np.zeros((num_frames, num_joint_angles, 3))

    for i, joint_angle in enumerate(joint_angle_list):
        for j in range(num_frames):

            # Rotation plane normal to define rotation angle
            rotation_plane_normal = None

            # Get the reference vector definition
            reference_vector_def = joint_angles[joint_angle]['reference_vector']

            # Get the reference vector
            if joint_angles[joint_angle]['reference_vector']['type'] == 'vector':

                reference_vector_origin_position = get_marker_position(markers, reference_vector_def['reference_vector_origin'], j)
                reference_vector_end_position = get_marker_position(markers, reference_vector_def['reference_vector_end'], j)
                # Calculate the reference vector
                reference_vector = Vector(reference_vector_end_position) - Vector(reference_vector_origin_position)

            elif joint_angles[joint_angle]['reference_vector']['type'] == 'crossproduct':
                
                cross_vector_1_origin_position = get_marker_position(markers, reference_vector_def['reference_cross_1_origin'], j)
                cross_vector_1_end_position = get_marker_position(markers, reference_vector_def['reference_cross_1_end'], j)
                cross_vector_2_origin_position = get_marker_position(markers, reference_vector_def['reference_cross_2_origin'], j)
                cross_vector_2_end_position = get_marker_position(markers, reference_vector_def['reference_cross_2_end'], j)

                # Calculate the cross product
                cross_vector_1 = Vector(cross_vector_1_end_position) - Vector(cross_vector_1_origin_position)
                cross_vector_2 = Vector(cross_vector_2_end_position) - Vector(cross_vector_2_origin_position)
                #  Calculate the reference vector
                reference_vector = cross_vector_1.cross(cross_vector_2)

            elif joint_angles[joint_angle]['reference_vector']['type'] == 'doublecrossproduct':

                cross_vector_1_origin_position = get_marker_position(markers, reference_vector_def['reference_cross_1_origin'], j)
                cross_vector_1_end_position = get_marker_position(markers, reference_vector_def['reference_cross_1_end'], j)
                cross_vector_2_origin_position = get_marker_position(markers, reference_vector_def['reference_cross_2_origin'], j)
                cross_vector_2_end_position = get_marker_position(markers, reference_vector_def['reference_cross_2_end'], j)
                cross_vector_3_origin_position = get_marker_position(markers, reference_vector_def['reference_cross_3_origin'], j)
                cross_vector_3_end_position = get_marker_position(markers, reference_vector_def['reference_cross_3_end'], j)

                # Calculate the cross product
                cross_vector_1 = Vector(cross_vector_1_end_position) - Vector(cross_vector_1_origin_position)
                cross_vector_2 = Vector(cross_vector_2_end_position) - Vector(cross_vector_2_origin_position)
                cross_vector_3 = Vector(cross_vector_3_end_position) - Vector(cross_vector_3_origin_position)
                #  Calculate the reference vector
                reference_vector = cross_vector_1.cross(cross_vector_2).cross(cross_vector_3)

            elif joint_angles[joint_angle]['reference_vector']['type'] == 'average':

                average_vector_1_origin_position = get_marker_position(markers, reference_vector_def['reference_average_1_origin'], j)
                average_vector_1_end_position = get_marker_position(markers, reference_vector_def['reference_average_1_end'], j)
                average_vector_2_origin_position = get_marker_position(markers, reference_vector_def['reference_average_2_origin'], j)
                average_vector_2_end_position = get_marker_position(markers, reference_vector_def['reference_average_2_end'], j)

                # Calculate the average vector
                average_vector_1 = Vector(average_vector_1_end_position) - Vector(average_vector_1_origin_position)
                average_vector_2 = Vector(average_vector_2_end_position) - Vector(average_vector_2_origin_position)
                #  Calculate the reference vector
                reference_vector = (average_vector_1 + average_vector_2) / 2

            else:
                raise ValueError(f"Invalid reference vector type: {joint_angles[joint_angle]['reference_vector']['type']}")

            # Get the rotation vector definition
            rotation_vector_def = joint_angles[joint_angle]['rotation_vector']

            # Get the rotation marker positions
            rotation_vector_origin_position = get_marker_position(markers, rotation_vector_def['rotation_vector_origin'], j)

            # If the rotation_vector_end is just a marker name string
            # then get the vector directly. If not, get the vector as
            # the projection on the projection plane
            if isinstance(rotation_vector_def['rotation_vector_end'], str):
                rotation_vector_end_position = get_marker_position(markers, rotation_vector_def['rotation_vector_end'], j)

            else:
                # Extract definitions
                end_def = joint_angles[joint_angle]['rotation_vector']['rotation_vector_end']

                # Get projected vector
                proj_vec_origin = get_marker_position(markers, end_def['projected_vector_origin'], j)
                proj_vec_end = get_marker_position(markers, end_def['projected_vector_end'], j)

                vec_to_project = proj_vec_end - proj_vec_origin

                # --- Compute plane axes ---

                # Axis 1
                axis1_def = end_def['projection_plane']['plane_axis_1']

                if axis1_def['type'] == 'vector':
                    axis1_origin = get_marker_position(markers, axis1_def['plane_axis_1_origin'], j)
                    axis1_end = get_marker_position(markers, axis1_def['plane_axis_1_end'], j)

                    axis1 = (axis1_end - axis1_origin).normalized()

                elif axis1_def['type'] == 'crossproduct':
                    cp1_origin = get_marker_position(markers, axis1_def['plane_axis_1_cross_1_origin'], j)
                    cp1_end = get_marker_position(markers, axis1_def['plane_axis_1_cross_1_end'], j)
                    cp2_origin = get_marker_position(markers, axis1_def['plane_axis_1_cross_2_origin'], j)
                    cp2_end = get_marker_position(markers, axis1_def['plane_axis_1_cross_2_end'], j)

                    vec1 = cp1_end - cp1_origin
                    vec2 = cp2_end - cp2_origin

                    axis1 = vec1.cross(vec2).normalized()

                elif axis1_def['type'] == 'doublecrossproduct':
                    cp1_origin = get_marker_position(markers, axis1_def['plane_axis_1_cross_1_origin'], j)
                    cp1_end = get_marker_position(markers, axis1_def['plane_axis_1_cross_1_end'], j)
                    cp2_origin = get_marker_position(markers, axis1_def['plane_axis_1_cross_2_origin'], j)
                    cp2_end = get_marker_position(markers, axis1_def['plane_axis_1_cross_2_end'], j)
                    cp3_origin = get_marker_position(markers, axis1_def['plane_axis_1_cross_3_origin'], j)
                    cp3_end = get_marker_position(markers, axis1_def['plane_axis_1_cross_3_end'], j)

                    vec1 = cp1_end - cp1_origin
                    vec2 = cp2_end - cp2_origin
                    vec3 = cp3_end - cp3_origin

                    axis1 = vec1.cross(vec2).cross(vec3).normalized()

                elif axis1_def['type'] == 'average':
                    cp1_origin = get_marker_position(markers, axis1_def['plane_axis_1_average_1_origin'], j)
                    cp1_end = get_marker_position(markers, axis1_def['plane_axis_1_average_1_end'], j)
                    cp2_origin = get_marker_position(markers, axis1_def['plane_axis_1_average_2_origin'], j)
                    cp2_end = get_marker_position(markers, axis1_def['plane_axis_1_average_2_end'], j)

                    vec1 = cp1_end - cp1_origin
                    vec2 = cp2_end - cp2_origin

                    axis1 = (vec1 + vec2) / 2

                else:
                    raise ValueError("Unsupported axis1 type")

                # Axis 2
                axis2_def = end_def['projection_plane']['plane_axis_2']
                if axis2_def['type'] == 'vector':
                    axis2_origin = get_marker_position(markers, axis2_def['plane_axis_2_origin'], j)
                    axis2_end = get_marker_position(markers, axis2_def['plane_axis_2_end'], j)

                    axis2 = (axis2_end - axis2_origin).normalized()

                elif axis2_def['type'] == 'crossproduct':
                    cp1_origin = get_marker_position(markers, axis2_def['plane_axis_2_cross_1_origin'], j)
                    cp1_end = get_marker_position(markers, axis2_def['plane_axis_2_cross_1_end'], j)
                    cp2_origin = get_marker_position(markers, axis2_def['plane_axis_2_cross_2_origin'], j)
                    cp2_end = get_marker_position(markers, axis2_def['plane_axis_2_cross_2_end'], j)

                    vec1 = (cp1_end - cp1_origin).normalized()
                    vec2 = (cp2_end - cp2_origin).normalized()

                    axis2 = vec1.cross(vec2).normalized()

                elif axis2_def['type'] == 'doublecrossproduct':
                    cp1_origin = get_marker_position(markers, axis2_def['plane_axis_2_cross_1_origin'], j)
                    cp1_end = get_marker_position(markers, axis2_def['plane_axis_2_cross_1_end'], j)
                    cp2_origin = get_marker_position(markers, axis2_def['plane_axis_2_cross_2_origin'], j)
                    cp2_end = get_marker_position(markers, axis2_def['plane_axis_2_cross_2_end'], j)
                    cp3_origin = get_marker_position(markers, axis2_def['plane_axis_2_cross_3_origin'], j)
                    cp3_end = get_marker_position(markers, axis2_def['plane_axis_2_cross_3_end'], j)

                    vec1 = (cp1_end - cp1_origin).normalized()
                    vec2 = (cp2_end - cp2_origin).normalized()
                    vec3 = (cp3_end - cp3_origin).normalized()

                    axis2 = vec1.cross(vec2).cross(vec3).normalized()

                elif axis2_def['type'] == 'average':
                    cp1_origin = get_marker_position(markers, axis2_def['plane_axis_2_average_1_origin'], j)
                    cp1_end = get_marker_position(markers, axis2_def['plane_axis_2_average_1_end'], j)
                    cp2_origin = get_marker_position(markers, axis2_def['plane_axis_2_average_2_origin'], j)
                    cp2_end = get_marker_position(markers, axis2_def['plane_axis_2_average_2_end'], j)

                    vec1 = (cp1_end - cp1_origin).normalized()
                    vec2 = (cp2_end - cp2_origin).normalized()

                    axis2 = (vec1 + vec2) / 2

                elif axis2_def['type'] == 'average_crossproduct':
                    cp1_origin = get_marker_position(markers, axis2_def['plane_axis_2_average_1_origin'], j)
                    cp1_end = get_marker_position(markers, axis2_def['plane_axis_2_average_1_end'], j)
                    cp2_origin = get_marker_position(markers, axis2_def['plane_axis_2_average_2_origin'], j)
                    cp2_end = get_marker_position(markers, axis2_def['plane_axis_2_average_2_end'], j)
                    cp3_origin = get_marker_position(markers, axis2_def['plane_axis_2_cross_1_origin'], j)
                    cp3_end = get_marker_position(markers, axis2_def['plane_axis_2_cross_1_end'], j)

                    vec1 = (cp1_end - cp1_origin).normalized()
                    vec2 = (cp2_end - cp2_origin).normalized()
                    avg = (vec1 + vec2) / 2

                    vec3 = (cp3_end - cp3_origin).normalized()

                    axis2 = avg.cross(vec3).normalized()                    

                else:
                    raise ValueError("Unsupported axis2 type")

                # --- Project vector onto plane ---

                # Define plane
                plane_normal = axis1.cross(axis2).normalized()
                vec_proj = vec_to_project - plane_normal * vec_to_project.dot(plane_normal)

                # Final projected position
                rotation_vector_end_position = proj_vec_origin + vec_proj

                # Assign the plane normal as rotation_plane_normal
                rotation_plane_normal = plane_normal

            
            # Calculate the rotation vector
            rotation_vector = rotation_vector_end_position - rotation_vector_origin_position

            # Get the cross product of the reference vector and the rotation vector
            cross_product = reference_vector.cross(rotation_vector)

            # In case rotation_plane_normal is None then set it as the cross product
            # TODO: Change this to a better plane normal for joints like elbows and knees as there won't be negative values
            if rotation_plane_normal is None:
                rotation_plane_normal = cross_product

            rotation_angle = m.degrees(rotation_vector.angle(reference_vector))

            if cross_product.dot(rotation_plane_normal) < 0:
                rotation_angle = -rotation_angle

            angle_values[j, i] = rotation_angle
            reference_vectors[j, i, :] = np.array(reference_vector)
            # Rotation vectors are not used downstream but left them for now,
            # easier for debugging
            rotation_vectors[j, i, :] = np.array(rotation_vector)
            rotation_plane_normals[j, i, :] = np.array(rotation_plane_normal)

    return angle_values, reference_vectors, rotation_vectors, rotation_plane_normals


def get_marker_position(
    markers_dict: dict,
    marker_name: str,
    frame: int,
    ):
    return Vector([
        markers_dict[marker_name]['fcurves'][0][frame],
        markers_dict[marker_name]['fcurves'][1][frame],
        markers_dict[marker_name]['fcurves'][2][frame],
    ])
