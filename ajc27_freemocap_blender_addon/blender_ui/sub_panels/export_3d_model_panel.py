import bpy

class VIEW3D_PT_export_3d_model_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Export 3D Model"
    bl_parent_id = "view3d.pt_freemocap_main_panel"

    def draw(self, context):
        layout = self.layout
        ui_props = context.scene.freemocap_ui_properties
        export_3d_model_props = ui_props.export_3d_model_properties

        row = layout.row(align=True)
        split = row.column().row().split(factor=0.6)
        split.column().label(text='Model Destination Path')
        split.column().prop(export_3d_model_props, 'model_destination_path')



        # FBX Options
        row = layout.row(align=True)
        row.prop(export_3d_model_props, "show_export_fbx_format_options", text="",
                 icon='TRIA_DOWN' if export_3d_model_props.show_export_fbx_format_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="FBX Options")

        if export_3d_model_props.show_export_fbx_format_options:
            box = layout.box()

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Add Leaf Bones')
            split.column().prop(export_3d_model_props, 'fbx_add_leaf_bones')

        layout.operator(
            'freemocap._export_3d_model',
            text='Export 3D Model',
        )