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
        color_marker_names = json.load(f)

    color_marker_3d_data = np.load(color_marker_3d_filepath)
    color_marker_3d_data = color_marker_3d_data / 1000  # Convert from millimeters to meters

    # Create the color_tracking_markers parent object
    bpy.ops.object.empty_add(type="PLAIN_AXES")
    color_markers_parent_empty = bpy.context.active_object
    color_markers_parent_empty.name = "Color Tracking Markers"
    color_markers_parent_empty.empty_display_size = 0.1
    color_markers_parent_empty.parent = data_parent_empty

    color_tracking_markers = create_empties(
        trajectory_frame_marker_xyz=color_marker_3d_data,
        names_list=color_marker_names,
        empty_scale=0.1,
        empty_type="SPHERE",
        parent_object=color_markers_parent_empty,
    )
