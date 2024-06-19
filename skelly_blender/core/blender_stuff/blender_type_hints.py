from typing import Dict

import bpy

from skelly_blender.core.pure_python.rigid_bodies.rigid_segment_definition import BlenderizedSegmentDefinition
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import BlenderizedTrajectory

BlenderizedName = str
EmptiesDictionary = Dict[BlenderizedName, bpy.types.Object]


BlenderizedTrajectories = Dict[BlenderizedName, BlenderizedTrajectory]
BlenderizedSegmentDefinitions = Dict[BlenderizedName, BlenderizedSegmentDefinition]
