import bpy
import numpy as np

from ajc27_freemocap_blender_addon.data_models.joint_angles.joint_angles import joint_angles
from ajc27_freemocap_blender_addon.core_functions.joint_angles.calculate_joint_angle_info import calculate_joint_angle_info
from ajc27_freemocap_blender_addon.core_functions.joint_angles.add_angle_meshes import add_angle_meshes
from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.ui_utilities import parent_meshes
from ajc27_freemocap_blender_addon.core_functions.joint_angles.create_angle_geometry_nodes import create_angle_geometry_nodes
from ajc27_freemocap_blender_addon.core_functions.joint_angles.animate_angle_meshes import animate_angle_meshes
from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.ui_utilities import draw_vector

# TODO: Add multicapture support. Change the joint_angles dict to have the correct scope marker names (left_elbow.001, etc.)
# but have to check the impact on the new angle/text meshes, if getting a sufix like .001 would affect the functions.
def add_joint_angles(
    data_parent_empty: bpy.types.Object,
    joint_angle_list: list,
    angle_radius: float = 10.0,
    overwrite_colors: bool = False,
    angle_mesh_color: tuple = (0.694,0.082,0.095,1.0),
    angle_text_color: tuple = (1.0,0.365,0.048,1.0),
    angle_text_size: float = 5.0,
    angle_text_orientation: str = 'rotation_plane_normal',
    angle_text_local_x_offset: float = 3.0,
    angle_text_local_y_offset: float = 0.0,
):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Create a dictionary with all the markers that are children of the data parent empty
    markers = {}
    for child in data_parent_empty.children_recursive:
        if child.type == 'EMPTY' and 'empties_parent' in child.name:
            for marker in child.children:
                if marker.type == 'EMPTY':
                    # Get the position fcurves
                    fcurve_x = marker.animation_data.action.fcurves.find("location", index=0)
                    fcurve_y = marker.animation_data.action.fcurves.find("location", index=1)
                    fcurve_z = marker.animation_data.action.fcurves.find("location", index=2)

                    # Get the fcurve data as numpy arrays
                    fcurve_data = np.array([
                        [kp.co[1] for kp in fcurve_x.keyframe_points],
                        [kp.co[1] for kp in fcurve_y.keyframe_points],
                        [kp.co[1] for kp in fcurve_z.keyframe_points]
                    ])
            
                    # Save the marker object and its position fcurves in the dictionary
                    markers[marker.name] = {
                        'object': marker,
                        'fcurves': fcurve_data,
                    }

    # Calculate the joint angle values and vectors
    angle_values, reference_vectors, rotation_vectors, rotation_plane_normals = calculate_joint_angle_info(
        joint_angle_list,
        markers,
    )

    # Temporal debug vectors code
    # draw_vector(
    #     bpy.data.objects["left_wrist"].location,
    #     rotation_vectors[bpy.context.scene.frame_current, 0, :],
    #     "left_ankle_rotation_vector"
    # )
    # draw_vector(
    #     bpy.data.objects["left_wrist"].location,
    #     reference_vectors[bpy.context.scene.frame_current, 0, :],
    #     "left_ankle_reference_vector"
    # )
    # draw_vector(
    #     bpy.data.objects["left_wrist"].location,
    #     rotation_plane_normals[bpy.context.scene.frame_current, 0, :],
    #     "left_ankle_rotation_plane_normal"
    # )
    

    # Get a list of the joint_centers
    joint_centers = []
    for joint_angle in joint_angle_list:
        joint_centers.append(joint_angles[joint_angle]['joint_center'])

    # Add the angle and text meshes
    angle_meshes = add_angle_meshes(
        joint_angle_list,
        joint_centers,
        'angle',
    )
    angletext_meshes = add_angle_meshes(
        joint_angle_list,
        joint_centers,
        'angletext',
    )
    # Parent the angle and text meshes to a empty object
    parent_meshes(data_parent_empty, 'joint_angles_parent', angle_meshes)
    parent_meshes(data_parent_empty, 'joint_angles_parent', angletext_meshes)

    # Create Geometry Nodes for each angle mesh
    create_angle_geometry_nodes(
        angle_meshes,
        'angle',
        angle_radius,
        overwrite_colors,
        angle_mesh_color,
        angle_text_color,
    )
    create_angle_geometry_nodes(
        angletext_meshes,
        'angletext',
        angle_text_size = angle_text_size,
        angle_text_local_x_offset = angle_text_local_x_offset,
        angle_text_local_y_offset = angle_text_local_y_offset,
    )
    
    # Animate the angle meshes
    animate_angle_meshes(
        angle_values,
        reference_vectors,
        rotation_plane_normals,
        angle_meshes,
        angletext_meshes,
        angle_text_orientation,
    )

    return
    