from ajc27_freemocap_blender_addon.blender_ui.main_view3d_panel import VIEW3D_PT_freemocap_main_panel
from ajc27_freemocap_blender_addon.blender_ui.operators import BLENDER_OPERATORS
from ajc27_freemocap_blender_addon.blender_ui.properties.core_properties import FREEMOCAP_CORE_PROPERTIES
from ajc27_freemocap_blender_addon.blender_ui.properties.ui_properties import FREEMOCAP_UI_PROPERTIES
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.retarget_animation_properties import (
    RetargetAnimationProperties,
    RetargetBonePair,
    UL_RetargetPairs,
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.set_bone_rotation_limits_properties import (
    SetBoneRotationLimitsProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.limit_markers_range_of_motion_properties import (
    LimitMarkersRangeOfMotionProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.export_3d_model_properties import (
    Export3DModelProperties
)
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.load_data_panel import VIEW3D_PT_load_data
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.video_export_panel import VIEW3D_PT_freemocap_video_export
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.visualizer_panel import VIEW3D_PT_data_view_panel
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.animation_panel import VIEW3D_PT_animation_panel
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.export_3d_model_panel import VIEW3D_PT_export_3d_model_panel

BLENDER_USER_INTERFACE_CLASSES = [FREEMOCAP_CORE_PROPERTIES,
                                  RetargetBonePair,
                                  RetargetAnimationProperties,
                                  UL_RetargetPairs,
                                  SetBoneRotationLimitsProperties,
                                  LimitMarkersRangeOfMotionProperties,
                                  Export3DModelProperties,
                                  FREEMOCAP_UI_PROPERTIES,
                                  VIEW3D_PT_freemocap_main_panel,
                                  VIEW3D_PT_load_data,
                                  # VIEW3D_PT_freemocap_video_export,
                                  VIEW3D_PT_data_view_panel,
                                  VIEW3D_PT_animation_panel,
                                  VIEW3D_PT_export_3d_model_panel] + BLENDER_OPERATORS

 