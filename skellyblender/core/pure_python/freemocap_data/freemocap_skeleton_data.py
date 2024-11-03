from dataclasses import dataclass

from skellyblender.core.pure_python.custom_types.derived_types import Trajectories, RigidBodyDefinitions
from skellyblender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class FreemocapSkeletonData(TypeSafeDataclass):
    """
    Terminology - "data" is a measurement of some sort
    """
    trajectories: Trajectories
    segment_definitions: RigidBodyDefinitions


