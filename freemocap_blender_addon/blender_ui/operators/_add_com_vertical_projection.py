from lib2to3.pgen2.tokenize import Operator

from freemocap_blender_addon.blender_ui.ui_utilities import add_com_vertical_projection


class FMC_VISUALIZER_ADD_COM_VERTICAL_PROJECTION(Operator):
    bl_idname = 'fmc_visualizer.add_com_vertical_projection'
    bl_label = 'Add COM Vertical Projection'
    bl_description = "Add COM Vertical Projection"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_visualizer_tool = scene.fmc_visualizer_tool

        print("Adding COM Vertical Projection.......")

        # Add COM Vertical Projection
        add_com_vertical_projection(neutral_color=fmc_visualizer_tool.com_vertical_projection_neutral_color,
                                    in_bos_color=fmc_visualizer_tool.com_vertical_projection_in_bos_color,
                                    out_bos_color=fmc_visualizer_tool.com_vertical_projection_out_bos_color)

        # Set the show COM Vertical Projection property to True
        fmc_visualizer_tool.show_com_vertical_projection = True

        return {'FINISHED'}
