from dataclasses import dataclass

from skelly_blender.core.blender_stuff.blenderizers.blenderize_name import blenderize_name
from skelly_blender.core.custom_types import BlenderizedName
from skelly_blender.core.pure_python.rigid_bodies.rigid_segment import RigidSegmentDefinition


@dataclass
class BlenderizedSegmentDefinition:
    name: BlenderizedName
    length: float
    parent: BlenderizedName
    child: BlenderizedName

    @classmethod
    def from_segment(cls, rigid_segment_definition: RigidSegmentDefinition) -> 'BlenderizedSegmentDefinition':
        return cls(
            name=blenderize_name(rigid_segment_definition.name),
            length=rigid_segment_definition.length,
            parent=blenderize_name(rigid_segment_definition.parent),
            child=blenderize_name(rigid_segment_definition.child),
        )
