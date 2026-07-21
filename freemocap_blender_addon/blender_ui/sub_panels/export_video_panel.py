import bpy


class VIEW3D_PT_export_video_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Export Video"
    bl_parent_id = "VIEW3D_PT_freemocap_main_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        ui_props = context.scene.freemocap_ui_properties
        export_video_props = ui_props.export_video_properties

        # Create a row with one column blank for indentation
        row = self.layout.row()
        row.label(text="", icon='BLANK1')

        layout = row.column(align=True)

        row = layout.row(align=True)
        split = row.column().row().split(factor=0.6)
        split.column().label(text='Video Profile')
        split.column().prop(export_video_props, 'export_profile')

        # Custom Profile Options
        row = layout.row(align=True)
        row.prop(export_video_props, "show_custom_profile_options", text="",
                 icon='TRIA_DOWN' if export_video_props.show_custom_profile_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Custom Profile Options")

        # box = layout.box()
        if export_video_props.show_custom_profile_options:
            box2 = layout.box()

            split = box2.column().row().split(factor=0.25)
            split.column().label(text='Width (px):')
            split.column().prop(export_video_props, 'custom_profile_width')
            split.column().label(text='Height (px):')
            split.column().prop(export_video_props, 'custom_profile_height')

            box2.label(text='Cameras Angles:')
            box3 = box2.box()

            row = box3.row(align=True)
            row.prop(export_video_props, 'custom_use_front_camera')
            if export_video_props.custom_use_front_camera:
                row = box3.row().split(factor=0.25)
                row.label(text='Width (px):')
                row.prop(export_video_props, 'custom_front_camera_width')
                row.label(text='Height (px):')
                row.prop(export_video_props, 'custom_front_camera_height')
                row = box3.row().split(factor=0.25)
                row.label(text='Position X:')
                row.prop(export_video_props, 'custom_front_camera_position_x')
                row.label(text='Position Y:')
                row.prop(export_video_props, 'custom_front_camera_position_y')

            row = box3.row(align=True)
            row.prop(export_video_props, 'custom_use_left_camera')
            if export_video_props.custom_use_left_camera:
                row = box3.row().split(factor=0.25)
                row.label(text='Width (px):')
                row.prop(export_video_props, 'custom_left_camera_width')
                row.label(text='Height (px):')
                row.prop(export_video_props, 'custom_left_camera_height')
                row = box3.row().split(factor=0.25)
                row.label(text='Position X:')
                row.prop(export_video_props, 'custom_left_camera_position_x')
                row.label(text='Position Y:')
                row.prop(export_video_props, 'custom_left_camera_position_y')

            row = box3.row(align=True)
            row.prop(export_video_props, 'custom_use_right_camera')
            if export_video_props.custom_use_right_camera:
                row = box3.row().split(factor=0.25)
                row.label(text='Width (px):')
                row.prop(export_video_props, 'custom_right_camera_width')
                row.label(text='Height (px):')
                row.prop(export_video_props, 'custom_right_camera_height')
                row = box3.row().split(factor=0.25)
                row.label(text='Position X:')
                row.prop(export_video_props, 'custom_right_camera_position_x')
                row.label(text='Position Y:')
                row.prop(export_video_props, 'custom_right_camera_position_y')

            row = box3.row(align=True)
            row.prop(export_video_props, 'custom_use_top_camera')
            if export_video_props.custom_use_top_camera:
                row = box3.row().split(factor=0.25)
                row.label(text='Width (px):')
                row.prop(export_video_props, 'custom_top_camera_width')
                row.label(text='Height (px):')
                row.prop(export_video_props, 'custom_top_camera_height')
                row = box3.row().split(factor=0.25)
                row.label(text='Position X:')
                row.prop(export_video_props, 'custom_top_camera_position_x')
                row.label(text='Position Y:')
                row.prop(export_video_props, 'custom_top_camera_position_y')

            box2.label(text='Overlays:')
            box4 = box2.box()
            row = box4.row(align=True)
            row.prop(export_video_props, 'custom_overlays_add_freemocap_logo')

            if export_video_props.custom_overlays_add_freemocap_logo:
                row = box4.row().split(factor=0.25)
                row.label(text='Scale X:')
                row.prop(export_video_props, 'custom_overlays_freemocap_logo_scale_x')
                row.label(text='Scale Y:')
                row.prop(export_video_props, 'custom_overlays_freemocap_logo_scale_y')
                row = box4.row().split(factor=0.25)
                row.label(text='Position X:')
                row.prop(export_video_props, 'custom_overlays_freemocap_logo_position_x')
                row.label(text='Position Y:')
                row.prop(export_video_props, 'custom_overlays_freemocap_logo_position_y')


        layout.operator('freemocap._export_video', text='Export Video')
