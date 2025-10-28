import enum
import re

import bpy

class ViewPanelPropNamesElements(enum.Enum):
    def __init__(self, property_name, object_name_pattern, object_type):
        self.property_name = property_name
        self.object_name_pattern = object_name_pattern
        self.object_type = object_type

    SHOW_ARMATURE = ("show_armature", "_rig(\.\d+)?$", "ARMATURE")
    SHOW_SKELLY_MESH = ("show_skelly_mesh", "skelly_mesh", "MESH")
    SHOW_TRACKED_POINTS = ("show_tracked_points", "empties_parent", "EMPTY")
    SHOW_RIGID_BODIES = ("show_rigid_bodies", "rigid_body_meshes_parent", "EMPTY")
    SHOW_CENTER_OF_MASS = ("show_center_of_mass", "center_of_mass", "MESH")
    SHOW_VIDEOS = ("show_videos", "videos_parent", "EMPTY")
    SHOW_COM_VERTICAL_PROJECTION = ("show_com_vertical_projection", "com_vertical_projection", "MESH")
    SHOW_BASE_OF_SUPPORT = ("show_base_of_support", "base_of_support", "MESH")
    SHOW_JOINT_ANGLES = ("show_joint_angles", "joint_angles_parent", "EMPTY")
    

class ViewPanelPropNames(enum.Enum):
    
    MOTION_PATH_SHOW_LINE = "motion_path_show_line"
    MOTION_PATH_LINE_THICKNESS = "motion_path_line_thickness"
    MOTION_PATH_USE_CUSTOM_COLOR = "motion_path_use_custom_color"
    MOTION_PATH_LINE_COLOR = "motion_path_line_color"
    MOTION_PATH_LINE_COLOR_POST = "motion_path_line_color_post"
    MOTION_PATH_FRAMES_BEFORE = "motion_path_frames_before"
    MOTION_PATH_FRAMES_AFTER = "motion_path_frames_after"
    MOTION_PATH_FRAME_STEP = "motion_path_frame_step"
    MOTION_PATH_SHOW_FRAME_NUMBERS = "motion_path_show_frame_numbers"
    MOTION_PATH_SHOW_KEYFRAMES = "motion_path_show_keyframes"
    MOTION_PATH_SHOW_KEYFRAME_NUMBER = "motion_path_show_keyframe_number"
    MOTION_PATH_TARGET_ELEMENT = "motion_path_target_element"
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

    BASE_OF_SUPPORT_Z_THRESHOLD = "base_of_support_z_threshold"
    BASE_OF_SUPPORT_POINT_RADIUS = "base_of_support_point_radius"
    BASE_OF_SUPPORT_COLOR = "base_of_support_color"

    JOINT_ANGLE = "joint_angle"
    JOINT_ANGLE_RADIUS = "joint_angle_radius"
    JOINT_ANGLE_OVERWRITE_COLORS = "joint_angle_overwrite_colors"
    JOINT_ANGLE_COLOR = "joint_angle_color"
    JOINT_ANGLE_TEXT_COLOR = "joint_angle_text_color"
    JOINT_ANGLE_TEXT_SIZE = "joint_angle_text_size"
    JOINT_ANGLE_TEXT_ORIENTATION = "joint_angle_text_orientation"
    JOINT_ANGLE_TEXT_LOCAL_X_OFFSET = "joint_angle_text_local_x_offset"
    JOINT_ANGLE_TEXT_LOCAL_Y_OFFSET = "joint_angle_text_local_y_offset"
    

class VIEW3D_PT_data_view_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Data View Settings"
    bl_parent_id = "VIEW3D_PT_freemocap_main_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        
        # Check if there is loaded data, set a message if not
        try:
            scope_data_parent = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]
        except KeyError:
            layout = self.layout
            layout.label(text="Load a recording session to view data settings.")
            return
        ui_props = context.scene.freemocap_ui_properties

        # Create a row with one column blank for indentation
        row = self.layout.row()
        row.label(text="", icon='BLANK1')

        layout = row.column(align=True)

        # Base Elements
        row = layout.row(align=True)
        row.prop(ui_props, "show_base_elements_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_base_elements_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Toggle Data Visibility")

        if ui_props.show_base_elements_options:
            box = layout.box()

            index = 0
            for base_element in ViewPanelPropNamesElements:
                object_name_pattern = base_element.object_name_pattern
                object_type = base_element.object_type
                element_exists = any(re.search(object_name_pattern, child.name) and child.type == object_type for child in scope_data_parent.children_recursive)
                if element_exists:
                    if index % 2 == 0:  # even index
                        split = box.column().row().split(factor=0.5)
                    split.column().prop(ui_props, base_element.property_name)
                    index += 1

        # Motion Paths
        row = layout.row(align=True)
        row.prop(ui_props, "show_motion_paths_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_motion_paths_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Motion Paths")
        if ui_props.show_motion_paths_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Target Element:")
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_TARGET_ELEMENT.value)

            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_LINE.value)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Thickness:")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LINE_THICKNESS.value)

            split = box.column().row().split(factor=0.25)
            split.column().label(text="Range Before:")
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frames:")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_FRAMES_BEFORE.value)
            split_3 = split.column().split(factor=0.3)
            split_3.column().label(text="Color:")
            split_3.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LINE_COLOR.value)

            split = box.column().row().split(factor=0.25)
            split.column().label(text="Range After:")
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frames:")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_FRAMES_AFTER.value)
            split_3 = split.column().split(factor=0.3)
            split_3.column().label(text="Color:")
            split_3.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_LINE_COLOR_POST.value)

            split = box.column().row().split(factor=0.5)
            split_2 = split.column().split(factor=0.5)
            split_2.column().label(text="Frame Step:")
            split_2.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_FRAME_STEP.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_FRAME_NUMBERS.value)
            split = box.column().row().split(factor=0.5)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_KEYFRAMES.value)
            split.column().prop(ui_props, ViewPanelPropNames.MOTION_PATH_SHOW_KEYFRAME_NUMBER.value)

            split = box.column().row().split(factor=0.6)
            split1 = split.column().row().split(factor=0.5)
            split1.operator('freemocap._add_motion_path', text='Add Motion Path')
            split1.operator('freemocap._clear_motion_path', text='Clear Motion Path')
            split.operator('freemocap._clear_all_motion_paths', text='Clear All Motion Paths')

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

        # # Joint Angles
        row = layout.row(align=True)
        row.prop(ui_props, "show_joint_angles_options", text="",
                 icon='TRIA_DOWN' if ui_props.show_joint_angles_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Joint Angles")

        if ui_props.show_joint_angles_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Joint Angle:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Angle Radius [cm]:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_RADIUS.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Overwrite Default Colors:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_OVERWRITE_COLORS.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Angle Color:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_COLOR.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Text Color:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_TEXT_COLOR.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Text Size [cm]:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_TEXT_SIZE.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Text Orientation:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_TEXT_ORIENTATION.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Local X Offset [cm]:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_TEXT_LOCAL_X_OFFSET.value)
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Local Y Offset [cm]:")
            split.column().prop(ui_props.add_joint_angles_properties, ViewPanelPropNames.JOINT_ANGLE_TEXT_LOCAL_Y_OFFSET.value)
            box.operator('freemocap._add_joint_angles', text='Add Joint Angles')

        # Data Overlays
        row = layout.row(align=True)
        row.prop(ui_props.add_data_overlays_properties, "show_add_data_overlays_options", text="",
                 icon='TRIA_DOWN' if ui_props.add_data_overlays_properties.show_add_data_overlays_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Data Overlays")

        if ui_props.add_data_overlays_properties.show_add_data_overlays_options:
            box = layout.box()
            # Common Overlay Properties
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Viewport Position:")
            split.column().prop(ui_props.add_data_overlays_properties, 'common_viewport_position')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Custom Position X (px):")
            split.column().prop(ui_props.add_data_overlays_properties, 'common_custom_position_x')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Custom Position Y (px):")
            split.column().prop(ui_props.add_data_overlays_properties, 'common_custom_position_y')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Overlay Margin (px):")
            split.column().prop(ui_props.add_data_overlays_properties, 'common_overlay_margin')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Overlay Width (px):")
            split.column().prop(ui_props.add_data_overlays_properties, 'common_overlay_width')
            split = box.column().row().split(factor=0.5)
            split.column().label(text="Overlay Height (px):")
            split.column().prop(ui_props.add_data_overlays_properties, 'common_overlay_height')
            
            # Time Series Plot Properties
            box2 = box.box()
            row = box2.row(align=True)
            row.prop(ui_props.add_data_overlays_properties, "show_time_series_plot_options", text="",
                     icon='TRIA_DOWN' if ui_props.add_data_overlays_properties.show_time_series_plot_options else 'TRIA_RIGHT', emboss=False)
            row.label(text="Time Series Plot", icon='GRAPH')
            if ui_props.add_data_overlays_properties.show_time_series_plot_options:
                split = box2.column().row().split(factor=0.3)
                split.column().label(text="Parameter:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_plot_parameter')
                split = box2.column().row().split(factor=0.5)
                split.column().label(text="Frame Window Size:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_window_size')
                split = box2.column().row().split(factor=0.5)
                split.column().label(text="Time Series Color:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_line_color')
                split = box2.column().row().split(factor=0.5)
                split.column().label(text="Current Frame Line Color:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_current_frame_line_color')
                split = box2.column().row().split(factor=0.5)
                split.column().label(text="Background Color:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_background_color')
                split = box2.column().row().split(factor=0.5)
                split.column().label(text="Line Width:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_line_width')
                split = box2.column().row().split(factor=0.5)
                split.column().label(text="Current Frame Line Width:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_current_frame_line_width')
                split = box2.column().row().split(factor=0.5)
                split.column().label(text="Border Line Width:")
                split.column().prop(ui_props.add_data_overlays_properties, 'time_series_border_line_width')

                box2.operator('freemocap._add_time_series_plot', text='Add Time Series Plot Overlay', icon='GRAPH')
            
            # ROM Gauge Properties
            box3 = box.box()
            row = box3.row(align=True)
            row.prop(ui_props.add_data_overlays_properties, "show_rom_gauge_options", text="",
                     icon='TRIA_DOWN' if ui_props.add_data_overlays_properties.show_rom_gauge_options else 'TRIA_RIGHT', emboss=False)
            row.label(text="ROM Gauge", icon='DRIVER_ROTATIONAL_DIFFERENCE')
            if ui_props.add_data_overlays_properties.show_rom_gauge_options:
                split = box3.column().row().split(factor=0.3)
                split.column().label(text="Parameter:")
                split.column().prop(ui_props.add_data_overlays_properties, 'rom_gauge_parameter')

                box3.operator('freemocap._add_rom_gauge', text='Add ROM Gauge Overlay', icon='DRIVER_ROTATIONAL_DIFFERENCE')
                

            box.operator('freemocap._clear_all_data_overlays', text='Clear All Data Overlays', icon='TRASH')