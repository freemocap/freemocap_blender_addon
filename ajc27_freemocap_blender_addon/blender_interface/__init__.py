from ajc27_freemocap_blender_addon.blender_interface.main_view3d_panel import VIEW3D_PT_freemocap
from ajc27_freemocap_blender_addon.blender_interface.operators import BLENDER_OPERATORS
from ajc27_freemocap_blender_addon.blender_interface.properties.properties import FMC_ADAPTER_PROPERTIES

BLENDER_USER_INTERFACE_CLASSES = [FMC_ADAPTER_PROPERTIES,
                                  VIEW3D_PT_freemocap,
                                  *BLENDER_OPERATORS,
                                  ]
