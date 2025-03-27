import bpy

class VIEW3D_PT_animation_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Animation"
    bl_parent_id = "view3d.pt_freemocap_main_panel"

    def draw(self, context):
        layout = self.layout
        ui_props = context.scene.freemocap_ui_properties
        animation_props = ui_props.retarget_animation_properties

        # Retarget
        row = layout.row(align=True)
        row.prop(animation_props, "show_retarget_animation_options", text="",
                 icon='TRIA_DOWN' if animation_props.show_retarget_animation_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Retarget")

        if animation_props.show_retarget_animation_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text='Source Armature')
            split.column().prop(animation_props, 'retarget_source_armature')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Target Armature')
            split.column().prop(animation_props, 'retarget_target_armature')

            box.operator(
                'freemocap._detect_bone_mapping',
                text='Detect Bone Mapping',
            )

            # Add the source bones list if any
            if animation_props.retarget_pairs:

                box.template_list(
                    "UL_RetargetPairs",
                    "",
                    animation_props,
                    "retarget_pairs",
                    animation_props,
                    "active_pair_index",
                    rows=10
                )
                



