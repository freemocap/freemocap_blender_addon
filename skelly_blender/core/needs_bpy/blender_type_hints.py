from typing import Dict

import bpy

from skelly_blender.core.pure_python.custom_types import BlenderizedName
from skelly_blender.core.needs_bpy.blenderizers.blenderized_segment import BlenderizedSegmentDefinition
from skelly_blender.core.needs_bpy.blenderizers.blenderized_trajectory import \
    BlenderizedTrajectoryABC

EmptyObject = bpy.types.Object #an `Empty` object in Blender
Empties = Dict[BlenderizedName, EmptyObject]

ArmatureObject = bpy.types.Object #an `Armature` object in Blender
RigObject = ArmatureObject #an `Armature` object in Blender with constraints and whatnot applied


BlenderizedTrajectories = Dict[BlenderizedName, BlenderizedTrajectoryABC]
BlenderizedSegmentDefinitions = Dict[BlenderizedName, BlenderizedSegmentDefinition]
