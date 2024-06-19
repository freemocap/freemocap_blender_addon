from dataclasses import dataclass

import bpy

from skelly_blender.core.pure_python.generic_type_hints import BlenderizedName
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ParentedEmpties(TypeSafeDataclass):
    empties: EmptiesDictionary
    parent_object: bpy.types.Object

    def __post_init__(self):
        for empty in self.empties.values():
            if empty.parent != self.parent_object:
                raise ValueError(
                    f"Empty `{empty.name}` is not parented to the parent object `{self.parent_object.name}`")

    @property
    def parent_name(self) -> BlenderizedName:
        return self.parent_object.name

    def __str__(self):
        return f"ParentedEmpties: {self.empties.keys()} parented to {self.parent_name}"
