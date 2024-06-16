from dataclasses import dataclass
from typing import Tuple

ROOT_BONE_PARENT_NAME = "ROOT"


@dataclass
class BonePoseDefinition:
    parent_bone_name: str
    rotation: Tuple[float, float, float]
    is_connected: bool = True

    def __str__(self):
        rotation_str = ", ".join([f"{r:.3f}" for r in self.rotation])
        return f"PoseElement(rotation={rotation_str}) [radians]: parent_bone_name: {self.parent_bone_name}, is_connected={self.is_connected}"
