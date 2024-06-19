from dataclasses import dataclass

from skelly_blender.core.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class RigidSegmentDefinition(TypeSafeDataclass):
    name: str
    length: float
    parent: str
    child: str
