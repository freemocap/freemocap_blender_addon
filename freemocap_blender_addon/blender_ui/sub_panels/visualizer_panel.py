import enum

import bpy

class ViewPanelPropNames(enum.Enum):
    SHOW_ARMATURE = "show_armature"
    SHOW_SKELLY_MESH = "show_skelly_mesh"
    SHOW_TRACKED_POINTS = "show_tracked_points"
    SHOW_RIGID_BODIES = "show_rigid_bodies"
    SHOW_CENTER_OF_MASS = "show_center_of_mass"
    SHOW_VIDEOS = "show_videos"
    SHOW_COM_VERTICAL_PROJECTION = "show_com_vertical_projection"
    SHOW_JOINT_ANGLES = "show_joint_angles"
    SHOW_BASE_OF_SUPPORT = "show_base_of_support"

    MOTION_PATH_SHOW_LINE = "motion_path_show_line"
    MOTION_PATH_LINE_THICKNESS = "motion_path_line_thickness"
    MOTION_PATH_USE_CUSTOM_COLOR = "motion_path_use_custom_color"
    MOTION_PATH_LINE_COLOR = "motion_path_line_color"
    MOTION_PATH_FRAMES_BEFORE = "motion_path_frames_before"
    MOTION_PATH_FRAMES_AFTER = "motion_path_frames_after"
    MOTION_PATH_FRAME_STEP = "motion_path_frame_step"
    MOTION_PATH_SHOW_FRAME_NUMBERS = "motion_path_show_frame_numbers"
    MOTION_PATH_SHOW_KEYFRAMES = "motion_path_show_keyframes"
    MOTION_PATH_SHOW_KEYFRAME_NUMBER = "motion_path_show_keyframe_number"
    MOTION_PATH_CENTER_OF_MASS = "motion_path_center_of_mass"
    MOTION_PATH_HEAD_CENTER = "motion_path_head_center"
    MOTION_PATH_NECK_CENTER = "motion_path_neck_center"
    MOTION_PATH_HIPS_CENTER = "motion_path_hips_center"
    MOTION_PATH_RIGHT_SHOULDER = "motion_path_right_shoulder"
    MOTION_PATH_LEFT_SHOULDER = "motion_path_left_shoulder"
    MOTION_PATH_RIGHT_ELBOW = "motion_path_right_elbow"
    MOTION_PATH_LEFT_ELBOW = "motion_path_left_elbow"
    MOTION_PATH_RIGHT_WRIST = "motion_path_right_wrist"
    MOTION_PATH_LEFT_WRIST = "motion_path_left_wrist"
    MOTION_PATH_RIGHT_HIP = "motion_path_right_hip"
    MOTION_PATH_LEFT_HIP = "motion_path_left_hip"
    MOTION_PATH_RIGHT_KNEE = "motion_path_right_knee"
    MOTION_PATH_LEFT_KNEE = "motion_path_left_knee"
    MOTION_PATH_RIGHT_ANKLE = "motion_path_right_ankle"
    MOTION_PATH_LEFT_ANKLE = "motion_path_left_ankle"

    COM_VERTICAL_PROJECTION_NEUTRAL_COLOR = "com_vertical_projection_neutral_color"
    COM_VERTICAL_PROJECTION_IN_BOS_COLOR = "com_vertical_projection_in_bos_color"
    COM_VERTICAL_PROJECTION_OUT_BOS_COLOR = "com_vertical_projection_out_bos_color"

    JOINT_ANGLES_COLOR = "joint_angles_color"
    JOINT_ANGLES_TEXT_COLOR = "joint_angles_text_color"

    BASE_OF_SUPPORT_Z_THRESHOLD = "base_of_support_z_threshold"
    BASE_OF_SUPPORT_POINT_RADIUS = "base_of_support_point_radius"
    BASE_OF_SUPPORT_COLOR = "base_of_support_color"

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
        row.label(text="Toggle Data Visibility")

        if ui_props.show_base_elements_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_ARMATURE.value)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_SKELLY_MESH.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_TRACKED_POINTS.value)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_RIGID_BODIES.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_CENTER_OF_MASS.value)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_VIDEOS.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_COM_VERTICAL_PROJECTION.value)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_JOINT_ANGLES.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.SHOW_BASE_OF_SUPPORT.value)

        # Motion Paths
        row = layout.row(align=True)
        row.prop(ui_props, "show_motion_paths_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_motion_paths_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Motion Paths")
        if ui_props.show_motion_paths_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_LINE.value)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Thickness")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LINE_THICKNESS.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_USE_CUSTOM_COLOR.value)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Color")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LINE_COLOR.value)
            split = box.column().row().split(factor=0.5)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frames Before")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_FRAMES_BEFORE.value)
            split_3 = split.column().split(factor=0.5)
            split_3.column().label(text="Frames After")
            split_3.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_FRAMES_AFTER.value)
            split = box.column().row().split(factor=0.5)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frame Step")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_FRAME_STEP.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_FRAME_NUMBERS.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_KEYFRAMES.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_KEYFRAME_NUMBER.value)
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_CENTER_OF_MASS.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_HEAD_CENTER.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_NECK_CENTER.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_HIPS_CENTER.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_RIGHT_SHOULDER.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LEFT_SHOULDER.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_RIGHT_ELBOW.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LEFT_ELBOW.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_RIGHT_WRIST.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LEFT_WRIST.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_RIGHT_HIP.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LEFT_HIP.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_RIGHT_KNEE.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LEFT_KNEE.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_RIGHT_ANKLE.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LEFT_ANKLE.value)

        # COM Vertical Projection
        row = layout.row(align=True)
        row.prop(ui_props, "show_com_vertical_projection_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_com_vertical_projection_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="COM Vertical Projection")

        if ui_props.show_com_vertical_projection_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Neutral Color:")
            split.column().prop(ui_props, ViewPanelPropNames.COM_VERTICAL_PROJECTION_NEUTRAL_COLOR.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="In BOS Color:")
            split.column().prop(ui_props, ViewPanelPropNames.COM_VERTICAL_PROJECTION_IN_BOS_COLOR.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Out of BOS Color:")
            split.column().prop(ui_props, ViewPanelPropNames.COM_VERTICAL_PROJECTION_OUT_BOS_COLOR.value)
            box.operator('freemocap._add_com_vertical_projection', text='Add COM Vertical Projection')


        # Base of Support
        row = layout.row(align=True)
        row.prop(ui_props, "show_base_of_support_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_base_of_support_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Base of Support")
        
        if ui_props.show_base_of_support_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Z Threshold (m):")
            split.column().prop(ui_props, ViewPanelPropNames.BASE_OF_SUPPORT_Z_THRESHOLD.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Point of Contact Radius (cm):")
            split.column().prop(ui_props, ViewPanelPropNames.BASE_OF_SUPPORT_POINT_RADIUS.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Base of Support Color:")
            split.column().prop(ui_props, ViewPanelPropNames.BASE_OF_SUPPORT_COLOR.value)
            box.operator('freemocap._add_base_of_support', text='Add Base of Support')
        #
        # # Joint Angles
        # row = layout.row(align=True)
        # row.prop(ui_props, "show_joint_angles_options", text="",
        #          icon='TRIA_DOWN' if ui_props.show_joint_angles_options else 'TRIA_RIGHT', emboss=False)
        # row.label(text="Joint Angles")
        #
        # if ui_props.show_joint_angles_options:
        #     box = layout.box()
        #     split = box.column().row().split(factor=0.5)
        #     split.column().label(text="Angle Color:")
        #     split.column().prop(ui_props, ViewPanelPropNames.JOINT_ANGLES_COLOR.value)
        #     split = box.column().row().split(factor=0.5)
        #     split.column().label(text="Text Color:")
        #     split.column().prop(ui_props, ViewPanelPropNames.JOINT_ANGLES_TEXT_COLOR.value)
        #     box.operator('freemocap._add_joint_angles', text='Add Joint Angles')
