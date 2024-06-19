from dataclasses import dataclass
from typing import TYPE_CHECKING

from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass
from skelly_blender.core.blender_stuff.blenderizable_enum import blenderize_name

if TYPE_CHECKING:
    from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedName



@dataclass
class RigidSegmentDefinition(TypeSafeDataclass):
    name: str
    length: float
    parent: str
    child: str

    def blenderize(self) -> "BlenderizedSegmentDefinition":
        return BlenderizedSegmentDefinition(name=blenderize_name(self.name),
                                            length=self.length,
                                            parent=blenderize_name(self.parent),
                                            child=blenderize_name(self.child))


@dataclass
class BlenderizedSegmentDefinition(RigidSegmentDefinition):
    name: "BlenderizedName"
    parent: "BlenderizedName"
    child: "BlenderizedName"
