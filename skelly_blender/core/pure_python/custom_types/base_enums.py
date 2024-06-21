from enum import Enum

from skelly_blender.core.needs_bpy.blenderizers.blenderize_name import blenderize_name
from skelly_blender.core.pure_python.custom_types.generic_types import BlenderizedName, KeypointMappingType
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.keypoint_mapping_abc import KeypointMapping


class BlenderizableEnum(Enum):
    def blenderize(self) -> BlenderizedName:
        return blenderize_name(self.name)


class ChainEnum(BlenderizableEnum):
    pass


class LinkageEnum(BlenderizableEnum):
    pass


class SegmentEnum(BlenderizableEnum):
    pass


class KeypointEnum(BlenderizableEnum):
    pass


class KeypointMappingsEnum(BlenderizableEnum): #TODO - Apply this `enumbuilder` thing to the other types
    """An Enum that can hold different types of keypoint mappings."""

    def __new__(cls, value: KeypointMappingType):
        obj = object.__new__(cls)
        obj._value_ = KeypointMapping.create(mapping=value)
        return obj
