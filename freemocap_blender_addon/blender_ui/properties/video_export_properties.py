import bpy

from freemocap_blender_addon.freemocap_data_handler.utilities.load_data import get_test_recording_path


class FMC_VIDEO_EXPORT_PROPERTIES(bpy.types.PropertyGroup):
    export_profile: bpy.props.EnumProperty(
        name='',
        description='Profile of the export video',
        items=[('debug', 'Debug', ''),
               ('showcase', 'Showcase', ''),
               ('scientific', 'Scientific', ''),
               ],
    )

    ground_contact_threshold: bpy.props.FloatProperty(
        name='',
        default=0.05,
        description='Ground contact threshold (m)'
    )
