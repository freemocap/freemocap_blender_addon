import bpy
import os
import json
import numpy as np

from ajc27_freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import create_empties


def create_color_tracking_markers(
    recording_folder: str,
    data_parent_empty: bpy.types.Object,
) -> None:
    
    # Get the color_markers_3d.npy filepath from the folder output_data/raw_data
    color_marker_3d_filepath = os.path.join(recording_folder, "output_data", "raw_data", "color_markers_3d.npy")

    # If the file does not exist, raise an error
    if not os.path.exists(color_marker_3d_filepath):
        raise FileNotFoundError(f"Color marker file {color_marker_3d_filepath} not found.")
    
    # Get the markers name list from the color_markers_3d.npy numpy file
    color_marker_names_filepath = os.path.join(recording_folder, "output_data", "raw_data", "color_markers_names.json")
    if not os.path.exists(color_marker_names_filepath):
        raise FileNotFoundError(f"Color marker name file {color_marker_names_filepath} not found.")
    with open(color_marker_names_filepath, "r") as f:
        color_marker_data = json.load(f)

    if color_marker_data and isinstance(color_marker_data[0], dict):
        color_marker_names = [data["name"] for data in color_marker_data]
    else:
        color_marker_names = color_marker_data

    color_marker_3d_data = np.load(color_marker_3d_filepath)
    color_marker_3d_data = color_marker_3d_data / 1000  # Convert from millimeters to meters

    # Create the color_tracking_markers parent object
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    color_markers_parent_empty = bpy.context.active_object
    color_markers_parent_empty.name = "color_tracking_markers_parent"
    color_markers_parent_empty.empty_display_size = 0.1
    color_markers_parent_empty.parent = data_parent_empty
    color_markers_parent_empty.hide_viewport = True

    color_tracking_markers = create_empties(
        trajectory_frame_marker_xyz=color_marker_3d_data,
        names_list=color_marker_names,
        empty_scale=0.01,
        empty_type="SPHERE",
        parent_object=color_markers_parent_empty,
    )

    # Set object colors if available
    if color_marker_data and isinstance(color_marker_data[0], dict):
        for obj_name, data in zip(color_tracking_markers, color_marker_data):
            obj = bpy.data.objects.get(obj_name)
            if not obj:
                continue

            if "color" in data:
                r, g, b = data["color"]
                rgba_color = (r / 255.0, g / 255.0, b / 255.0, 1.0)

                # Create a sphere object parented to the empty
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(0, 0, 0))
                sphere_obj = bpy.context.active_object
                sphere_obj.name = f"{data['name']}_sphere"
                sphere_obj.parent = obj
                sphere_obj.location = (0, 0, 0)

                # Create a new material called marker_x (using the marker name)
                material_name = data["name"]
                material = bpy.data.materials.get(material_name)
                if not material:
                    material = bpy.data.materials.new(name=material_name)
                
                material.use_nodes = True
                principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
                if principled_bsdf:
                    principled_bsdf.inputs["Base Color"].default_value = rgba_color

                # Assign the material to the sphere
                if sphere_obj.data.materials:
                    sphere_obj.data.materials[0] = material
                else:
                    sphere_obj.data.materials.append(material)
