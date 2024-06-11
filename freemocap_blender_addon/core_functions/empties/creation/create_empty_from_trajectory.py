from typing import Dict, Tuple

import bpy
import numpy as np


def create_empties_from_trajectories(trajectories: Dict[str, np.ndarray],
                                     name: str,
                                     empty_scale: float = 0.01,
                                     empty_type: str = "SPHERE") -> Tuple[Dict[str, bpy.types.Object], bpy.types.Object]:
    """
    Create empties for each trajectory in the dictionary and parent them to a new parent empty object.

    """

    empties = {}

    # Create a parent empty object
    bpy.ops.object.empty_add(type="ARROWS")
    parent_object = bpy.context.editable_objects[-1]
    parent_object.name = name

    for trajectory_name, trajectory_data in trajectories.items():
        empties[trajectory_name] = create_keyframed_empty_from_3d_trajectory_data(
            trajectory_fr_xyz=trajectory_data,
            trajectory_name=f"{name}_{trajectory_name}",
            parent_object=parent_object,
            empty_scale=empty_scale,
            empty_type=empty_type,
        )

    return empties, parent_object


def create_keyframed_empty_from_3d_trajectory_data(
        trajectory_fr_xyz: np.ndarray,
        trajectory_name: str,
        parent_object: bpy.types.Object,
        empty_scale: float = 0.01,
        empty_type: str = "PLAIN_AXES",
) -> bpy.types.Object:
    """
    Create a key framed empty from 3D trajectory data.

    Parameters
    ----------
    trajectory_fr_xyz : np.ndarray
        3D trajectory data with shape (number_of_frames, 3).
    trajectory_name : str
        Name for the empty object.
    parent_object : bpy.types.Object
        The parent object to which the empty will be parented.
    empty_scale : float, optional
        Scale of the empty object, by default 0.1.
    empty_type : str, optional
        Type of the empty object, by default "PLAIN_AXES".

    Returns
    -------
    bpy.types.Object
        The created empty object.
    """
    print(f"Creating keyframed empty from: {trajectory_name}...")
    bpy.ops.object.empty_add(type=empty_type)
    empty_object = bpy.context.editable_objects[-1]
    empty_object.name = trajectory_name

    empty_object.empty_display_size = empty_scale

    empty_object.parent = parent_object

    for frame_number in range(trajectory_fr_xyz.shape[0]):
        empty_object.location = [
            trajectory_fr_xyz[frame_number, 0],
            trajectory_fr_xyz[frame_number, 1],
            trajectory_fr_xyz[frame_number, 2],
        ]

        empty_object.keyframe_insert(data_path="location", frame=frame_number)

    return empty_object
