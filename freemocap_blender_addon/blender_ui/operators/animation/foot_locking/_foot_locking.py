import bpy
import numpy as np

from freemocap_blender_addon.blender_ui.operators.animation.foot_locking.methods.foot_group_movement import run_foot_group_movement


class FREEMOCAP_OT_foot_locking(bpy.types.Operator):
    bl_idname = 'freemocap._foot_locking'
    bl_label = 'Foot Locking'
    bl_description = "Foot Locking"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        # Get the top-level parent empty that contains all marker empties
        data_parent_empty = bpy.data.objects[
            context.scene.freemocap_properties.scope_data_parent
        ]

        # ── Frame Range ──────────────────────────────────────────────────
        start_frame = context.scene.frame_start
        end_frame = context.scene.frame_end

        props = context.scene.freemocap_ui_properties.foot_locking_properties

        if props.foot_locking_method == 'foot_group_movement':

            print("Applying Foot Locking (Method: Foot Group Movement).......")

            # Determine which feet to process
            if props.fgm_target_foot == 'both_feet':
                target_foot_list = ['left_foot', 'right_foot']
            else:
                target_foot_list = [props.fgm_target_foot]

            # Foot locking algorithm parameters
            z_threshold = props.fgm_z_threshold
            ground_level = props.fgm_ground_level
            negative_height_limit = props.fgm_negative_height_limit
            min_lock_frames = props.fgm_min_lock_frames
            blend_frames = props.fgm_blend_frames
            xy_radius = props.fgm_xy_radius
            xy_moving_average_window = props.fgm_xy_moving_average_window
            knee_hip_compensation_coefficient = props.fgm_knee_hip_compensation_coefficient
            compensate_upper_body = props.fgm_compensate_upper_body
            

            run_foot_group_movement(
                data_parent_empty=data_parent_empty,
                start_frame=start_frame,
                end_frame=end_frame,
                target_foot_list=target_foot_list,
                z_threshold=z_threshold,
                ground_level=ground_level,
                negative_height_limit=negative_height_limit,
                min_lock_frames=min_lock_frames,
                blend_frames=blend_frames,
                xy_radius=xy_radius,
                xy_moving_average_window=xy_moving_average_window,
                knee_hip_compensation_coefficient=knee_hip_compensation_coefficient,
                compensate_upper_body=compensate_upper_body,
            )

        # Force a viewport refresh by setting the current frame
        context.scene.frame_current = context.scene.frame_current

        return {'FINISHED'}
