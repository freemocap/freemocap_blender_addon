from dataclasses import dataclass

from skelly_blender.core.custom_types import Trajectories, RigidSegmentDefinitions
from skelly_blender.core.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class FreemocapSkeletonData(TypeSafeDataclass):
    """
    Terminology - "data" is a measurement of some sort
    """
    trajectories: Trajectories
    segment_definitions: RigidSegmentDefinitions


