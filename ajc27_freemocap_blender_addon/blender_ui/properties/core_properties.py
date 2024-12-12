import bpy

from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import get_test_recording_path


class FREEMOCAP_CORE_PROPERTIES(bpy.types.PropertyGroup):
    print("Initializing FREEMOCAP_PROPERTIES class...")

    data_parent_empty: bpy.props.PointerProperty(
        name="FreeMoCap data parent empty",
        description="Empty that serves as parent for all the freemocap empties",
        type=bpy.types.Object,
        poll=lambda self, object_in: object_in.type == 'EMPTY',
    )

    recording_path: bpy.props.StringProperty(
        name="FreeMoCap recording path",
        description="Path to a freemocap recording",
        default=get_test_recording_path(),
        subtype='FILE_PATH',
    )

    video_export_profile: bpy.props.EnumProperty(
        name='',
        description='Profile of the export video',
        items=[('default', 'Default', ''),
               ('debug', 'Debug', ''),
               ('showcase', 'Showcase', ''),
               ('scientific', 'Scientific', ''),
               ],
    )
