from dataclasses import dataclass
from pathlib import Path

import numpy as np

from skelly_blender.core.pure_python.load_data.data_paths.paths_dataclass import PathsDataclass


@dataclass
class NpyPaths(PathsDataclass):
    def __post_init__(self):
        super().__post_init__()
        for field in self.__dict__.values():
            if isinstance(field, NpyPaths):
                continue
            if not field.endswith(".npy"):
                raise ValueError(f"Path {field} is not a npy file")
            if not Path(field).exists():
                raise FileNotFoundError(f"Path {field} does not exist")
            if np.load(field).size == 0:
                raise ValueError(f"Empty npy file: {field}")

    def __str__(self):
        return super().__str__()


@dataclass
class HandsNpyPaths(NpyPaths):
    right: str
    left: str


@dataclass
class SkeletonNpyPaths(NpyPaths):
    body: str
    hands: HandsNpyPaths
    face: str
    reprojection_error: str


@dataclass
class CenterOfMassNpyPaths(NpyPaths):
    total_body_center_of_mass: str
    segment_center_of_mass: str
