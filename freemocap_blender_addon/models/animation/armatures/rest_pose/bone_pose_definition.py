from dataclasses import dataclass
from typing import Tuple

ROOT_BONE_PARENT_NAME = "ROOT"
@dataclass
class BonePoseDefinition:
    parent_bone_name: str
    rotation: Tuple[float, float, float]
    is_connected: bool = True

    @property
    def is_root(self):
        return self.parent_bone_name == ROOT_BONE_PARENT_NAME
    def __str__(self):
        rotation_str = ", ".join([f"{r:.3f}" for r in self.rotation])
        return f"PoseElement(rotation={rotation_str}) [radians]: is_root={self.is_root}, is_connected={self.is_connected}"
