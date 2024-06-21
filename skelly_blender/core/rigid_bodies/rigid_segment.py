from dataclasses import dataclass

from skelly_blender.core.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class RigidSegmentDefinition(TypeSafeDataclass):
    """
    Terminology "defintion" means that it involves setting a number of some kind, but its not necessarily a direct
    empirical measurement like "data" (in this case, its 'length' which is derived from the empirically measured
    trajectory data)
    """
    name: str
    length: float
    parent: str
    child: str

    def __post_init__(self):
        if self.length <= 0:
            raise ValueError("Length must be positive")
        if self.parent == self.child:
            raise ValueError("Parent and child must be different")
        if self.parent not in AllSegments:
            raise ValueError(f"Parent {self.parent} not in {AllSegmentNames}")
