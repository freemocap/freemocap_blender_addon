from typing import Union

import bpy
import numpy as np

from skelly_blender.core.needs_bpy.blender_type_hints import BlenderizedName, BlenderizedTrajectories, ParentEmpty, \
    EmptyObject
from skelly_blender.core.needs_bpy.empties.empties_dataclasses import ParentedEmpties
from skelly_blender.core.pure_python.custom_types.derived_types import Trajectories


def create_keyframed_empties(trajectories: Union[BlenderizedTrajectories, Trajectories],
                             parent_empty:ParentEmpty,
                             empty_scale: float = 0.025,
                             empty_type: str = "SPHERE") -> ParentedEmpties:
    """
    Create empties for each trajectory in the dictionary and parent them to a new parent empty object.

    """

    empties = {}



    for trajectory_name, trajectory in trajectories.items():

        empties[trajectory_name] = create_keyframed_empty_from_3d_trajectory_data(
            trajectory_fr_xyz=trajectory.trajectory_fr_xyz,
            trajectory_name=trajectory_name,
            parent_empty=parent_empty,
            empty_scale=empty_scale,
            empty_type=empty_type,
        )

    return ParentedEmpties(empties=empties,
                           parent_empty=parent_empty)


def create_keyframed_empty_from_3d_trajectory_data(
        trajectory_fr_xyz: np.ndarray,
        trajectory_name: BlenderizedName,
        parent_empty: ParentEmpty,
        empty_scale: float = 0.01,
        empty_type: str = "PLAIN_AXES",
) -> EmptyObject:
    """
    Create a key framed empty from 3D trajectory data.

    Parameters
    ----------
    trajectory_fr_xyz : np.ndarray
        3D trajectory data with shape (number_of_frames, 3).
    trajectory_name : str
        Name for the empty object.
    parent_empty : bpy.types.Object
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
    print(f"Creating keyframed empty: `{trajectory_name}`")
    bpy.ops.object.empty_add(type=empty_type)
    empty_object = bpy.context.editable_objects[-1]
    empty_object.name = trajectory_name

    empty_object.empty_display_size = empty_scale

    empty_object.parent = parent_empty

    for frame_number in range(trajectory_fr_xyz.shape[0]):
        empty_object.location = [
            trajectory_fr_xyz[frame_number, 0],
            trajectory_fr_xyz[frame_number, 1],
            trajectory_fr_xyz[frame_number, 2],
        ]

        empty_object.keyframe_insert(data_path="location", frame=frame_number)

    return empty_object
