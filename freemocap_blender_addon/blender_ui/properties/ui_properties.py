import bpy

from freemocap_blender_addon.blender_ui.ui_utilities import toggle_element_visibility, update_motion_path


class FREEMOCAP_UI_PROPERTIES(bpy.types.PropertyGroup):
    show_base_elements_options: bpy.props.BoolProperty(
        name='',
        default=False,
    )  # type: ignore

    show_armature: bpy.props.BoolProperty(
        name='Armature',
        description='Show Armature',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_armature',
                                                      parent_pattern=r'_rig\Z|root\Z',
                                                      toggle_children_not_parent=False),
    )  # type: ignore

    show_body_mesh: bpy.props.BoolProperty(
        name='Body Mesh',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_body_mesh',
                                                      parent_pattern=r'skelly_mesh',
                                                      toggle_children_not_parent=False),
    )  # type: ignore

    show_markers: bpy.props.BoolProperty(
        name='Markers',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_markers',
                                                      parent_pattern=r'empties_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_rigid_body: bpy.props.BoolProperty(
        name='Rigid Body',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_rigid_body',
                                                      parent_pattern=r'rigid_body_meshes_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_center_of_mass: bpy.props.BoolProperty(
        name='Center of Mass',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_center_of_mass',
                                                      parent_pattern=r'center_of_mass_data_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_videos: bpy.props.BoolProperty(
        name='Capture Videos',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_videos',
                                                      parent_pattern=r'videos_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_com_vertical_projection: bpy.props.BoolProperty(
        name='COM Vertical Projection',
        default=False,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_com_vertical_projection',
                                                      parent_pattern=r'COM_Vertical_Projection',
                                                      toggle_children_not_parent=False),
    )  # type: ignore

    show_joint_angles: bpy.props.BoolProperty(
        name='Joint Angles',
        default=False,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_joint_angles',
                                                      parent_pattern=r'joint_angles_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_base_of_support: bpy.props.BoolProperty(
        name='Base of Support',
        default=False,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property='show_base_of_support',
                                                      parent_pattern=r'base_of_support',
                                                      toggle_children_not_parent=False),
    )  # type: ignore

    show_motion_paths_options: bpy.props.BoolProperty(
        name='',
        default=False,
    )  # type: ignore

    motion_path_show_line: bpy.props.BoolProperty(
        name='Show Line',
        default=True,
    )  # type: ignore

    motion_path_line_thickness: bpy.props.IntProperty(
        name='',
        min=1,
        max=6,
        default=6,
    )  # type: ignore

    motion_path_use_custom_color: bpy.props.BoolProperty(
        name='Use Custom Color',
        default=False,
    )  # type: ignore

    motion_path_line_color: bpy.props.FloatVectorProperty(
        name='',
        subtype='COLOR',
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0),
    )  # type: ignore

    motion_path_frames_before: bpy.props.IntProperty(
        name='',
        min=1,
        default=10,
    )  # type: ignore

    motion_path_frames_after: bpy.props.IntProperty(
        name='',
        min=1,
        default=10,
    )  # type: ignore

    motion_path_frame_step: bpy.props.IntProperty(
        name='',
        min=1,
        default=1,
    )  # type: ignore

    motion_path_show_frame_numbers: bpy.props.BoolProperty(
        name='Show Frame Numbers',
        default=False,
    )  # type: ignore

    motion_path_show_keyframes: bpy.props.BoolProperty(
        name='Show Keyframes',
        default=False,
    )  # type: ignore

    motion_path_show_keyframe_number: bpy.props.BoolProperty(
        name='Show Keyframe Number',
        default=False,
    )  # type: ignore

    motion_path_center_of_mass: bpy.props.BoolProperty(
        name='Center of Mass',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='center_of_mass'),
    )  # type: ignore

    motion_path_head_center: bpy.props.BoolProperty(
        name='Head Center',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='head_center'),
    )  # type: ignore

    motion_path_neck_center: bpy.props.BoolProperty(
        name='Neck Center',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='neck_center'),
    )  # type: ignore

    motion_path_hips_center: bpy.props.BoolProperty(
        name='Hips Center',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='hips_center'),
    )  # type: ignore

    motion_path_right_shoulder: bpy.props.BoolProperty(
        name='Right Shoulder',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='right_shoulder'),
    )  # type: ignore

    motion_path_left_shoulder: bpy.props.BoolProperty(
        name='Left Shoulder',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='left_shoulder'),
    )  # type: ignore

    motion_path_right_elbow: bpy.props.BoolProperty(
        name='Right Elbow',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='right_elbow'),
    )  # type: ignore

    motion_path_left_elbow: bpy.props.BoolProperty(
        name='Left Elbow',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='left_elbow'),
    )  # type: ignore

    motion_path_right_wrist: bpy.props.BoolProperty(
        name='Right Wrist',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='right_wrist'),
    )  # type: ignore

    motion_path_left_wrist: bpy.props.BoolProperty(
        name='Left Wrist',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='left_wrist'),
    )  # type: ignore

    motion_path_right_hip: bpy.props.BoolProperty(
        name='Right Hip',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='right_hip'),
    )  # type: ignore

    motion_path_left_hip: bpy.props.BoolProperty(
        name='Left Hip',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='left_hip'),
    )  # type: ignore

    motion_path_right_knee: bpy.props.BoolProperty(
        name='Right Knee',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='right_knee'),
    )  # type: ignore

    motion_path_left_knee: bpy.props.BoolProperty(
        name='Left Knee',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='left_knee'),
    )  # type: ignore

    motion_path_right_ankle: bpy.props.BoolProperty(
        name='Right Ankle',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='right_ankle'),
    )  # type: ignore

    motion_path_left_ankle: bpy.props.BoolProperty(
        name='Left Ankle',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object='left_ankle'),
    )  # type: ignore

    show_com_vertical_projection_options: bpy.props.BoolProperty(
        name='',
        default=False,
    )  # type: ignore

    com_vertical_projection_neutral_color: bpy.props.FloatVectorProperty(
        name='',
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0)
    )  # type: ignore

    com_vertical_projection_in_bos_color: bpy.props.FloatVectorProperty(
        name='',
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 1.0, 0.0, 1.0)
    )  # type: ignore

    com_vertical_projection_out_bos_color: bpy.props.FloatVectorProperty(
        name='',
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.0, 0.0, 1.0)
    )  # type: ignore

    show_joint_angles_options: bpy.props.BoolProperty(
        name='',
        default=False,
    )  # type: ignore

    joint_angles_color: bpy.props.FloatVectorProperty(
        name='',
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.694, 0.082, 0.095, 1.0)
    )  # type: ignore

    joint_angles_text_color: bpy.props.FloatVectorProperty(
        name='',
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.365, 0.048, 1.0)
    )  # type: ignore

    show_base_of_support_options: bpy.props.BoolProperty(
        name='',
        default=False,
    )  # type: ignore

    base_of_support_z_threshold: bpy.props.FloatProperty(
        name='',
        default=0.1
    )  # type: ignore

    base_of_support_point_radius: bpy.props.FloatProperty(
        name='',
        min=1.0,
        default=7.0
    )  # type: ignore

    base_of_support_color: bpy.props.FloatVectorProperty(
        name='',
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.007, 0.267, 1.0, 1.0)
    )  # type: ignore

