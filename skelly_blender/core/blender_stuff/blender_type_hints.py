from dataclasses import dataclass
from typing import Dict

import bpy

from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory

BlenderizedName = str
EmptiesDictionary = Dict[BlenderizedName, bpy.types.Object]


@dataclass
class BlenderizedTrajectory(Trajectory):
    name: BlenderizedName


BlenderizedTrajectories = Dict[BlenderizedName, BlenderizedTrajectory]
