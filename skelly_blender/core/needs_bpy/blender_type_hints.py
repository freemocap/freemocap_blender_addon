from typing import Dict

import bpy

from skelly_blender.core.needs_bpy.blenderizers.blenderized_segment import BlenderizedSegmentDefinition
from skelly_blender.core.needs_bpy.blenderizers.blenderized_trajectory import \
    BlenderizedTrajectory
from skelly_blender.core.pure_python.custom_types.generic_types import BlenderizedName

EmptyObject = bpy.types.Object #an `Empty` object in Blender
ParentEmpty = EmptyObject #an `Empty` object in Blender that will be the parent of other objects
Empties = Dict[BlenderizedName, EmptyObject]

ArmatureObject = bpy.types.Object #an `Armature` object in Blender
RigObject = ArmatureObject #an `Armature` object in Blender with constraints and whatnot applied


BlenderizedTrajectories = Dict[BlenderizedName, BlenderizedTrajectory]
BlenderizedSegmentDefinitions = Dict[BlenderizedName, BlenderizedSegmentDefinition]
