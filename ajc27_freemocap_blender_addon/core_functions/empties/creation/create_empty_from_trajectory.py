from typing import List, Union, Dict
import bpy
import numpy as np


def create_empties(
    trajectory_frame_marker_xyz: np.ndarray,
    names_list: Union[List[str], str],
    empty_scale: float,
    empty_type: str,
    parent_object: bpy.types.Object,
) -> Dict[str, bpy.types.Object]:
    
    if isinstance(names_list, str):
        names_list = [names_list] * trajectory_frame_marker_xyz.shape[1]
    
    empties = {}
    number_of_trajectories = trajectory_frame_marker_xyz.shape[1]
    
    for marker_number in range(number_of_trajectories):
        trajectory_name = names_list[marker_number]
        trajectory_fr_xyz = trajectory_frame_marker_xyz[:, marker_number, :]
        
        empties[trajectory_name] = create_keyframed_empty_from_3d_trajectory_data(
            trajectory_fr_xyz=trajectory_fr_xyz,
            trajectory_name=trajectory_name,
            parent_object=parent_object,
            empty_scale=empty_scale,
            empty_type=empty_type,
        )

    return empties

def create_keyframed_empty_from_3d_trajectory_data(
    trajectory_fr_xyz: np.ndarray,
    trajectory_name: str,
    parent_object: bpy.types.Object,
    empty_scale: float = 0.1,
    empty_type: str = "PLAIN_AXES",
) -> bpy.types.Object:
    
    # Create empty object
    empty_object = bpy.data.objects.new(trajectory_name, None)
    empty_object.empty_display_type = empty_type
    empty_object.empty_display_size = empty_scale
    empty_object.parent = parent_object
    bpy.context.collection.objects.link(empty_object)

    # Create an action and fcurves
    action = bpy.data.actions.new(name=f"{trajectory_name}_Action")
    empty_object.animation_data_create()
    empty_object.animation_data.action = action

    # If Blender version is >= 4.4, create the structure for the action
    if bpy.app.version >= (4, 4):
        slot = action.slots.new(id_type='OBJECT', name=trajectory_name)
        layer = action.layers.new("Layer")
        strip = layer.strips.new(type='KEYFRAME')
        channelbag = strip.channelbag(slot, ensure=True)
        empty_object.animation_data.action_slot = action.slots[0]

    # Precompute frames and locations
    num_frames = trajectory_fr_xyz.shape[0]
    start_frame = bpy.context.scene.frame_start
    frames = np.arange(start_frame, start_frame + num_frames, dtype=np.float32)

    # For each axis (x, y, z), set keyframes in bulk
    for axis_idx in range(3):

        if bpy.app.version >= (4, 4):
            fcurve = channelbag.fcurves.new(data_path="location", index=axis_idx)
        else:
            fcurve = action.fcurves.new(data_path="location", index=axis_idx)
            
        fcurve.keyframe_points.add(count=num_frames)

        # Create a flattened array of [frame0, value0, frame1, value1, ...]
        co = np.empty(2 * num_frames, dtype=np.float32)
        co[0::2] = frames  # Frame numbers
        co[1::2] = trajectory_fr_xyz[:, axis_idx]  # Axis values

        # Assign all keyframes at once
        fcurve.keyframe_points.foreach_set("co", co)

        # Finalize changes
        fcurve.update()

    return empty_object
