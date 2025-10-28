import bpy


class VIEW3D_PT_export_3d_model_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Export 3D Model"
    bl_parent_id = "VIEW3D_PT_freemocap_main_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        ui_props = context.scene.freemocap_ui_properties
        export_3d_model_props = ui_props.export_3d_model_properties

        # Create a row with one column blank for indentation
        row = self.layout.row()
        row.label(text="", icon='BLANK1')

        layout = row.column(align=True)

        row = layout.row(align=True)
        split = row.column().row().split(factor=0.6)
        split.column().label(text='Model Destination Folder')
        split.column().prop(export_3d_model_props, 'model_destination_folder')

        row = layout.row(align=True)
        split = row.column().row().split(factor=0.6)
        split.column().label(text='Model Format')
        split.column().prop(export_3d_model_props, 'model_format')

        row = layout.row(align=True)
        split = row.column().row().split(factor=0.6)
        split.column().label(text='Bones Naming Convention')
        split.column().prop(export_3d_model_props, 'bones_naming_convention')

        row = layout.row(align=True)
        split = row.column().row().split(factor=0.6)
        split.column().label(text='Rest Pose Type')
        split.column().prop(export_3d_model_props, 'rest_pose_type')

        row = layout.row(align=True)
        split = row.column().row().split(factor=0.6)
        split.column().label(text='Restore Defaults After Export')
        split.column().prop(export_3d_model_props, 'restore_defaults_after_export')

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

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Primary Bone Axis')
            split.column().prop(export_3d_model_props, 'fbx_primary_bone_axis')

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Secondary Bone Axis')
            split.column().prop(export_3d_model_props, 'fbx_secondary_bone_axis')

        layout.operator(
            'freemocap._export_3d_model',
            text='Export 3D Model',
        )