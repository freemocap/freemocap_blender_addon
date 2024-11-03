from skellyblender.ui.main_view3d_panel import VIEW3D_PT_freemocap
from skellyblender.ui.operators import BLENDER_OPERATORS
from skellyblender.ui.properties.properties import SKELLY_BLENDER_PROPERTIES

BLENDER_USER_INTERFACE_CLASSES = [SKELLY_BLENDER_PROPERTIES,
                                  VIEW3D_PT_freemocap,
                                  *BLENDER_OPERATORS,
                                  ]
