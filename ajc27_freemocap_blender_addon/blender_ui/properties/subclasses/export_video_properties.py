import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes


class ExportVideoProperties(bpy.types.PropertyGroup):
    export_profile: PropertyTypes.Enum(
        name='',
        description='Profile for exporting the video',
        items=[
            ('showcase', 'Showcase', 'Showcase'),
            ('debug', 'Debug', 'Debug'),
            ('scientific', 'Scientific', 'Scientific'),
            ('multiview', 'Multiview', 'Multiview')
        ],
        default='Showcase',
    ) # type: ignore