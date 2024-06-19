from abc import ABC
from dataclasses import dataclass

import numpy as np

from skelly_blender.core.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class Trajectory(TypeSafeDataclass, ABC):
    """
    A Trajectory is a time series of 3D coordinates that represents the movement of a point over time
    """
    name: str
    trajectory_data: np.ndarray

    def __post_init__(self):
        if not len(self.trajectory_data.shape) == 2:
            raise ValueError("Data shape should be (frame, xyz)")
        if not self.trajectory_data.shape[1] == 3:
            raise ValueError("Trajectory data should be 3D (xyz)")

        print(f"Initialized: {self}")

    def __str__(self):
        out_str = f"Trajectory: {self.name} (shape: {self.trajectory_data.shape})"
        return out_str
