import bpy
class VIEW3D_PT_data_view_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Data View Settings"
    bl_parent_id = "view3d.pt_freemocap_main_panel"

    def draw(self, context):
        layout = self.layout
        if context.scene.freemocap_properties.data_parent_empty is None:
            layout.label(text="Load a recording session to view data settings.")
            return
        ui_props = context.scene.freemocap_ui_properties

        # Base Elements
        row = layout.row(align=True)
        row.prop(ui_props, "show_base_elements_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_base_elements_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Base Elements")

        if ui_props.show_base_elements_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'show_armature')
            split.column().prop(ui_props, 'show_body_mesh')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'show_markers')
            split.column().prop(ui_props, 'show_rigid_body')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'show_center_of_mass')
            split.column().prop(ui_props, 'show_videos')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'show_com_vertical_projection')
            split.column().prop(ui_props, 'show_joint_angles')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'show_base_of_support')

        # Motion Paths
        row = layout.row(align=True)
        row.prop(ui_props, "show_motion_paths_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_motion_paths_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Motion Paths")

        if ui_props.show_motion_paths_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_show_line')
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Thickness")
            split_2.column().prop(ui_props, 'motion_path_line_thickness')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_use_custom_color')
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Color")
            split_2.column().prop(ui_props, 'motion_path_line_color')
            split = box.column().row().split(factor=0.5)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frames Before")
            split_2.column().prop(ui_props, 'motion_path_frames_before')
            split_3 = split.column().split(factor=0.5)
            split_3.column().label(text="Frames After")
            split_3.column().prop(ui_props, 'motion_path_frames_after')
            split = box.column().row().split(factor=0.5)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frame Step")
            split_2.column().prop(ui_props, 'motion_path_frame_step')
            split.column().prop(ui_props, 'motion_path_show_frame_numbers')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_show_keyframes')
            split.column().prop(ui_props, 'motion_path_show_keyframe_number')
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_center_of_mass')
            split.column().prop(ui_props, 'motion_path_head_center')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_neck_center')
            split.column().prop(ui_props, 'motion_path_hips_center')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_right_shoulder')
            split.column().prop(ui_props, 'motion_path_left_shoulder')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_right_elbow')
            split.column().prop(ui_props, 'motion_path_left_elbow')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_right_wrist')
            split.column().prop(ui_props, 'motion_path_left_wrist')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_right_hip')
            split.column().prop(ui_props, 'motion_path_left_hip')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_right_knee')
            split.column().prop(ui_props, 'motion_path_left_knee')
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, 'motion_path_right_ankle')
            split.column().prop(ui_props, 'motion_path_left_ankle')

        # COM Vertical Projection
        row = layout.row(align=True)
        row.prop(ui_props, "show_com_vertical_projection_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_com_vertical_projection_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="COM Vertical Projection")

        if ui_props.show_com_vertical_projection_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Neutral Color:")
            split.column().prop(ui_props, 'com_vertical_projection_neutral_color')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="In BOS Color:")
            split.column().prop(ui_props, 'com_vertical_projection_in_bos_color')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Out of BOS Color:")
            split.column().prop(ui_props, 'com_vertical_projection_out_bos_color')
            box.operator('freemocap._add_com_vertical_projection', text='Add COM Vertical Projection')

        # Joint Angles
        row = layout.row(align=True)
        row.prop(ui_props, "show_joint_angles_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_joint_angles_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Joint Angles")

        if ui_props.show_joint_angles_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Angle Color:")
            split.column().prop(ui_props, 'joint_angles_color')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Text Color:")
            split.column().prop(ui_props, 'joint_angles_text_color')
            box.operator('freemocap._add_joint_angles', text='Add Joint Angles')

        # Base of Support
        row = layout.row(align=True)
        row.prop(ui_props, "show_base_of_support_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_base_of_support_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Base of Support")

        if ui_props.show_base_of_support_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Z Threshold (m):")
            split.column().prop(ui_props, 'base_of_support_z_threshold')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Point of Contact Radius (cm):")
            split.column().prop(ui_props, 'base_of_support_point_radius')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Base of Support Color:")
            split.column().prop(ui_props, 'base_of_support_color')
            box.operator('freemocap._add_base_of_support', text='Add Base of Support')