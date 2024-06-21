from dataclasses import dataclass

from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_segments import BodySegments
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class RigidBodyDefinition(TypeSafeDataclass):
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
        if self.parent.upper() not in BodyKeypoints.__members__.keys(): #TODO - make an 'all segments' enum or something to handles hands, etc
            raise ValueError(f"Parent {self.parent.upper()} not in {BodyKeypoints}")

    def __str__(self):
        return f"RigidBodyDefinition: {self.name} (length: {self.length:.3f}, parent: {self.parent}, child: {self.child})"