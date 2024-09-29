import bpy

class VIEW3D_PT_load_data(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Load FreeMoCap Data"
    bl_parent_id = "view3d.pt_freemocap_main_panel"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Load FreeMoCap Data")
        # Clear scene button
        clear_scene_box = layout.box()
        clear_scene_box.operator('freemocap._clear_scene', text='Clear Scene')

        # Run all panel
        box = layout.box()
        row = box.row()
        row.label(text="FreeMoCap Recording:")
        row.prop(context.scene.freemocap_properties, "recording_path", text="")
        box.operator('freemocap._load_data', text='Load Data')

        # Save data to disk panel
        box = layout.box()
        box.prop(context.scene.freemocap_properties, "data_parent_empty", text="Data Parent Empty")