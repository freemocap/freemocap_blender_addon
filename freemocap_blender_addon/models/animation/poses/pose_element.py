from dataclasses import dataclass
from typing import Tuple


@dataclass
class PoseElement:
    rotation: Tuple[float, float, float]

    def __str__(self):
        rotation_str = ", ".join([f"{r:.3f}" for r in self.rotation])
        return f"PoseElement(rotation={rotation_str}) [radians]"
