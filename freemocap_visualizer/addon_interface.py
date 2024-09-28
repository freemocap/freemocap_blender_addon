import bpy
from bpy.types import Operator, Panel

from .functions import (
    toggle_element_visibility,
    add_com_vertical_projection,
    add_joint_angles,
    add_base_of_support,
    toggle_motion_path
)

def update_motion_path(self, context, data_object: str):
    toggle_motion_path(
        self,
        context,
        panel_property='motion_path_' + data_object,
        data_object=data_object,
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

# Class with the different properties of the interface
class FMC_VISUALIZER_PROPERTIES(bpy.types.PropertyGroup):

    show_base_elements_options: bpy.props.BoolProperty(
        name = '',
        default = False,
    ) # type: ignore

    show_armature: bpy.props.BoolProperty(
        name = 'Armature',
        description = 'Show Armature',
        default = True,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_armature',
                                                       parent_pattern=r'_rig\Z|root\Z',
                                                       toggle_children_not_parent=False),
    ) # type: ignore

    show_body_mesh: bpy.props.BoolProperty(
        name = 'Body Mesh',
        default = True,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_body_mesh',
                                                       parent_pattern=r'skelly_mesh',
                                                       toggle_children_not_parent=False),
    ) # type: ignore

    show_markers: bpy.props.BoolProperty(
        name = 'Markers',
        default = True,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_markers',
                                                       parent_pattern=r'empties_parent',
                                                       toggle_children_not_parent=True),
    ) # type: ignore

    show_rigid_body: bpy.props.BoolProperty(
        name = 'Rigid Body',
        default = True,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_rigid_body',
                                                       parent_pattern=r'rigid_body_meshes_parent',
                                                       toggle_children_not_parent=True),
    ) # type: ignore

    show_center_of_mass: bpy.props.BoolProperty(
        name = 'Center of Mass',
        default = True,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_center_of_mass',
                                                       parent_pattern=r'center_of_mass_data_parent',
                                                       toggle_children_not_parent=True),
    ) # type: ignore

    show_videos: bpy.props.BoolProperty(
        name = 'Capture Videos',
        default = True,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_videos',
                                                       parent_pattern=r'videos_parent',
                                                       toggle_children_not_parent=True),
    ) # type: ignore

    show_com_vertical_projection: bpy.props.BoolProperty(
        name = 'COM Vertical Projection',
        default = False,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_com_vertical_projection',
                                                       parent_pattern=r'COM_Vertical_Projection',
                                                       toggle_children_not_parent=False),
    ) # type: ignore

    show_joint_angles: bpy.props.BoolProperty(
        name = 'Joint Angles',
        default = False,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_joint_angles',
                                                       parent_pattern=r'joint_angles_parent',
                                                       toggle_children_not_parent=True),
    ) # type: ignore

    show_base_of_support: bpy.props.BoolProperty(
        name = 'Base of Support',
        default = False,
        update = lambda a,b: toggle_element_visibility(a,
                                                       b,
                                                       panel_property='show_base_of_support',
                                                       parent_pattern=r'base_of_support',
                                                       toggle_children_not_parent=False),
    ) # type: ignore

    show_motion_paths_options: bpy.props.BoolProperty(
        name = '',
        default = False,
    ) # type: ignore

    motion_path_show_line: bpy.props.BoolProperty(
        name = 'Show Line',
        default = True,
    ) # type: ignore

    motion_path_line_thickness: bpy.props.IntProperty(
        name = '',
        min = 1,
        max = 6,
        default = 6,
    ) # type: ignore

    motion_path_use_custom_color: bpy.props.BoolProperty(
        name = 'Use Custom Color',
        default = False,
    ) # type: ignore

    motion_path_line_color: bpy.props.FloatVectorProperty(
        name = '',
        subtype = 'COLOR',
        min = 0.0,
        max = 1.0,
        default = (1.0, 1.0, 1.0),
    ) # type: ignore

    motion_path_frames_before: bpy.props.IntProperty(
        name = '',
        min = 1,
        default = 10,
    ) # type: ignore

    motion_path_frames_after: bpy.props.IntProperty(
        name = '',
        min = 1,
        default = 10,
    ) # type: ignore

    motion_path_frame_step: bpy.props.IntProperty(
        name = '',
        min = 1,
        default = 1,
    ) # type: ignore

    motion_path_show_frame_numbers: bpy.props.BoolProperty(
        name = 'Show Frame Numbers',
        default = False,
    ) # type: ignore

    motion_path_show_keyframes: bpy.props.BoolProperty(
        name = 'Show Keyframes',
        default = False,
    ) # type: ignore

    motion_path_show_keyframe_number: bpy.props.BoolProperty(
        name = 'Show Keyframe Number',
        default = False,
    ) # type: ignore

    motion_path_center_of_mass: bpy.props.BoolProperty(
        name = 'Center of Mass',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='center_of_mass'),
    ) # type: ignore

    motion_path_head_center: bpy.props.BoolProperty(
        name = 'Head Center',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='head_center'),
    ) # type: ignore

    motion_path_neck_center: bpy.props.BoolProperty(
        name = 'Neck Center',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='neck_center'),
    ) # type: ignore

    motion_path_hips_center: bpy.props.BoolProperty(
        name = 'Hips Center',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='hips_center'),
    ) # type: ignore
        
    motion_path_right_shoulder: bpy.props.BoolProperty(
        name = 'Right Shoulder',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='right_shoulder'),
    ) # type: ignore

    motion_path_left_shoulder: bpy.props.BoolProperty(
        name = 'Left Shoulder',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='left_shoulder'),
    ) # type: ignore

    motion_path_right_elbow: bpy.props.BoolProperty(
        name = 'Right Elbow',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='right_elbow'),
    ) # type: ignore
        
    motion_path_left_elbow: bpy.props.BoolProperty(
        name = 'Left Elbow',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='left_elbow'),
    ) # type: ignore

    motion_path_right_wrist: bpy.props.BoolProperty(
        name = 'Right Wrist',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='right_wrist'),
    ) # type: ignore

    motion_path_left_wrist: bpy.props.BoolProperty(
        name = 'Left Wrist',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='left_wrist'),
    ) # type: ignore

    motion_path_right_hip: bpy.props.BoolProperty(
        name = 'Right Hip',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='right_hip'),
    ) # type: ignore

    motion_path_left_hip: bpy.props.BoolProperty(
        name = 'Left Hip',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='left_hip'),
    ) # type: ignore

    motion_path_right_knee: bpy.props.BoolProperty(
        name = 'Right Knee',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='right_knee'),
    ) # type: ignore

    motion_path_left_knee: bpy.props.BoolProperty(
        name = 'Left Knee',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='left_knee'),
    ) # type: ignore
    
    motion_path_right_ankle: bpy.props.BoolProperty(
        name = 'Right Ankle',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='right_ankle'),
    ) # type: ignore

    motion_path_left_ankle: bpy.props.BoolProperty(
        name = 'Left Ankle',
        default = False,
        update = lambda a,b: update_motion_path(a,
                                                b,
                                                data_object='left_ankle'),
    ) # type: ignore

    show_com_vertical_projection_options: bpy.props.BoolProperty(
        name = '',
        default = False,
    ) # type: ignore

    com_vertical_projection_neutral_color: bpy.props.FloatVectorProperty(
        name = '',
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (1.0,1.0,1.0,1.0)
    ) # type: ignore

    com_vertical_projection_in_bos_color: bpy.props.FloatVectorProperty(
        name = '',
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (0.0,1.0,0.0,1.0)
    ) # type: ignore

    com_vertical_projection_out_bos_color: bpy.props.FloatVectorProperty(
        name = '',
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (1.0,0.0,0.0,1.0)
    ) # type: ignore

    show_joint_angles_options: bpy.props.BoolProperty(
        name = '',
        default = False,
    ) # type: ignore

    joint_angles_color: bpy.props.FloatVectorProperty(
        name = '',
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (0.694,0.082,0.095,1.0)
    ) # type: ignore

    joint_angles_text_color: bpy.props.FloatVectorProperty(
        name = '',
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (1.0,0.365,0.048,1.0)        
    ) # type: ignore

    show_base_of_support_options: bpy.props.BoolProperty(
        name = '',
        default = False,
    ) # type: ignore

    base_of_support_z_threshold: bpy.props.FloatProperty(
        name = '',
        default = 0.1
    ) # type: ignore

    base_of_support_point_radius: bpy.props.FloatProperty(
        name = '',
        min = 1.0,
        default = 7.0
    ) # type: ignore

    base_of_support_color: bpy.props.FloatVectorProperty(
        name = '',
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (0.007,0.267,1.0,1.0)
    ) # type: ignore

    
# UI Panel Class
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
        row.prop(fmc_visualizer_tool, "show_base_elements_options", text="", icon='TRIA_DOWN' if fmc_visualizer_tool.show_base_elements_options else 'TRIA_RIGHT', emboss=False)
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
        row.prop(fmc_visualizer_tool, "show_motion_paths_options", text="", icon='TRIA_DOWN' if fmc_visualizer_tool.show_motion_paths_options else 'TRIA_RIGHT', emboss=False)
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
        row.prop(fmc_visualizer_tool, "show_com_vertical_projection_options", text="", icon='TRIA_DOWN' if fmc_visualizer_tool.show_com_vertical_projection_options else 'TRIA_RIGHT', emboss=False)
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
        row.prop(fmc_visualizer_tool, "show_joint_angles_options", text="", icon='TRIA_DOWN' if fmc_visualizer_tool.show_joint_angles_options else 'TRIA_RIGHT', emboss=False)
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
        row.prop(fmc_visualizer_tool, "show_base_of_support_options", text="", icon='TRIA_DOWN' if fmc_visualizer_tool.show_base_of_support_options else 'TRIA_RIGHT', emboss=False)
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


# Operator classes that executes the methods
class FMC_VISUALIZER_ADD_COM_VERTICAL_PROJECTION(Operator):
    bl_idname = 'fmc_visualizer.add_com_vertical_projection'
    bl_label = 'Add COM Vertical Projection'
    bl_description = "Add COM Vertical Projection"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_visualizer_tool = scene.fmc_visualizer_tool

        print("Adding COM Vertical Projection.......")

        # Add COM Vertical Projection
        add_com_vertical_projection(neutral_color=fmc_visualizer_tool.com_vertical_projection_neutral_color,
                                    in_bos_color=fmc_visualizer_tool.com_vertical_projection_in_bos_color,
                                    out_bos_color=fmc_visualizer_tool.com_vertical_projection_out_bos_color)

        # Set the show COM Vertical Projection property to True
        fmc_visualizer_tool.show_com_vertical_projection = True

        return {'FINISHED'}
    
class FMC_VISUALIZER_ADD_JOINT_ANGLES(Operator):
    bl_idname = 'fmc_visualizer.add_joint_angles'
    bl_label = 'Add Joint Angles'
    bl_description = "Add Joint Angles"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_visualizer_tool = scene.fmc_visualizer_tool

        print("Adding Joint Angles.......")

        # Add Joint Angles
        add_joint_angles(angles_color=fmc_visualizer_tool.joint_angles_color,
                         text_color=fmc_visualizer_tool.joint_angles_text_color)

        # Set the show Joint Angles property to True
        fmc_visualizer_tool.show_joint_angles = True

        return {'FINISHED'}
    
class FMC_VISUALIZER_ADD_BASE_OF_SUPPORT(Operator):
    bl_idname = 'fmc_visualizer.add_base_of_support'
    bl_label = 'Add Base of Support'
    bl_description = "Add Base of Support"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_visualizer_tool = scene.fmc_visualizer_tool

        print("Adding Base of Support.......")

        # Check if the COM_Vertical_Projection object exists, if not create it
        if bpy.data.objects.get("COM_Vertical_Projection") is None:
            add_com_vertical_projection(neutral_color=fmc_visualizer_tool.com_vertical_projection_neutral_color,
                                        in_bos_color=fmc_visualizer_tool.com_vertical_projection_in_bos_color,
                                        out_bos_color=fmc_visualizer_tool.com_vertical_projection_out_bos_color)
            
            # Set the show COM Vertical Projection property to True
            fmc_visualizer_tool.show_com_vertical_projection = True

        # Add Base of Support
        add_base_of_support(z_threshold=fmc_visualizer_tool.base_of_support_z_threshold,
                            point_of_contact_radius=fmc_visualizer_tool.base_of_support_point_radius,
                            color=fmc_visualizer_tool.base_of_support_color)

        # Set the show Base of Support property to True
        fmc_visualizer_tool.show_base_of_support = True

        return {'FINISHED'}
