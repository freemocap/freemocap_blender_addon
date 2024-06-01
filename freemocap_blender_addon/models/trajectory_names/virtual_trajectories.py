from dataclasses import dataclass
from typing import Optional, List

from freemocap_blender_addon.utilities.named_ndarray import NamedNumpyArray


@dataclass
class WeightedSumDefinition:
    trajectory_names: List[str]
    weights: List[float]


@dataclass
class TrajectoryData(NamedNumpyArray):
    virtual: Optional[WeightedSumDefinition]
    children: Optional[List[str]]

    @property
    def is_virtual(self) -> bool:
        return self.virtual is not None

    @property
    def is_leaf(self) -> bool:
        return self.children is None
