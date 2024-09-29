
from freemocap_blender_addon.blender_ui.ui_utilities import add_com_vertical_projection

import bpy

class FREEMOCAP_OT_add_com_vertical_projection(bpy.types.Operator):
    bl_idname = 'freemocap._add_com_vertical_projection'
    bl_label = 'Add COM Vertical Projection'
    bl_description = "Add COM Vertical Projection"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Adding COM Vertical Projection.......")

        # Add COM Vertical Projection
        add_com_vertical_projection(neutral_color=context.scene.freemocap_ui_properties.com_vertical_projection_neutral_color,
                                    in_bos_color=context.scene.freemocap_ui_properties.com_vertical_projection_in_bos_color,
                                    out_bos_color=context.scene.freemocap_ui_properties.com_vertical_projection_out_bos_color)

        # Set the show COM Vertical Projection property to True
        context.scene.freemocap_ui_properties.show_com_vertical_projection = True

        return {'FINISHED'}
