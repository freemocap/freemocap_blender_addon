from dataclasses import dataclass

import bpy

from skellyblender.core.needs_bpy.blender_type_hints import Empties, BlenderizedName, ParentEmpty
from skellyblender.core.needs_bpy.blenderizers.blenderized_skeleton_data import parentify_name
from skellyblender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class ParentedEmpties(TypeSafeDataclass):
    empties: Empties
    parent_empty: ParentEmpty

    def __post_init__(self):
        for empty in self.empties.values():
            if empty.parent != self.parent_empty:
                raise ValueError(
                    f"Empty `{empty.name}` is not parented to the parent object `{self.parent_empty.name}`")

    @property
    def parent_name(self) -> BlenderizedName:
        return self.parent_empty.name

    def get_empty(self, empty_name: BlenderizedName) -> bpy.types.Object:
        return self.empties[parentify_name(name=empty_name, parent_name=self.parent_name)]

    def __str__(self):
        return f"ParentedEmpties: {self.empties.keys()} parented to {self.parent_name}"
