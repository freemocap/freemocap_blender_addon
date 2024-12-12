
import bpy

from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.ui_utilities import add_joint_angles


class FREEMOCAP_OT_add_joint_angles(bpy.types.Operator):
    bl_idname = 'freemocap._add_joint_angles'
    bl_label = 'Add Joint Angles'
    bl_description = "Add Joint Angles"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene

        print("Adding Joint Angles.......")

        # Add Joint Angles
        add_joint_angles(angles_color=scene.freemocap_ui_properties.joint_angles_color,
                         text_color=scene.freemocap_ui_properties.joint_angles_text_color)

        # Set the show Joint Angles property to True
        scene.freemocap_ui_properties.show_joint_angles = True

        return {'FINISHED'}
