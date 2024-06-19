from typing import Dict

import bpy

from skelly_blender.core.custom_types import BlenderizedName
from skelly_blender.core.blender_stuff.blenderizers.blenderized_segment import BlenderizedSegmentDefinition
from skelly_blender.core.blender_stuff.blenderizers.blenderized_trajectory import \
    BlenderizedTrajectory

EmptyObject = bpy.types.Object #an `Empty` object in Blender
Empties = Dict[BlenderizedName, EmptyObject]

ArmatureObject = bpy.types.Object #an `Armature` object in Blender
RigObject = ArmatureObject #an `Armature` object in Blender with constraints and whatnot applied


BlenderizedTrajectories = Dict[BlenderizedName, BlenderizedTrajectory]
BlenderizedSegmentDefinitions = Dict[BlenderizedName, BlenderizedSegmentDefinition]
