import bpy
import os
import json
import numpy as np

from ajc27_freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import create_empties


def create_yolo_object_markers(
    recording_folder: str,
    data_parent_empty: bpy.types.Object,
) -> None:
    
    # Get the yolo_object_markers_3d.npy filepath
    yolo_marker_3d_filepath = os.path.join(recording_folder, "output_data", "yolo_object_tracking", "yolo_object_markers_3d.npy")

    # If the file does not exist, print a warning and return early
    if not os.path.exists(yolo_marker_3d_filepath):
        print(f"YOLO marker file {yolo_marker_3d_filepath} not found. Skipping YOLO marker creation.")
        return
    
    # Get the model info json to retrieve marker names
    yolo_model_info_filepath = os.path.join(recording_folder, "output_data", "yolo_object_tracking", "yolo_object_model_info.json")
    if not os.path.exists(yolo_model_info_filepath):
        print(f"YOLO model info file {yolo_model_info_filepath} not found. Skipping YOLO marker creation.")
        return
    
    with open(yolo_model_info_filepath, "r") as f:
        yolo_model_info = json.load(f)

    # Extract marker names from the model info
    yolo_marker_names = yolo_model_info.get("tracked_object_names", [])

    # Load the 3D data
    yolo_marker_3d_data = np.load(yolo_marker_3d_filepath)
    
    # YOLO data shape is (frames, objects, 6) -> (x, y, z, conf, class, error)
    # We only need the first 3 channels (x, y, z)
    yolo_marker_3d_data = yolo_marker_3d_data[:, :, :3]
    
    # Convert from millimeters to meters
    yolo_marker_3d_data = yolo_marker_3d_data / 1000

    # Create the yolo_object_markers parent object
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    yolo_markers_parent_empty = bpy.context.active_object
    yolo_markers_parent_empty.name = "yolo_object_markers_parent"
    yolo_markers_parent_empty.empty_display_size = 0.1
    yolo_markers_parent_empty.parent = data_parent_empty
    yolo_markers_parent_empty.hide_viewport = True

    # Create empties for the tracked objects
    create_empties(
        trajectory_frame_marker_xyz=yolo_marker_3d_data,
        names_list=yolo_marker_names,
        empty_scale=0.025,
        empty_type="SPHERE",
        parent_object=yolo_markers_parent_empty,
    )

    # Define a list of 10 distinct colors (RGBA)
    default_colors = [
        (1.0, 0.0, 0.0, 1.0),   # Red
        (0.0, 1.0, 0.0, 1.0),   # Green
        (0.0, 0.0, 1.0, 1.0),   # Blue
        (1.0, 1.0, 0.0, 1.0),   # Yellow
        (0.0, 1.0, 1.0, 1.0),   # Cyan
        (1.0, 0.0, 1.0, 1.0),   # Magenta
        (1.0, 0.5, 0.0, 1.0),   # Orange
        (0.5, 0.0, 0.5, 1.0),   # Purple
        (0.5, 1.0, 0.0, 1.0),   # Lime
        (1.0, 0.0, 0.5, 1.0),   # Pink
    ]

    # Create colored spheres for each tracked object
    for i, obj_name in enumerate(yolo_marker_names):
        obj = bpy.data.objects.get(obj_name)
        if not obj:
            continue

        # Get Color
        rgba_color = default_colors[i]

        # Create a sphere object parented to the empty
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(0, 0, 0))
        sphere_obj = bpy.context.active_object
        sphere_obj.name = f"{obj_name}_sphere"
        sphere_obj.parent = obj
        sphere_obj.location = (0, 0, 0)

        # Create/Get material and assign color
        material_name = f"{obj_name}_material"
        material = bpy.data.materials.get(material_name) or bpy.data.materials.new(name=material_name)
        
        material.use_nodes = True
        principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
        if principled_bsdf:
            principled_bsdf.inputs["Base Color"].default_value = rgba_color

        sphere_obj.data.materials.append(material)
