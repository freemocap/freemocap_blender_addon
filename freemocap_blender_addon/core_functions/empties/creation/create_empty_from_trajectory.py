from typing import List, Optional, Union, Dict
import bpy
import numpy as np


def create_empties(
    trajectory_frame_marker_xyz: np.ndarray,
    names_list: Union[List[str], str],
    empty_scale: float,
    empty_type: str,
    parent_object: bpy.types.Object,
    fallback_trajectory_fr_xyz: Optional[np.ndarray] = None,
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
            fallback_trajectory_fr_xyz=fallback_trajectory_fr_xyz,
        )

    return empties


def _fill_nan_1d(values: np.ndarray, fallback_values: Optional[np.ndarray] = None) -> np.ndarray:
    """Forward-fill NaN samples from the last valid value, back-fill any leading NaNs,
    and fall back to `fallback_values` (or zero, if none given) if every sample is NaN
    (e.g. an entirely missing trajectory)."""
    nan_mask = np.isnan(values)
    if not nan_mask.any():
        return values
    if nan_mask.all():
        if fallback_values is None:
            return np.zeros_like(values)
        # The fallback itself may have gaps (e.g. the wrist trajectory is also partially missing) -
        # fill it against zero rather than propagating NaN.
        return _fill_nan_1d(fallback_values)

    filled = values.copy()
    valid_indices = np.flatnonzero(~nan_mask)
    hold_indices = np.maximum.accumulate(np.where(~nan_mask, np.arange(len(values)), 0))
    filled = filled[hold_indices]
    filled[: valid_indices[0]] = values[valid_indices[0]]
    return filled


def create_keyframed_empty_from_3d_trajectory_data(
    trajectory_fr_xyz: np.ndarray,
    trajectory_name: str,
    parent_object: bpy.types.Object|None=None,
    empty_scale: float = 0.1,
    empty_type: str = "PLAIN_AXES",
    fallback_trajectory_fr_xyz: Optional[np.ndarray] = None,
) -> bpy.types.Object:
    
    # Create empty object
    empty_object = bpy.data.objects.new(trajectory_name, None)
    empty_object.empty_display_type = empty_type
    empty_object.empty_display_size = empty_scale
    empty_object.parent = parent_object if parent_object else None
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
        fallback_values = fallback_trajectory_fr_xyz[:, axis_idx] if fallback_trajectory_fr_xyz is not None else None
        co[1::2] = _fill_nan_1d(trajectory_fr_xyz[:, axis_idx], fallback_values)  # Axis values, with NaNs filled

        # Assign all keyframes at once
        fcurve.keyframe_points.foreach_set("co", co)

        # Finalize changes
        fcurve.update()

    return empty_object
