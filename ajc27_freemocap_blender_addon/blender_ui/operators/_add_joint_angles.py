import bpy
import numpy as np

from ajc27_freemocap_blender_addon.core_functions.joint_angles.add_joint_angles import add_joint_angles
from ajc27_freemocap_blender_addon.data_models.joint_angles.joint_angles import joint_angles


class FREEMOCAP_OT_add_joint_angles(bpy.types.Operator):
    bl_idname = 'freemocap._add_joint_angles'
    bl_label = 'Add Joint Angles'
    bl_description = "Add Joint Angles"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene

        data_parent_empty = bpy.data.objects[scene.freemocap_properties.scope_data_parent]

        print("Adding Joint Angles.......")

        joint_angles_properties = context.scene.freemocap_ui_properties.add_joint_angles_properties

        # Get the list of joint angles
        joint_angle_group = joint_angles_properties.joint_angle

        joint_angle_list = []

        if joint_angle_group == 'all':
            joint_angle_list = list(joint_angles.keys())
        elif 'segment' in joint_angle_group:
            segment_name = joint_angle_group.split('#')[1]
            joint_angle_list = list(set([joint_angle for joint_angle in joint_angles.keys() if joint_angles[joint_angle]['segment'] == segment_name]))
        else:
            joint_angle_list = [joint_angle_group]

        # Execute the add joint angles function
        add_joint_angles(
            data_parent_empty=data_parent_empty,
            joint_angle_list=joint_angle_list,
            angle_radius=joint_angles_properties.joint_angle_radius,
            overwrite_colors=joint_angles_properties.joint_angle_overwrite_colors,
            angle_mesh_color=joint_angles_properties.joint_angle_color,
            angle_text_color=joint_angles_properties.joint_angle_text_color,
            angle_text_size=joint_angles_properties.joint_angle_text_size,
            angle_text_orientation=joint_angles_properties.joint_angle_text_orientation,
            angle_text_local_x_offset=joint_angles_properties.joint_angle_text_local_x_offset,
            angle_text_local_y_offset=joint_angles_properties.joint_angle_text_local_y_offset,
        )

        # Set the show Joint Angles property to True
        scene.freemocap_ui_properties.show_joint_angles = True

        return {'FINISHED'}
