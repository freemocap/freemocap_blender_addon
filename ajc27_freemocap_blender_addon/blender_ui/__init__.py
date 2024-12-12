from ajc27_freemocap_blender_addon.blender_ui.main_view3d_panel import VIEW3D_PT_freemocap_main_panel
from ajc27_freemocap_blender_addon.blender_ui.operators import BLENDER_OPERATORS
from ajc27_freemocap_blender_addon.blender_ui.properties.core_properties import FREEMOCAP_CORE_PROPERTIES
from ajc27_freemocap_blender_addon.blender_ui.properties.ui_properties import FREEMOCAP_UI_PROPERTIES
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.load_data_panel import VIEW3D_PT_load_data
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.video_export_panel import VIEW3D_PT_freemocap_video_export
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.visualizer_panel import VIEW3D_PT_data_view_panel

BLENDER_USER_INTERFACE_CLASSES = [FREEMOCAP_CORE_PROPERTIES,
                                  FREEMOCAP_UI_PROPERTIES,
                                  VIEW3D_PT_freemocap_main_panel,
                                  VIEW3D_PT_load_data,
                                  # VIEW3D_PT_freemocap_video_export,
                                  VIEW3D_PT_data_view_panel] + BLENDER_OPERATORS

