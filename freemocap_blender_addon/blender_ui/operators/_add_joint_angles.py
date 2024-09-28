from lib2to3.pgen2.tokenize import Operator

from freemocap_blender_addon.blender_ui.ui_utilities import add_joint_angles


class FMC_VISUALIZER_ADD_JOINT_ANGLES(Operator):
    bl_idname = 'fmc_visualizer.add_joint_angles'
    bl_label = 'Add Joint Angles'
    bl_description = "Add Joint Angles"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_visualizer_tool = scene.fmc_visualizer_tool

        print("Adding Joint Angles.......")

        # Add Joint Angles
        add_joint_angles(angles_color=fmc_visualizer_tool.joint_angles_color,
                         text_color=fmc_visualizer_tool.joint_angles_text_color)

        # Set the show Joint Angles property to True
        fmc_visualizer_tool.show_joint_angles = True

        return {'FINISHED'}
