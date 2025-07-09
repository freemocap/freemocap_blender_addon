
import bpy

from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.ui_utilities import add_joint_angles
from ajc27_freemocap_blender_addon.data_models.joint_angles.joint_angles import joint_angles


class FREEMOCAP_OT_add_joint_angles(bpy.types.Operator):
    bl_idname = 'freemocap._add_joint_angles'
    bl_label = 'Add Joint Angles'
    bl_description = "Add Joint Angles"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene

        print("Adding Joint Angles.......")

        joint_angles_properties = context.scene.freemocap_ui_properties.add_joint_angles_properties
        # props = context.scene.freemocap_ui_properties.limit_markers_range_of_motion_properties

        # Get the list of joint angles
        joint_angle_group = joint_angles_properties.joint_angle

        joint_angle_list = []

        if joint_angle_group == 'all':
            joint_angle_list = list(joint_angles.keys())
        elif 'segment' in joint_angle_group:
            segment_name = joint_angle_group.split('_')[1]
            joint_angle_list = list(set([joint_angle for joint_angle in joint_angles.keys() if joint_angles[joint_angle]['segment'] == segment_name]))
        else:
            joint_angle_list = [joint_angle_group]
        
        print(f"Joint angles: {joint_angle_list}")

        # Calculate the joint angle values
        # get_joint_angle_values(joint_angle_list)

        # # Add Joint Angles
        # add_joint_angles(angles_color=scene.freemocap_ui_properties.joint_angles_color,
        #                  text_color=scene.freemocap_ui_properties.joint_angles_text_color)

        # # Set the show Joint Angles property to True
        # scene.freemocap_ui_properties.show_joint_angles = True

        return {'FINISHED'}
