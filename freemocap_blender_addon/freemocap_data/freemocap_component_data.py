import enum
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from freemocap_blender_addon.freemocap_data.freemocap_data_paths import DEFAULT_TRACKER_TYPE, NpyPaths, TrackerType
from freemocap_blender_addon.models.mediapipe_names.mediapipe_trajectory_names import MEDIAPIPE_BODY_NAMES


class ComponentType(enum.Enum):
    BODY = "body"
    FACE = "face"
    FULL_BODY_CENTER_OF_MASS = "full_body_center_of_mass"
    SEGMENT_CENTER_OF_MASS = "segment_center_of_mass"
    HAND_RIGHT = "hand_right"
    HAND_LEFT = "hand_left"


@dataclass
class FreemocapComponentData:
    data: np.ndarray
    component_type: ComponentType
    trajectory_names: List[str]
    data_dimension_names: List[str]
    tracker_type: TrackerType

    @classmethod
    def create(cls,
               npy_path: str,
               component_type: ComponentType,
               tracker_type: str = DEFAULT_TRACKER_TYPE,
               ) -> 'FreemocapComponentData':
        names = cls._get_trajectory_names(component_type=component_type,
                                          tracker_type=tracker_type)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = np.array(self.data)

        if isinstance(self.trajectory_names, str):
            self.trajectory_names = list(self.trajectory_names)

        if self.data.ndim == 3:
            self.data_dimension_names = ["frame", "trajectory", "xyz"]
            if not self.data.shape[1] == len(self.trajectory_names):
                raise ValueError(
                    f"Data frame shape {self.data.shape} does not match trajectory names length {len(self.trajectory_names)}")

        elif self.data.ndim == 2:
            if not len(self.trajectory_names) == 1:
                raise ValueError(
                    f"Data frame shape {self.data.shape} does not match trajectory names length {len(self.trajectory_names)}")
            self.data_dimension_names = ["frame", "xyz"]

    @classmethod
    def _get_trajectory_names(cls, component_type: ComponentType,
                              tracker_type: TrackerType) -> List[str]:
        if not tracker_type == 'mediapipe':
            raise NotImplementedError(f"Tracker type {tracker_type} not implemented")

        if component_type == ComponentType.BODY:
            return MEDIAPIPE_BODY_NAMES
