from dataclasses import dataclass
from typing import List, Literal

import numpy as np

FREEMOCAP_DATA_COMPONENT_TYPES = Literal["body", "right_hand", "left_hand", "face", "other"]

@dataclass
class FreemocapComponentData:
    name: str
    data: np.ndarray
    data_source: str
    trajectory_names: List[str]
    data_dimension_names: List[str] = None
    error: np.ndarray = None

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = np.array(self.data)

        if isinstance(self.trajectory_names, str):
            self.trajectory_names = list(self.trajectory_names)

        if self.data.ndim == 3:
            self.data_dimension_names = ["frame", "marker", "xyz"]
            if not self.data.shape[1] == len(self.trajectory_names):
                raise ValueError(
                    f"Data frame shape {self.data.shape} does not match trajectory names length {len(self.trajectory_names)}")

        elif self.data.ndim == 2:
            if not len(self.trajectory_names) == 1:
                raise ValueError(
                    f"Data frame shape {self.data.shape} does not match trajectory names length {len(self.trajectory_names)}")
            self.data_dimension_names = ["frame", "xyz"]
