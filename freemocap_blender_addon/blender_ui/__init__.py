from freemocap_blender_addon.blender_ui.main_view3d_panel import VIEW3D_PT_freemocap
from freemocap_blender_addon.blender_ui.operators import BLENDER_OPERATORS
from freemocap_blender_addon.blender_ui.properties.core_properties import FMC_ADAPTER_PROPERTIES

BLENDER_USER_INTERFACE_CLASSES = [FMC_ADAPTER_PROPERTIES,
                                  VIEW3D_PT_freemocap,
                                  *BLENDER_OPERATORS,
                                  ]
