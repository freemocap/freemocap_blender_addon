import bpy


class VIEW3D_PT_export_video_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Export Video"
    bl_parent_id = "view3d.pt_freemocap_main_panel"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        # split = box.column().row().split(factor=0.6)
        # split.column().label(text='Video Profile')
        # split.split().column().prop(context.scene.freemocap_properties, 'video_export_profile')

        # box.label(text='Scientific Profile Options')
        # split = box.column().row().split(factor=0.6)
        # split.column().label(text='Ground Contact Threshold (m)')
        # split.split().column().prop(context.scene.freemocap_properties, 'ground_contact_threshold')

        box.operator('freemocap._export_video', text='Export Video')
