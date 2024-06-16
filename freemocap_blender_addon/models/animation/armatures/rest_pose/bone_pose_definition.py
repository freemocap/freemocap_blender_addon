from dataclasses import dataclass
from typing import Tuple, Optional

import mathutils
import math as m

ROOT_BONE_NAME = "ROOT"



@dataclass
class BonePoseDefinition:
    parent_bone_name: Optional[str]
    rotation: Tuple[float, float, float]
    is_connected: bool = True

    def __str__(self):
        rotation_str = ", ".join([f"{r:.3f}" for r in self.rotation])
        return f"PoseElement(rotation={rotation_str}) [radians]: parent_bone_name: {self.parent_bone_name}, is_connected={self.is_connected}"

    @property
    def rotation_as_radians(self) -> mathutils.Vector:
        return mathutils.Vector((m.radians(self.rotation[0]),
                                 m.radians(self.rotation[1]),
                                 m.radians(self.rotation[2])))

    @property
    def rotation_matrix(self) -> mathutils.Matrix:
        return mathutils.Euler(
            mathutils.Vector(self.rotation_as_radians),
            "XYZ",
        ).to_matrix()
