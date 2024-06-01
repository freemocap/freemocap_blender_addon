import enum
from dataclasses import dataclass
from typing import List

import numpy as np

from freemocap_blender_addon.freemocap_data.freemocap_data_paths import DataSourceType
from freemocap_blender_addon.models.mediapipe_names.mediapipe_trajectory_names import MEDIAPIPE_TRAJECTORY_NAMES

FRAME_TRAJECTORY_XYZ: List[str] = ["frame_number", "trajectory_index", "xyz"]


class ComponentType(enum.Enum):
    BODY = "body"
    FACE = "face"
    HAND = "hand"


@dataclass
class FreemocapComponentData:
    data: np.ndarray
    component_type: ComponentType
    trajectory_names: List[str]
    dimension_names: List[str]
    data_source: DataSourceType

    @classmethod
    def create(cls,
               data: np.ndarray,
               component_type: ComponentType,
               data_source: DataSourceType,
               ):
        if not len(data.shape) == 3:
            raise ValueError("Data shape should be 3D")

        cls(data=data,
            component_type=component_type,
            data_source=data_source,
            trajectory_names=cls._get_trajectory_names(component_type=component_type,
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

    @classmethod
    def _get_trajectory_names(cls, component_type: ComponentType,
                              data_source: DataSourceType) -> List[str]:
        if data_source == 'mediapipe':
            if component_type == ComponentType.BODY:
                return MEDIAPIPE_TRAJECTORY_NAMES.body
            elif component_type == ComponentType.FACE:
                return MEDIAPIPE_TRAJECTORY_NAMES.face
            elif component_type == ComponentType.HAND:
                return MEDIAPIPE_TRAJECTORY_NAMES.hands
