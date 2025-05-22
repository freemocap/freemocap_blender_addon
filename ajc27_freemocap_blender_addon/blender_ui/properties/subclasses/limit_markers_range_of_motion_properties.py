import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes


class LimitMarkersRangeOfMotionProperties(bpy.types.PropertyGroup):
    show_limit_markers_range_of_motion_options: PropertyTypes.Bool(
        description = 'Toggle Limit Markers Range of Motion Options'
    ) # type: ignore
