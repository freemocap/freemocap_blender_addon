import bpy


class VIEW3D_PT_animation_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "Animation"
    bl_parent_id = "VIEW3D_PT_freemocap_main_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        ui_props = context.scene.freemocap_ui_properties
        retarget_animation_props = ui_props.retarget_animation_properties
        set_bone_rotation_limits_props = ui_props.set_bone_rotation_limits_properties
        limit_markers_range_of_motion_props = ui_props.limit_markers_range_of_motion_properties
        foot_locking_props = ui_props.foot_locking_properties

        # Create a row with one column blank for indentation
        row = self.layout.row()
        row.label(text="", icon='BLANK1')

        layout = row.column(align=True)

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
                    "ANIMATION_UL_RetargetPairs",
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

            split = box.column().row().split(factor=0.7)
            split.column().label(text='Limit Palm Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_palm_markers')

            split = box.column().row().split(factor=0.7)
            split.column().label(text='Limit Proximal Phalanx Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_proximal_phalanx_markers')

            split = box.column().row().split(factor=0.7)
            split.column().label(text='Limit Intermediate Phalanx Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_intermediate_phalanx_markers')

            split = box.column().row().split(factor=0.7)
            split.column().label(text='Limit Distal Phalanx Markers')
            split.column().prop(limit_markers_range_of_motion_props, 'limit_distal_phalanx_markers')

            split = box.column().row().split(factor=0.7)
            split.column().label(text='Range of Motion Scale')
            split.column().prop(limit_markers_range_of_motion_props, 'range_of_motion_scale')

            split = box.column().row().split(factor=0.7)
            split.column().label(text='Hand Locked Track Marker')
            split.column().prop(limit_markers_range_of_motion_props, 'hand_locked_track_marker')

            split = box.column().row().split(factor=0.7)
            split.column().label(text='Hand Damped Track Marker')
            split.column().prop(limit_markers_range_of_motion_props, 'hand_damped_track_marker')

            # TODO: Add fields to adjust the min max axis limit values
            # Not sure what to use, degrees amount, a percentage of the min-max range?
            # The obvious choice would be to put the min and max limits on the UI
            # but that would be too many inputs if each phalange has its own limit entry

            box.operator(
                'freemocap._limit_markers_range_of_motion',
                text='Limit Markers Range of Motion',
            )

        # Foot Locking
        row = layout.row(align=True)
        row.prop(foot_locking_props, "show_foot_locking_options", text="",
                 icon='TRIA_DOWN' if foot_locking_props.show_foot_locking_options else 'TRIA_RIGHT', emboss=False)
        row.label(text="Foot Locking")

        if foot_locking_props.show_foot_locking_options:
            row = layout.row(align=True)
            split = row.split(factor=0.5)
            split.column().label(text='Foot Locking Method')
            split.column().prop(foot_locking_props, 'foot_locking_method')

            row = layout.row(align=True)
            row.prop(foot_locking_props, "show_individual_marker_height_options", text="",
                icon='TRIA_DOWN' if foot_locking_props.show_individual_marker_height_options else 'TRIA_RIGHT', emboss=False)
            row.label(text="Individual Marker Height Options")

            if foot_locking_props.show_individual_marker_height_options:

                box = layout.box()

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Target Foot')
                split.split().column().prop(
                    foot_locking_props,
                    'target_foot'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Target foot base markers')
                split.split().column().prop(
                    foot_locking_props,
                    'target_base_markers'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Z Threshold (m)')
                split.split().column().prop(
                    foot_locking_props,
                    'z_threshold'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Ground Level (m)')
                split.split().column().prop(
                    foot_locking_props,
                    'ground_level'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Frame Window Minimum Size')
                split.split().column().prop(
                    foot_locking_props,
                    'frame_window_min_size'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Initial Attenuation Count')
                split.split().column().prop(
                    foot_locking_props,
                    'initial_attenuation_count'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Final Attenuation Count')
                split.split().column().prop(
                    foot_locking_props,
                    'final_attenuation_count'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Lock XY at Ground Level')
                split.split().column().prop(
                    foot_locking_props,
                    'lock_xy_at_ground_level'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Knee Hip Compensation Coefficient')
                split.split().column().prop(
                    foot_locking_props,
                    'knee_hip_compensation_coefficient'
                )

                split = box.column().row().split(factor=0.6)
                split.column().label(text='Compensate Upper Body Markers')
                split.split().column().prop(
                    foot_locking_props,
                    'compensate_upper_body'
                )

            row = layout.row(align=True)
            row.operator(
                'freemocap._foot_locking',
                text='Apply Foot Locking',
            )
                    



