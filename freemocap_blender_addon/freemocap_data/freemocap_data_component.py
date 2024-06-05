import enum
from dataclasses import dataclass
from typing import List

import numpy as np

from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, ComponentType
from freemocap_blender_addon.utilities.get_keypoint_names import get_keypoint_names




@dataclass
class FreemocapDataComponent:
    data: np.ndarray
    component_type: ComponentType
    trajectory_names: List[str]
    dimension_names: List[str]
    data_source: TrackerSourceType

    @classmethod
    def create(cls,
               data: np.ndarray,
               component_type: ComponentType,
               data_source: TrackerSourceType,
               ):
        if not len(data.shape) == 3:
            raise ValueError("Data shape should be 3D")

        return cls(data=data,
                   component_type=component_type,
                   data_source=data_source,
                   trajectory_names=get_keypoint_names(component_type=component_type,
                                                       data_source=data_source),
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


