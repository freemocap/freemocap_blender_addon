from lib2to3.pgen2.tokenize import Operator

import bpy

from freemocap_blender_addon.blender_ui.ui_utilities import add_com_vertical_projection, add_base_of_support


class FREEMOCAP_OT_add_base_of_support(bpy.types.Operator):
    bl_idname = 'freemocap._add_base_of_support'
    bl_label = 'Add Base of Support'
    bl_description = "Add Base of Support"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):


        print("Adding Base of Support.......")
        ui_props = context.scene.freemocap_ui_properties
        # Check if the COM_Vertical_Projection object exists, if not create it
        if bpy.data.objects.get("COM_Vertical_Projection") is None:
            add_com_vertical_projection(neutral_color=ui_props.com_vertical_projection_neutral_color,
                                        in_bos_color=ui_props.com_vertical_projection_in_bos_color,
                                        out_bos_color=ui_props.com_vertical_projection_out_bos_color)

            # Set the show COM Vertical Projection property to True
            ui_props.show_com_vertical_projection = True

        # Add Base of Support
        add_base_of_support(z_threshold=ui_props.base_of_support_z_threshold,
                            point_of_contact_radius=ui_props.base_of_support_point_radius,
                            color=ui_props.base_of_support_color)

        # Set the show Base of Support property to True
        ui_props.show_base_of_support = True

        return {'FINISHED'}
