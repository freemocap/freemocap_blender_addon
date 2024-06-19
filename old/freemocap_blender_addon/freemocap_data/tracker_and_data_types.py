from enum import Enum
from typing import List


class DataTypes(str, Enum):
    SKELETON = "skeleton"
    CENTER_OF_MASS = "center_of_mass"


FRAME_TRAJECTORY_XYZ: List[str] = ["frame_number", "trajectory_index", "xyz"]
