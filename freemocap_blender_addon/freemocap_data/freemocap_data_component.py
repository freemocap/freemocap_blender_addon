from dataclasses import dataclass
from typing import List

import numpy as np

from freemocap_blender_addon.freemocap_data.create_virtual_trajectories import add_virtual_trajectories
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, ComponentType, \
    FRAME_TRAJECTORY_XYZ
from freemocap_blender_addon.utilities.get_keypoint_names import get_keypoint_names, get_virtual_trajectory_definitions


@dataclass
class BodyDataComponent:
    data: np.ndarray
    trajectory_names: List[str]
    dimension_names: List[str]

    @classmethod
    def create(cls,
               data: np.ndarray,
               data_source: TrackerSourceType,
               ):
        if not len(data.shape) == 3:
            raise ValueError("Data shape should be (frame, trajectory, xyz)")
        if not data.shape[2] == 3:
            raise ValueError("Trajectory data should be 3D (xyz)")

        all_names, all_data = add_virtual_trajectories(data=data,
                                                       names=get_keypoint_names(component_type=ComponentType.BODY,
                                                                                data_source=data_source),
                                                       virtual_trajectory_definitions=get_virtual_trajectory_definitions(
                                                           data_source=data_source)
                                                       )
        return cls(data=all_data,
                   trajectory_names=all_names,
                   dimension_names=FRAME_TRAJECTORY_XYZ
                   )

    def __post_init__(self):
        if not self.data.shape[1] == len(self.trajectory_names):
            raise ValueError(
                f"Data frame shape {self.data.shape} does not match trajectory names length {len(self.trajectory_names)}")

        elif self.data.ndim == 2:
            if not len(self.trajectory_names) == 1:
                raise ValueError(
                    f"Data frame shape {self.data.shape} does not match trajectory names length {len(self.trajectory_names)}")
