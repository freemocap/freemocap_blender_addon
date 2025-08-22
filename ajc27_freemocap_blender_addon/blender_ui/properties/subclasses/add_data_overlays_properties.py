import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes

class AddDataOverlaysProperties(bpy.types.PropertyGroup):
    show_add_data_overlays_options: PropertyTypes.Bool(
        description = 'Toggle Add Data Overlays Options'
    ) # type: ignore