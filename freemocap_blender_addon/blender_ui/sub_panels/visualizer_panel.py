from bpy.types import Panel

class VIEW3D_PT_freemocap_visualizer(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Freemocap Visualizer"
    bl_label = "Freemocap Visualizer"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        fmc_visualizer_tool = scene.fmc_visualizer_tool

        # Base Elements
        row = layout.row(align=True)
        row.prop(fmc_visualizer_tool,
                 "show_base_elements_options",
                 text="",
                 icon='TRIA_DOWN' if fmc_visualizer_tool.show_base_elements_options else 'TRIA_RIGHT',
                 emboss=False)
        row.label(text="Base Elements")

        if fmc_visualizer_tool.show_base_elements_options:
            box = layout.box()

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'show_armature')
            split.column().prop(fmc_visualizer_tool, 'show_body_mesh')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'show_markers')
            split.column().prop(fmc_visualizer_tool, 'show_rigid_body')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'show_center_of_mass')
            split.column().prop(fmc_visualizer_tool, 'show_videos')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'show_com_vertical_projection')
            split.column().prop(fmc_visualizer_tool, 'show_joint_angles')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'show_base_of_support')

        # Motion Paths
        row = layout.row(align=True)
        row.prop(fmc_visualizer_tool, "show_motion_paths_options", text="",
                 icon='TRIA_DOWN' if fmc_visualizer_tool.show_motion_paths_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Motion Paths")

        if fmc_visualizer_tool.show_motion_paths_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_show_line')
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Thickness")
            split_2.column().prop(fmc_visualizer_tool, 'motion_path_line_thickness')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_use_custom_color')
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Color")
            split_2.column().prop(fmc_visualizer_tool, 'motion_path_line_color')

            split = box.column().row().split(factor=0.5)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frames Before")
            split_2.column().prop(fmc_visualizer_tool, 'motion_path_frames_before')
            split_3 = split.column().split(factor=0.5)
            split_3.column().label(text="Frames After")
            split_3.column().prop(fmc_visualizer_tool, 'motion_path_frames_after')

            split = box.column().row().split(factor=0.5)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frame Step")
            split_2.column().prop(fmc_visualizer_tool, 'motion_path_frame_step')
            split.column().prop(fmc_visualizer_tool, 'motion_path_show_frame_numbers')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_show_keyframes')
            split.column().prop(fmc_visualizer_tool, 'motion_path_show_keyframe_number')

            box = layout.box()

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_center_of_mass')
            split.column().prop(fmc_visualizer_tool, 'motion_path_head_center')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_neck_center')
            split.column().prop(fmc_visualizer_tool, 'motion_path_hips_center')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_right_shoulder')
            split.column().prop(fmc_visualizer_tool, 'motion_path_left_shoulder')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_right_elbow')
            split.column().prop(fmc_visualizer_tool, 'motion_path_left_elbow')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_right_wrist')
            split.column().prop(fmc_visualizer_tool, 'motion_path_left_wrist')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_right_hip')
            split.column().prop(fmc_visualizer_tool, 'motion_path_left_hip')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_right_knee')
            split.column().prop(fmc_visualizer_tool, 'motion_path_left_knee')

            split = box.column().row().split(factor=0.5)
            split.column().prop(fmc_visualizer_tool, 'motion_path_right_ankle')
            split.column().prop(fmc_visualizer_tool, 'motion_path_left_ankle')

        # COM Vertical Projection
        row = layout.row(align=True)
        row.prop(fmc_visualizer_tool, "show_com_vertical_projection_options", text="",
                 icon='TRIA_DOWN' if fmc_visualizer_tool.show_com_vertical_projection_options else 'TRIA_RIGHT',
                 emboss=False)
        row.label(text="COM Vertical Projection")

        if fmc_visualizer_tool.show_com_vertical_projection_options:
            box = layout.box()

            split = box.column().row().split(factor=0.5)
            split.column().label(text="Neutral Color:")
            split.column().prop(fmc_visualizer_tool, 'com_vertical_projection_neutral_color')

            split = box.column().row().split(factor=0.5)
            split.column().label(text="In BOS Color:")
            split.column().prop(fmc_visualizer_tool, 'com_vertical_projection_in_bos_color')

            split = box.column().row().split(factor=0.5)
            split.column().label(text="Out of BOS Color:")
            split.column().prop(fmc_visualizer_tool, 'com_vertical_projection_out_bos_color')

            box.operator('fmc_visualizer.add_com_vertical_projection', text='Add COM Vertical Projection')

        # Joint Angles
        row = layout.row(align=True)
        row.prop(fmc_visualizer_tool, "show_joint_angles_options", text="",
                 icon='TRIA_DOWN' if fmc_visualizer_tool.show_joint_angles_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Joint Angles")

        if fmc_visualizer_tool.show_joint_angles_options:
            box = layout.box()

            split = box.column().row().split(factor=0.5)
            split.column().label(text="Angle Color:")
            split.column().prop(fmc_visualizer_tool, 'joint_angles_color')

            split = box.column().row().split(factor=0.5)
            split.column().label(text="Text Color:")
            split.column().prop(fmc_visualizer_tool, 'joint_angles_text_color')

            box.operator('fmc_visualizer.add_joint_angles', text='Add Joint Angles')

        # Base of Support
        row = layout.row(align=True)
        row.prop(fmc_visualizer_tool,
                 "show_base_of_support_options",
                 text="",
                 icon='TRIA_DOWN' if fmc_visualizer_tool.show_base_of_support_options else 'TRIA_RIGHT',
                 emboss=False)
        row.label(text="Base of Support")

        if fmc_visualizer_tool.show_base_of_support_options:
            box = layout.box()

            split = box.column().row().split(factor=0.5)
            split.column().label(text="Z Threshold (m):")
            split.column().prop(fmc_visualizer_tool, 'base_of_support_z_threshold')

            split = box.column().row().split(factor=0.5)
            split.column().label(text="Point of Contact Radius (cm):")
            split.column().prop(fmc_visualizer_tool, 'base_of_support_point_radius')

            split = box.column().row().split(factor=0.5)
            split.column().label(text="Base of Support Color:")
            split.column().prop(fmc_visualizer_tool, 'base_of_support_color')

            box.operator('fmc_visualizer.add_base_of_support', text='Add Base of Support')
