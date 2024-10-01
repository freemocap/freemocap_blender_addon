import bpy

from freemocap_blender_addon.blender_ui.ui_utilities import add_base_of_support
from freemocap_blender_addon.core_functions.com_bos.add_com_vertical_projection import add_com_vertical_projection


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
            data_parent_object = context.scene.freemocap_properties.data_parent_empty
            add_com_vertical_projection(data_parent_object=data_parent_object,
                                        neutral_color=ui_props.com_vertical_projection_neutral_color,
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
