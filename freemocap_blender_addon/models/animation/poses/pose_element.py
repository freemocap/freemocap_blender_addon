from dataclasses import dataclass
from typing import Tuple


@dataclass
class PoseElement:
    rotation: Tuple[float, float, float]
    is_root: bool = False
    is_connected: bool = True

    def __str__(self):
        rotation_str = ", ".join([f"{r:.3f}" for r in self.rotation])
        return f"PoseElement(rotation={rotation_str}) [radians]: is_root={self.is_root}, is_connected={self.is_connected}"
