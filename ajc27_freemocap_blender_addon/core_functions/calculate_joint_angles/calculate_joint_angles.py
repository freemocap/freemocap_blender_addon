import numpy as np
import math as m
from mathutils import Vector

from ajc27_freemocap_blender_addon.core_functions.calculate_joint_angles.joint_angle_definitions import joint_angles

def calculate_joint_angles(
    output_path: str,
    marker_names: list,
    marker_frame_xyz: np.ndarray
):
    print("Calculating joint angles...")

    angle_list = list(joint_angles.keys())
    # Initialize an array to hold the angle values with nans
    angle_values = np.full((marker_frame_xyz.shape[0], len(angle_list)), np.nan)

    for joint_angle in joint_angles:
        for frame in range(marker_frame_xyz.shape[0]):

            # Rotation plane normal to define rotation angle sign
            rotation_plane_normal = None

            # Get the reference vector definition
            reference_vector_def = joint_angles[joint_angle]['reference_vector']

            # Get the reference vector
            if joint_angles[joint_angle]['reference_vector']['type'] == 'vector':
                reference_vector_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_vector_origin'])]
                reference_vector_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_vector_end'])]
            
                # Calculate the reference vector
                reference_vector = Vector(reference_vector_end_position) - Vector(reference_vector_origin_position)

            elif joint_angles[joint_angle]['reference_vector']['type'] == 'crossproduct':

                cross_vector_1_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_1_origin'])]
                cross_vector_1_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_1_end'])]
                cross_vector_2_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_2_origin'])]
                cross_vector_2_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_2_end'])]

                # Calculate the cross product
                cross_vector_1 = Vector(cross_vector_1_end_position) - Vector(cross_vector_1_origin_position)
                cross_vector_2 = Vector(cross_vector_2_end_position) - Vector(cross_vector_2_origin_position)
                #  Calculate the reference vector
                reference_vector = cross_vector_1.cross(cross_vector_2)

            elif joint_angles[joint_angle]['reference_vector']['type'] == 'doublecrossproduct':

                cross_vector_1_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_1_origin'])]
                cross_vector_1_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_1_end'])]
                cross_vector_2_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_2_origin'])]
                cross_vector_2_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_2_end'])]
                cross_vector_3_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_3_origin'])]
                cross_vector_3_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_cross_3_end'])]

                # Calculate the cross product
                cross_vector_1 = Vector(cross_vector_1_end_position) - Vector(cross_vector_1_origin_position)
                cross_vector_2 = Vector(cross_vector_2_end_position) - Vector(cross_vector_2_origin_position)
                cross_vector_3 = Vector(cross_vector_3_end_position) - Vector(cross_vector_3_origin_position)
                # Calculate the reference vector
                reference_vector = cross_vector_1.cross(cross_vector_2).cross(cross_vector_3)

            elif joint_angles[joint_angle]['reference_vector']['type'] == 'average':

                average_vector_1_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_average_1_origin'])]
                average_vector_1_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_average_1_end'])]
                average_vector_2_origin_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_average_2_origin'])]
                average_vector_2_end_position = marker_frame_xyz[frame, marker_names.index(reference_vector_def['reference_average_2_end'])]

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
            rotation_vector_origin_position = marker_frame_xyz[
                frame, marker_names.index(rotation_vector_def['rotation_vector_origin'])
            ]

            # If the rotation_vector_end is just a marker name string
            # then get the vector directly. If not, get the vector as
            # the projection on the projection plane
            if isinstance(rotation_vector_def['rotation_vector_end'], str):
                rotation_vector_end_position = marker_frame_xyz[
                    frame, marker_names.index(rotation_vector_def['rotation_vector_end'])
                ]

            else:
                # Extract definitions
                end_def = joint_angles[joint_angle]['rotation_vector']['rotation_vector_end']

                # Get projected vector
                proj_vec_origin = marker_frame_xyz[frame, marker_names.index(end_def['projected_vector_origin'])]
                proj_vec_end = marker_frame_xyz[frame, marker_names.index(end_def['projected_vector_end'])]
                
                vec_to_project = proj_vec_end - proj_vec_origin

                # --- Compute plane axes ---

                # Axis 1
                axis1_def = end_def['projection_plane']['plane_axis_1']

                if axis1_def['type'] == 'vector':
                    axis1_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_origin'])]
                    axis1_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_end'])]

                    axis1 = (Vector(axis1_end) - Vector(axis1_origin)).normalized()

                elif axis1_def['type'] == 'crossproduct':
                    cp1_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_1_origin'])]
                    cp1_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_1_end'])]
                    cp2_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_2_origin'])]
                    cp2_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_2_end'])]

                    vec1 = Vector(cp1_end) - Vector(cp1_origin)
                    vec2 = Vector(cp2_end) - Vector(cp2_origin)

                    axis1 = vec1.cross(vec2).normalized()

                elif axis1_def['type'] == 'doublecrossproduct':
                    cp1_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_1_origin'])]
                    cp1_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_1_end'])]
                    cp2_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_2_origin'])]
                    cp2_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_2_end'])]
                    cp3_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_3_origin'])]
                    cp3_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_cross_3_end'])]

                    vec1 = Vector(cp1_end) - Vector(cp1_origin)
                    vec2 = Vector(cp2_end) - Vector(cp2_origin)
                    vec3 = Vector(cp3_end) - Vector(cp3_origin)

                    axis1 = vec1.cross(vec2).cross(vec3).normalized()

                elif axis1_def['type'] == 'average':
                    cp1_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_average_1_origin'])]
                    cp1_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_average_1_end'])]
                    cp2_origin = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_average_2_origin'])]
                    cp2_end = marker_frame_xyz[frame, marker_names.index(axis1_def['plane_axis_1_average_2_end'])]

                    vec1 = Vector(cp1_end) - Vector(cp1_origin)
                    vec2 = Vector(cp2_end) - Vector(cp2_origin)

                    axis1 = (vec1 + vec2) / 2

                else:
                    raise ValueError("Unsupported axis1 type")

                # Axis 2
                axis2_def = end_def['projection_plane']['plane_axis_2']
                if axis2_def['type'] == 'vector':
                    axis2_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_origin'])]
                    axis2_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_end'])]

                    axis2 = (Vector(axis2_end) - Vector(axis2_origin)).normalized()

                elif axis2_def['type'] == 'crossproduct':
                    cp1_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_1_origin'])]
                    cp1_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_1_end'])]
                    cp2_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_2_origin'])]
                    cp2_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_2_end'])]

                    vec1 = (Vector(cp1_end) - Vector(cp1_origin)).normalized()
                    vec2 = (Vector(cp2_end) - Vector(cp2_origin)).normalized()

                    axis2 = vec1.cross(vec2).normalized()

                elif axis2_def['type'] == 'doublecrossproduct':
                    cp1_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_1_origin'])]
                    cp1_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_1_end'])]
                    cp2_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_2_origin'])]
                    cp2_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_2_end'])]
                    cp3_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_3_origin'])]
                    cp3_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_3_end'])]

                    vec1 = (Vector(cp1_end) - Vector(cp1_origin)).normalized()
                    vec2 = (Vector(cp2_end) - Vector(cp2_origin)).normalized()
                    vec3 = (Vector(cp3_end) - Vector(cp3_origin)).normalized()

                    axis2 = vec1.cross(vec2).cross(vec3).normalized()

                elif axis2_def['type'] == 'average':
                    cp1_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_1_origin'])]
                    cp1_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_1_end'])]
                    cp2_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_2_origin'])]
                    cp2_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_2_end'])]

                    vec1 = (Vector(cp1_end) - Vector(cp1_origin)).normalized()
                    vec2 = (Vector(cp2_end) - Vector(cp2_origin)).normalized()

                    axis2 = (vec1 + vec2) / 2

                elif axis2_def['type'] == 'average_crossproduct':
                    cp1_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_1_origin'])]
                    cp1_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_1_end'])]
                    cp2_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_2_origin'])]
                    cp2_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_average_2_end'])]
                    cp3_origin = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_1_origin'])]
                    cp3_end = marker_frame_xyz[frame, marker_names.index(axis2_def['plane_axis_2_cross_1_end'])]

                    vec1 = (Vector(cp1_end) - Vector(cp1_origin)).normalized()
                    vec2 = (Vector(cp2_end) - Vector(cp2_origin)).normalized()
                    avg = (vec1 + vec2) / 2

                    vec3 = (Vector(cp3_end) - Vector(cp3_origin)).normalized()

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
            rotation_vector = Vector(rotation_vector_end_position) - Vector(rotation_vector_origin_position)

            # Get the cross product of the reference vector and the rotation vector
            cross_product = reference_vector.cross(rotation_vector)

            # In case rotation_plane_normal is None then set it as the cross product
            if rotation_plane_normal is None:
                rotation_plane_normal = cross_product

            rotation_angle = m.degrees(rotation_vector.angle(reference_vector))

            if cross_product.dot(rotation_plane_normal) < 0:
                rotation_angle = -rotation_angle

            # Store the angle value in the angle_values array
            angle_values[frame, angle_list.index(joint_angle)] = rotation_angle

    # Write the angle values to a csv file. Use the angle_list as the header
    np.savetxt(
        output_path,
        angle_values,
        delimiter=",",
        header=",".join(angle_list),
        comments='',
        fmt='%.8f',
    )

    return