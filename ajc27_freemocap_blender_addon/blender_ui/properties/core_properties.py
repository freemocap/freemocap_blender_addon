import bpy
import re

from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import get_test_recording_path
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.visualizer_panel import ViewPanelPropNamesElements

# Function to enable or disable the ui elements checkboxes depending on the elements visibility
def update_scope_ui_variables(self, context):

    scope_data_parent = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]
    for base_element in ViewPanelPropNamesElements:
        if base_element == ViewPanelPropNamesElements.SHOW_TRACKED_POINTS:
            tracked_points_parent = next((child for child in scope_data_parent.children_recursive if 'empties_parent' in child.name), None)
            base_element_visible = (
                any(
                    child.type == 'EMPTY' 
                    and not child.hide_get() 
                    for child in tracked_points_parent.children_recursive
                )
            )
        elif base_element == ViewPanelPropNamesElements.SHOW_RIGID_BODIES:
            rigid_body_meshes_parent = next((child for child in scope_data_parent.children_recursive if 'rigid_body_meshes_parent' in child.name), None)
            base_element_visible = (
                any(
                    child.type == 'MESH' 
                    and not child.hide_get() 
                    for child in rigid_body_meshes_parent.children_recursive
                )
            )
        elif base_element == ViewPanelPropNamesElements.SHOW_VIDEOS:
            videos_parent = next((child for child in scope_data_parent.children_recursive if 'videos_parent' in child.name), None)
            base_element_visible = (
                any(
                    child.type == 'MESH' 
                    and not child.hide_get() 
                    for child in videos_parent.children_recursive
                )
            )
        else:
            base_element_visible = (
                any(
                    re.search(base_element.object_name_pattern, child.name) 
                    and child.type == base_element.object_type 
                    and not child.hide_get() 
                    for child in scope_data_parent.children_recursive
                )
            )

        setattr(
            context.scene.freemocap_ui_properties,
            base_element.property_name,
            base_element_visible
        )

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
        update=lambda self, context: update_scope_ui_variables(self, context),
    ) # type: ignore

    recording_path: bpy.props.StringProperty(
        name="FreeMoCap recording path",
        description="Path to a freemocap recording",
        default=get_test_recording_path(),
        subtype='DIR_PATH',
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
