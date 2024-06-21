from skelly_blender.core.blender_stuff.blenderizers.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.custom_types import KeypointMappingType
from skelly_blender.core.skeleton_model.abstract_base_classes.keypoint_mapping_abc import KeypointMapping


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
