class VIEW3D_PT_freemocap_video_export(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Freemocap Video Export"
    bl_label = "Freemocap Video Export"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        fmc_video_export_tool = scene.fmc_video_export_tool

        box = layout.box()

        split = box.column().row().split(factor=0.6)
        split.column().label(text='Video Profile')
        split.split().column().prop(fmc_video_export_tool, 'export_profile')

        box.label(text='Scientific Profile Options')
        split = box.column().row().split(factor=0.6)
        split.column().label(text='Ground Contact Threshold (m)')
        split.split().column().prop(fmc_video_export_tool, 'ground_contact_threshold')

        box.operator('fmc_export_video.export_video', text='Export Video')
