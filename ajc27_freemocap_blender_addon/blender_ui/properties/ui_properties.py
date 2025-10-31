import re

import bpy
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.visualizer_panel import ViewPanelPropNames
from ajc27_freemocap_blender_addon.blender_ui.sub_panels.visualizer_panel import ViewPanelPropNamesElements

from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.add_joint_angles_properties import (
    AddJointAnglesProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.retarget_animation_properties import (
    RetargetAnimationProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.set_bone_rotation_limits_properties import (
    SetBoneRotationLimitsProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.limit_markers_range_of_motion_properties import (
    LimitMarkersRangeOfMotionProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.export_3d_model_properties import (
    Export3DModelProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.export_video_properties import (
    ExportVideoProperties
)

from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.foot_locking_properties import (
    FootLockingProperties
)
from ajc27_freemocap_blender_addon.blender_ui.properties.subclasses.add_data_overlays_properties import (
    AddDataOverlaysProperties
)
# TODO: Group the rest of the properties as the Retarget Animation and Set Bone Rotation Limits Properties

class FREEMOCAP_UI_PROPERTIES(bpy.types.PropertyGroup):
    show_base_elements_options: bpy.props.BoolProperty(
        name='',
        default=False,
    )  # type: ignore

    show_armature: bpy.props.BoolProperty(
        name='Armature',
        description='Show Armature',
        default=True,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_ARMATURE.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_ARMATURE.object_name_pattern,
            toggle_children_not_parent=False
        ),
    )  # type: ignore

    show_skelly_mesh: bpy.props.BoolProperty(
        name='Skelly Mesh',
        default=True,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_SKELLY_MESH.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_SKELLY_MESH.object_name_pattern,
            toggle_children_not_parent=False
        ),
    )  # type: ignore

    show_tracked_points: bpy.props.BoolProperty(
        name='Tracked Points',
        default=True,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_TRACKED_POINTS.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_TRACKED_POINTS.object_name_pattern,
            toggle_children_not_parent=True
        ),
    )  # type: ignore

    show_rigid_bodies: bpy.props.BoolProperty(
        name='Rigid Bodies',
        default=True,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_RIGID_BODIES.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_RIGID_BODIES.object_name_pattern,
            toggle_children_not_parent=True
        ),
    )  # type: ignore

    show_center_of_mass: bpy.props.BoolProperty(
        name='Center of Mass',
        default=True,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_CENTER_OF_MASS.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_CENTER_OF_MASS.object_name_pattern,
            toggle_children_not_parent=True
        ),
    )  # type: ignore

    show_videos: bpy.props.BoolProperty(
        name='Capture Videos',
        default=True,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_VIDEOS.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_VIDEOS.object_name_pattern,
            toggle_children_not_parent=True
        ),
    )  # type: ignore

    show_com_vertical_projection: bpy.props.BoolProperty(
        name='COM Vertical Projection',
        default=False,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_COM_VERTICAL_PROJECTION.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_COM_VERTICAL_PROJECTION.object_name_pattern,
            toggle_children_not_parent=False
        ),
    )  # type: ignore

    show_joint_angles: bpy.props.BoolProperty(
        name='Joint Angles',
        default=False,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_JOINT_ANGLES.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_JOINT_ANGLES.object_name_pattern,
            toggle_children_not_parent=True
        ),
    )  # type: ignore

    show_base_of_support: bpy.props.BoolProperty(
        name='Base of Support',
        default=False,
        update=lambda a, b: toggle_element_visibility(
            a,
            b,
            panel_property=ViewPanelPropNamesElements.SHOW_BASE_OF_SUPPORT.property_name,
            parent_pattern=ViewPanelPropNamesElements.SHOW_BASE_OF_SUPPORT.object_name_pattern,
            toggle_children_not_parent=False
        ),
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

    motion_path_line_color_post: bpy.props.FloatVectorProperty(
        name='',
        subtype='COLOR',
        min=0.0,
        max=1.0,
        default=(0.5, 0.5, 0.5),
    )  # type: ignore

    motion_path_frames_before: bpy.props.IntProperty(
        name='',
        min=1,
        default=10,
    )  # type: ignore

    motion_path_frames_after: bpy.props.IntProperty(
        name='',
        min=1,
        default=1,
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

    motion_path_target_element: bpy.props.EnumProperty(
        name='',
        items=[
            ('center_of_mass_mesh', 'Center of Mass', ''),
            ('head_center', 'Head Center', ''),
            ('neck_center', 'Neck Center', ''),
            ('hips_center', 'Hips Center', ''),
            ('left_shoulder', 'Left Shoulder', ''),
            ('left_elbow', 'Left Elbow', ''),
            ('left_wrist', 'Left Wrist', ''),
            ('left_hip', 'Left Hip', ''),
            ('left_knee', 'Left Knee', ''),
            ('left_ankle', 'Left Ankle', ''),
            ('left_heel', 'Left Heel', ''),
            ('left_foot_index', 'Left Foot Index', ''),
            ('right_shoulder', 'Right Shoulder', ''),
            ('right_elbow', 'Right Elbow', ''),
            ('right_wrist', 'Right Wrist', ''),
            ('right_hip', 'Right Hip', ''),
            ('right_knee', 'Right Knee', ''),
            ('right_ankle', 'Right Ankle', ''),
            ('right_heel', 'Right Heel', ''),
            ('right_foot_index', 'Right Foot Index', ''),
        ],
        default='center_of_mass_mesh',
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

    add_joint_angles_properties: bpy.props.PointerProperty(
        type=AddJointAnglesProperties
    ) # type: ignore

    # Animation
    retarget_animation_properties: bpy.props.PointerProperty(
        type=RetargetAnimationProperties
    ) # type: ignore
    set_bone_rotation_limits_properties: bpy.props.PointerProperty(
        type=SetBoneRotationLimitsProperties
    ) # type: ignore
    limit_markers_range_of_motion_properties: bpy.props.PointerProperty(
        type=LimitMarkersRangeOfMotionProperties
    ) # type: ignore
    foot_locking_properties: bpy.props.PointerProperty(
        type=FootLockingProperties
    ) # type: ignore

    # Export 3D Model
    export_3d_model_properties: bpy.props.PointerProperty(
        type=Export3DModelProperties
    ) # type: ignore

    # Export Video
    export_video_properties: bpy.props.PointerProperty(
        type=ExportVideoProperties
    ) # type: ignore
    foot_locking_properties: bpy.props.PointerProperty(
        type=FootLockingProperties
    ) # type: ignore

    # Data Overlays
    add_data_overlays_properties: bpy.props.PointerProperty(
        type=AddDataOverlaysProperties
    ) # type: ignore


def toggle_element_visibility(self,
                              context,
                              panel_property: str,
                              parent_pattern: str,
                              toggle_children_not_parent: bool,)->None:

    data_parent_object = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]
    for data_object in data_parent_object.children_recursive:
        if re.search(parent_pattern, data_object.name):
            hide_objects(data_object,
                         not bool(self[panel_property]),
                         toggle_children_not_parent)


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
