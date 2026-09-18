import bpy

from freemocap_blender_addon.blender_ui.operators.animation.limit_markers_range_of_motion.limit_markers_range_of_motion import (
    limit_markers_range_of_motion,
)


class FREEMOCAP_OT_limit_markers_range_of_motion(bpy.types.Operator):
    bl_idname = 'freemocap._limit_markers_range_of_motion'
    bl_label = 'Limit Markers Range of Motion'
    bl_description = "Limit Markers Range of Motion"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Limiting Markers Range of Motion.......")

        scene = context.scene
        props = context.scene.freemocap_ui_properties.limit_markers_range_of_motion_properties

        # Get the top-level parent empty that contains all marker empties
        data_parent_empty = bpy.data.objects[
            context.scene.freemocap_properties.scope_data_parent
        ]

        # Frame Range
        start_frame = context.scene.frame_start
        end_frame = context.scene.frame_end

        target_categories = []

        if props.limit_palm_markers:
            target_categories.append('palm')
        if props.limit_proximal_phalanx_markers:
            target_categories.append('proximal_phalanx')
        if props.limit_intermediate_phalanx_markers:
            target_categories.append('intermediate_phalanx')
        if props.limit_distal_phalanx_markers:
            target_categories.append('distal_phalanx')
            
        if len(target_categories) == 0:
            print("No target categories selected")
            return {'FINISHED'}
        
        range_of_motion_scale = props.range_of_motion_scale
        hand_locked_track_marker_name = props.hand_locked_track_marker
        hand_damped_track_marker_name = props.hand_damped_track_marker

        limit_markers_range_of_motion(
            data_parent_empty=data_parent_empty,
            start_frame=start_frame,
            end_frame=end_frame,
            target_categories=target_categories,
            range_of_motion_scale=range_of_motion_scale,
            hand_locked_track_marker_name=hand_locked_track_marker_name,
            hand_damped_track_marker_name=hand_damped_track_marker_name,
        )

        return {'FINISHED'}
