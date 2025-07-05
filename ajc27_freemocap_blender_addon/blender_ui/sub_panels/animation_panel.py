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
        retarget_animation_props = ui_props.retarget_animation_properties
        set_bone_rotation_limits_props = ui_props.set_bone_rotation_limits_properties
        limit_markers_range_of_motion_props = ui_props.limit_markers_range_of_motion_properties

        # Retarget
        row = layout.row(align=True)
        row.prop(retarget_animation_props, "show_retarget_animation_options", text="",
                 icon='TRIA_DOWN' if retarget_animation_props.show_retarget_animation_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Retarget")

        if retarget_animation_props.show_retarget_animation_options:
            box = layout.box()
            split = box.column().row().split(factor=0.5)
            split.column().label(text='Source Armature')
            split.column().prop(retarget_animation_props, 'retarget_source_armature')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Target Armature')
            split.column().prop(retarget_animation_props, 'retarget_target_armature')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Source Root Bone')
            split.column().prop(retarget_animation_props, 'retarget_source_root_bone')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Target Root Bone')
            split.column().prop(retarget_animation_props, 'retarget_target_root_bone')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Source Axes Convention')
            split_2 = split.column().split(factor=0.333)
            split_2.column().prop(retarget_animation_props, 'retarget_source_x_axis_convention')
            split_2.column().prop(retarget_animation_props, 'retarget_source_y_axis_convention')
            split_2.column().prop(retarget_animation_props, 'retarget_source_z_axis_convention')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Target Axes Convention')
            split_2 = split.column().split(factor=0.333)
            split_2.column().prop(retarget_animation_props, 'retarget_target_x_axis_convention')
            split_2.column().prop(retarget_animation_props, 'retarget_target_y_axis_convention')
            split_2.column().prop(retarget_animation_props, 'retarget_target_z_axis_convention')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Target Bone Rotation Mixmode')
            split.column().prop(retarget_animation_props, 'retarget_target_bone_rotation_mixmode')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Target Bone Rotation Target Space')
            split.column().prop(retarget_animation_props, 'retarget_target_bone_rotation_target_space')

            split = box.column().row().split(factor=0.5)
            split.column().label(text='Target Bone Rotation Owner Space')
            split.column().prop(retarget_animation_props, 'retarget_target_bone_rotation_owner_space')            

            box.operator(
                'freemocap._detect_bone_mapping',
                text='Detect Bone Mapping',
            )

            # Add the source bones list if any
            if retarget_animation_props.retarget_pairs:

                box.template_list(
                    "UL_RetargetPairs",
                    "",
                    retarget_animation_props,
                    "retarget_pairs",
                    retarget_animation_props,
                    "active_pair_index",
                    rows=10
                )

            # Add the retarget animation button
            if retarget_animation_props.retarget_pairs:
                box.operator(
                    'freemocap._retarget_animation',
                    text='Retarget Animation',
                )

        # Set Bone Rotation Limits
        # row = layout.row(align=True)
        # row.prop(set_bone_rotation_limits_props, "show_set_bone_rotation_limits_options", text="",
        #          icon='TRIA_DOWN' if set_bone_rotation_limits_props.show_set_bone_rotation_limits_options else 'TRIA_RIGHT', emboss=False)
        # row.label(text="Set Bone Rotation Limits")

        # if set_bone_rotation_limits_props.show_set_bone_rotation_limits_options:
        #     box = layout.box()
        #     box.operator(
        #         'freemocap._set_bone_rotation_limits',
        #         text='Set Bone Rotation Limits',
        #     )

        # Limit Markers Range of Motion
        row = layout.row(align=True)
        row.prop(limit_markers_range_of_motion_props, "show_limit_markers_range_of_motion_options", text="",
                 icon='TRIA_DOWN' if limit_markers_range_of_motion_props.show_limit_markers_range_of_motion_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Limit Markers Range of Motion")
        
        if limit_markers_range_of_motion_props.show_limit_markers_range_of_motion_options:
            box = layout.box()

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Limit Palm Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_palm_markers')

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Limit Proximal Phalanx Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_proximal_phalanx_markers')

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Limit Intermediate Phalanx Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_intermediate_phalanx_markers')

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Limit Distal Phalanx Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_distal_phalanx_markers')

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Range of Motion Scale')
            split.column().prop(limit_markers_range_of_motion_props, 'range_of_motion_scale')

            split = box.column().row().split(factor=0.8)
            split.column().label(text='Hand Locked Track Marker')
            split.column().prop(limit_markers_range_of_motion_props, 'hand_locked_track_marker')

            # TODO: Add fields to adjust the min max axis limit values
            # Not sure what to use, degrees amount, a percentage of the min-max range?
            # The obvious choice would be to put the min and max limits on the UI
            # but that would be too many inputs if each phalange has its own limit entry

            box.operator(
                'freemocap._limit_markers_range_of_motion',
                text='Limit Markers Range of Motion',
            )
                



