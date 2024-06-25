from skelly_blender.blender_interface.main_view3d_panel import VIEW3D_PT_freemocap
from skelly_blender.blender_interface.operators import BLENDER_OPERATORS
from skelly_blender.blender_interface.properties.properties import SKELLY_BLENDER_PROPERTIES

BLENDER_USER_INTERFACE_CLASSES = [SKELLY_BLENDER_PROPERTIES,
                                  VIEW3D_PT_freemocap,
                                  *BLENDER_OPERATORS,
                                  ]
