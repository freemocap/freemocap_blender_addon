import bpy


class VIEW3D_PT_export_video_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Export Video"
    bl_parent_id = "view3d.pt_freemocap_main_panel"

    def draw(self, context):
        layout = self.layout
        ui_props = context.scene.freemocap_ui_properties
        export_video_props = ui_props.export_video_properties

        box = layout.box()
        split = box.column().row().split(factor=0.6)
        split.column().label(text='Video Profile')
        split.column().prop(export_video_props, 'export_profile')

        box.operator('freemocap._export_video', text='Export Video')
