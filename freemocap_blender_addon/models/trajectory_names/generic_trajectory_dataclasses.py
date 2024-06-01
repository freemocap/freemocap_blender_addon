from dataclasses import dataclass
from typing import Optional, List

import numpy as np


@dataclass
class HandsTrajectoryNames:
    right: Optional[List[str]]
    left: Optional[List[str]]


@dataclass
class HumanTrajectoryNames:
    body: Optional[List[str]]
    face: Optional[List[str]]
    hands: Optional[HandsTrajectoryNames]


@dataclass
class TetrapodTrajectoryNames(HumanTrajectoryNames):
    tail: Optional[List[str]]


@dataclass
class WeightedSumDefinition:
    trajectory_names: List[str]
    weights: List[float]


@dataclass
class TrajectoryData:
    data: np.ndarray
    virtual: Optional[WeightedSumDefinition]
    children: Optional[List[str]]

    def __post_init__(self):
        if self.data.shape[-1] != 3:
            raise ValueError("TrajectoryData data must have shape (N,..., 3), i.e. be a 3D trajectory")

    @property
    def is_virtual(self) -> bool:
        return self.virtual is not None

    @property
    def is_leaf(self) -> bool:
        return self.children is None
