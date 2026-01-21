from dataclasses import dataclass
from typing import Tuple


@dataclass
class PoseElement:
    rotation: Tuple[float, float, float]
    roll: float = 0