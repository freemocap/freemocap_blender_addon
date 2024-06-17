from dataclasses import dataclass
from typing import Tuple, Optional

import mathutils
import math as m

ROOT_BONE_NAME = "ROOT"
@dataclass
class BonePoseDefinition:
    parent_bone_name: Optional[str]
    local_rotation_degrees: Tuple[float, float, float] = (0, 0, 0) #rotation defined relative to parent bone's reference frame
    offset: Tuple[float, float, float] = (0, 0, 0)
    is_connected: bool = True

    def __str__(self):
        rotation_str = ", ".join([f"{r:.3f}" for r in self.local_rotation_degrees])
        return f"PoseElement(local_rotation_degrees={rotation_str}) [degrees]: parent_bone_name: {self.parent_bone_name}, is_connected={self.is_connected}"

    @property
    def rotation_as_radians(self) -> mathutils.Vector:
        return mathutils.Vector((m.radians(self.local_rotation_degrees[0]),
                                 m.radians(self.local_rotation_degrees[1]),
                                 m.radians(self.local_rotation_degrees[2])))

    @property
    def rotation_matrix(self) -> mathutils.Matrix:
        return mathutils.Euler(
            mathutils.Vector(self.rotation_as_radians),
            "XYZ",
        ).to_matrix()

