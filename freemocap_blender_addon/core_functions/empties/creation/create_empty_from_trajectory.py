from typing import Dict, Tuple

import bpy
import numpy as np

from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


class ParentedEmpties(TypeSafeDataclass):
    empties: Dict[str, bpy.types.Object]
    parent_object: bpy.types.Object

    def __post_init__(self):
        for empty in self.empties.values():
            if empty.parent != self.parent_object:
                raise ValueError(f"Empty `{empty.name}` is not parented to the parent object `{self.parent_object.name}`")

    @property
    def parent_name(self):
        return self.parent_object.name


    def __str__(self):
        return f"ParentedEmpties: {self.empties.keys()} parented to {self.parent_name}"


def create_empties_from_trajectories(keypoint_trajectories: KeypointTrajectories,
                                     parent_name: str,
                                     empty_scale: float = 0.01,
                                     empty_type: str = "SPHERE") -> ParentedEmpties:
    """
    Create empties for each trajectory in the dictionary and parent them to a new parent empty object.

    """

    empties = {}

    # Create a parent empty object
    bpy.ops.object.empty_add(type="ARROWS")
    parent_object = bpy.context.editable_objects[-1]
    parent_object.name = parent_name

    for parent_name, trajectory in keypoint_trajectories.items():
        empties[parent_name] = create_keyframed_empty_from_3d_trajectory_data(
            trajectory_fr_xyz=trajectory.trajectory_data,
            trajectory_name=f"{parent_name}_{parent_name}",
            parent_object=parent_object,
            empty_scale=empty_scale,
            empty_type=empty_type,
        )

    return ParentedEmpties(empties=empties, parent_object=parent_object)


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
    print(f"Creating keyframed empty: `{trajectory_name}`")
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
