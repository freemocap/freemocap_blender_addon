from enum import Enum

from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedName
from skelly_blender.core.blender_stuff.blenderizers.blenderize_name import blenderize_name


class BlenderizableEnum(Enum):
    def blenderize(self) -> BlenderizedName:
        return blenderize_name(self.name)


