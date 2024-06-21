from dataclasses import dataclass

from skelly_blender.core.needs_bpy.blenderizers.blenderize_name import blenderize_name
from skelly_blender.core.pure_python.custom_types.generic_types import BlenderizedName
from skelly_blender.core.pure_python.rigid_bodies.rigid_body_definition_class import RigidBodyDefinition


@dataclass
class BlenderizedSegmentDefinition:
    name: BlenderizedName
    length: float
    parent: BlenderizedName
    child: BlenderizedName

    @classmethod
    def from_segment(cls, rigid_segment_definition: RigidBodyDefinition) -> 'BlenderizedSegmentDefinition':
        return cls(
            name=blenderize_name(rigid_segment_definition.name),
            length=rigid_segment_definition.length,
            parent=blenderize_name(rigid_segment_definition.parent),
            child=blenderize_name(rigid_segment_definition.child),
        )

    def __str__(self):
        return f"{self.name}: {self.length:.3f} {self.parent} {self.child}"