import re

import bpy
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.visualizer_panel import ViewPanelPropNames

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
                                                      panel_property=ViewPanelPropNames.SHOW_ARMATURE.value,
                                                      parent_pattern=r'_rig\Z|root\Z',
                                                      toggle_children_not_parent=False),
    )  # type: ignore

    show_skelly_mesh: bpy.props.BoolProperty(
        name='Skelly Mesh',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_SKELLY_MESH.value,
                                                      parent_pattern=r'skelly_mesh',
                                                      toggle_children_not_parent=False),
    )  # type: ignore

    show_tracked_points: bpy.props.BoolProperty(
        name='Tracked Points',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_TRACKED_POINTS.value,
                                                      parent_pattern=r'empties_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_rigid_bodies: bpy.props.BoolProperty(
        name='Rigid Bodies',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_RIGID_BODIES.value,
                                                      parent_pattern=r'rigid_body_meshes_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_center_of_mass: bpy.props.BoolProperty(
        name='Center of Mass',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_CENTER_OF_MASS.value,
                                                      parent_pattern=r'center_of_mass_data_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_videos: bpy.props.BoolProperty(
        name='Capture Videos',
        default=True,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_VIDEOS.value,
                                                      parent_pattern=r'videos_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_com_vertical_projection: bpy.props.BoolProperty(
        name='COM Vertical Projection',
        default=False,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_COM_VERTICAL_PROJECTION.value,
                                                      parent_pattern=r'COM_Vertical_Projection',
                                                      toggle_children_not_parent=False),
    )  # type: ignore

    show_joint_angles: bpy.props.BoolProperty(
        name='Joint Angles',
        default=False,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_JOINT_ANGLES.value,
                                                      parent_pattern=r'joint_angles_parent',
                                                      toggle_children_not_parent=True),
    )  # type: ignore

    show_base_of_support: bpy.props.BoolProperty(
        name='Base of Support',
        default=False,
        update=lambda a, b: toggle_element_visibility(a,
                                                      b,
                                                      panel_property=ViewPanelPropNames.SHOW_BASE_OF_SUPPORT.value,
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
        default=2,
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
                                               data_object_basename='center_of_mass'),
    )  # type: ignore

    motion_path_head_center: bpy.props.BoolProperty(
        name='Head Center',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='head_center'),
    )  # type: ignore

    motion_path_neck_center: bpy.props.BoolProperty(
        name='Neck Center',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='neck_center'),
    )  # type: ignore

    motion_path_hips_center: bpy.props.BoolProperty(
        name='Hips Center',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='hips_center'),
    )  # type: ignore

    motion_path_right_shoulder: bpy.props.BoolProperty(
        name='Right Shoulder',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='right_shoulder'),
    )  # type: ignore

    motion_path_left_shoulder: bpy.props.BoolProperty(
        name='Left Shoulder',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='left_shoulder'),
    )  # type: ignore

    motion_path_right_elbow: bpy.props.BoolProperty(
        name='Right Elbow',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='right_elbow'),
    )  # type: ignore

    motion_path_left_elbow: bpy.props.BoolProperty(
        name='Left Elbow',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='left_elbow'),
    )  # type: ignore

    motion_path_right_wrist: bpy.props.BoolProperty(
        name='Right Wrist',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='right_wrist'),
    )  # type: ignore

    motion_path_left_wrist: bpy.props.BoolProperty(
        name='Left Wrist',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='left_wrist'),
    )  # type: ignore

    motion_path_right_hip: bpy.props.BoolProperty(
        name='Right Hip',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='right_hip'),
    )  # type: ignore

    motion_path_left_hip: bpy.props.BoolProperty(
        name='Left Hip',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='left_hip'),
    )  # type: ignore

    motion_path_right_knee: bpy.props.BoolProperty(
        name='Right Knee',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='right_knee'),
    )  # type: ignore

    motion_path_left_knee: bpy.props.BoolProperty(
        name='Left Knee',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='left_knee'),
    )  # type: ignore

    motion_path_right_ankle: bpy.props.BoolProperty(
        name='Right Ankle',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='right_ankle'),
    )  # type: ignore

    motion_path_left_ankle: bpy.props.BoolProperty(
        name='Left Ankle',
        default=False,
        update=lambda a, b: update_motion_path(a,
                                               b,
                                               data_object_basename='left_ankle'),
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
        default=(1.0, 1.0, 0.0, 1.0)
    )  # type: ignore

    com_vertical_projection_in_bos_color: bpy.props.FloatVectorProperty(
        name='',
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, .125, 1.0, 1.0)
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
        default=(1.0, 1.0, 1.0, 0.5)
    )  # type: ignore

def update_motion_path(self, context, data_object_basename: str):
    toggle_motion_path(
        self,
        context,
        panel_property='motion_path_' + data_object_basename,
        data_object_basename=data_object_basename,
        show_line=self.motion_path_show_line,
        line_thickness=self.motion_path_line_thickness,
        use_custom_color=self.motion_path_use_custom_color,
        line_color=self.motion_path_line_color,
        frames_before=self.motion_path_frames_before,
        frames_after=self.motion_path_frames_after,
        frame_step=self.motion_path_frame_step,
        show_frame_numbers=self.motion_path_show_frame_numbers,
        show_keyframes=self.motion_path_show_keyframes,
        show_keyframe_number=self.motion_path_show_keyframe_number
    )

def toggle_element_visibility(self,
                              context,
                              panel_property: str,
                              parent_pattern: str,
                              toggle_children_not_parent: bool,)->None:

    for data_object in context.scene.freemocap_properties.data_parent_empty.children_recursive:
        if re.search(parent_pattern, data_object.name):
            hide_objects(data_object,
                         not bool(self[panel_property]),
                         toggle_children_not_parent)

# Function to toggle the visibility of the motion paths
def toggle_motion_path(self,
                       context,
                       panel_property: str,
                       data_object_basename: str,
                       show_line: bool = True,
                       line_thickness: int = 6,
                       use_custom_color: bool = False,
                       line_color: tuple = (0.5, 1.0, 0.8),
                       frames_before: int = 10,
                       frames_after: int = 10,
                       frame_step: int = 1,
                       show_frame_numbers: bool = False,
                       show_keyframes: bool = False,
                       show_keyframe_number: bool = False)->None:

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get reference to the object
    data_object_name = None
    for child in context.scene.freemocap_properties.data_parent_empty.children_recursive:
        if re.search(data_object_basename, child.name):
            data_object_name = child.name
            break
    if not data_object_name:
        raise ValueError(f'Object with name {data_object_basename} not found in children of `data_parent_empty`: {context.scene.freemocap_properties.data_parent_empty}')

    obj = bpy.data.objects[data_object_basename]

    # Select the object
    obj.select_set(True)

    # Set the object as active object
    bpy.context.view_layer.objects.active = obj

    if bool(self[panel_property]):
        # Calculate paths
        bpy.ops.object.paths_calculate(display_type='CURRENT_FRAME', range='SCENE')
        # Set motion path properties for the specific object
        if obj.motion_path:
            obj.motion_path.lines = show_line
            obj.motion_path.line_thickness = line_thickness
            obj.motion_path.use_custom_color = use_custom_color
            obj.motion_path.color = line_color
            obj.animation_visualization.motion_path.frame_before = frames_before
            obj.animation_visualization.motion_path.frame_after = frames_after
            obj.animation_visualization.motion_path.frame_step = frame_step
            obj.animation_visualization.motion_path.show_frame_numbers = show_frame_numbers
            obj.animation_visualization.motion_path.show_keyframe_highlight = show_keyframes
            obj.animation_visualization.motion_path.show_keyframe_numbers = show_keyframe_number
    else:
        bpy.ops.object.paths_clear(only_selected=True)

# Function to hide (or unhide) Blender objects
def hide_objects(data_object: bpy.types.Object,
                 hide: bool = True,
                 hide_children_not_parent: bool = False, ) -> None:
    if hide_children_not_parent:
        for child_object in data_object.children:
            # Hide child object
            child_object.hide_set(hide)
            # Execute the function recursively
            hide_objects(child_object, hide, hide_children_not_parent)
    else:
        data_object.hide_set(hide)