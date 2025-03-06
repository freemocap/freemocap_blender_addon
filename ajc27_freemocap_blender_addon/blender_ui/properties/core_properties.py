import bpy

from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import get_test_recording_path


class FREEMOCAP_CORE_PROPERTIES(bpy.types.PropertyGroup):
    print("Initializing FREEMOCAP_PROPERTIES class...")

    data_parent_collection: bpy.props.CollectionProperty(
        name="FreeMoCap data parent empties",
        description="A collection of empties to be used as parents",
        type=bpy.types.PropertyGroup
    ) # type: ignore

    scope_data_parent: bpy.props.EnumProperty(
        name="Scope data parent",
        description="Dropdown to select the data parent empty that defines the scope of the addon functions",
        items=lambda self, context: FREEMOCAP_CORE_PROPERTIES.get_collection_items(self),
    ) # type: ignore

    recording_path: bpy.props.StringProperty(
        name="FreeMoCap recording path",
        description="Path to a freemocap recording",
        default=get_test_recording_path(),
        subtype='FILE_PATH',
    ) # type: ignore

    video_export_profile: bpy.props.EnumProperty(
        name='',
        description='Profile of the export video',
        items=[('default', 'Default', ''),
               ('debug', 'Debug', ''),
               ('showcase', 'Showcase', ''),
               ('scientific', 'Scientific', ''),
               ],
    ) # type: ignore

    @staticmethod
    def get_collection_items(self):
        items = []
        if self.data_parent_collection is None:
            items = [('', '', '')]
        else:
            for idx, item in enumerate(self.data_parent_collection):
                items.append((item.name, item.name, ""))
        return items
