from lib2to3.pgen2.tokenize import Operator

import bpy

from freemocap_blender_addon.blender_ui.ui_utilities import add_com_vertical_projection, add_base_of_support


class FMC_VISUALIZER_ADD_BASE_OF_SUPPORT(Operator):
    bl_idname = 'fmc_visualizer.add_base_of_support'
    bl_label = 'Add Base of Support'
    bl_description = "Add Base of Support"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_visualizer_tool = scene.fmc_visualizer_tool

        print("Adding Base of Support.......")

        # Check if the COM_Vertical_Projection object exists, if not create it
        if bpy.data.objects.get("COM_Vertical_Projection") is None:
            add_com_vertical_projection(neutral_color=fmc_visualizer_tool.com_vertical_projection_neutral_color,
                                        in_bos_color=fmc_visualizer_tool.com_vertical_projection_in_bos_color,
                                        out_bos_color=fmc_visualizer_tool.com_vertical_projection_out_bos_color)

            # Set the show COM Vertical Projection property to True
            fmc_visualizer_tool.show_com_vertical_projection = True

        # Add Base of Support
        add_base_of_support(z_threshold=fmc_visualizer_tool.base_of_support_z_threshold,
                            point_of_contact_radius=fmc_visualizer_tool.base_of_support_point_radius,
                            color=fmc_visualizer_tool.base_of_support_color)

        # Set the show Base of Support property to True
        fmc_visualizer_tool.show_base_of_support = True

        return {'FINISHED'}
