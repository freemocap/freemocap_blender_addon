import logging
import bpy

logger = logging.getLogger(__name__)

import bpy


# Main Parent Panel
class VIEW3D_PT_freemocap_main_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "💀FreeMoCap Blender Addon"
    bl_idname = "view3d.pt_freemocap_main_panel"

    def draw(self, context):
        pass
        # layout = self.layout
        # layout.label(text="FreeMoCap Addon")


