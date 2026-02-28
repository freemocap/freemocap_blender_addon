"""
Foot Group Movement - Foot Locking Method

This method applies foot locking by analyzing the heel and foot_index
(toe) markers to detect when the foot is stationary on the ground.
It groups those frames into contiguous locked blocks, blends
the transition in/out with quadratic easing, preserves the original
bone length between heel and toe, and optionally compensates
the knee, hip, and upper body markers.

Additionally, a "Soft Anti-Digging Constraint" prevents foot markers
from going below the ground level. When the required lift exceeds
the configurable negative_height_limit, the foot is rotated around
the ankle to bring the markers up to ground level instead of
lifting the entire leg structure.
"""

import bpy
import numpy as np
import math
import mathutils
from mathutils import Vector

from ajc27_freemocap_blender_addon.data_models.bones.bone_definitions import (
    get_bone_definitions,
)
from ajc27_freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import (
    get_mediapipe_hierarchy,
)
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.foot_locking_markers import (
    foot_locking_markers,
)
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.helpers.basic_functions import (
    translate_marker,
)

# Load the mediapipe hierarchy once at module level
MEDIAPIPE_HIERARCHY = get_mediapipe_hierarchy()


def run_foot_group_movement(context):
    """
    Main entry point for the Foot Group Movement foot-locking method.
    Called by the foot locking operator when this method is selected.
    """
    print("Applying Foot Locking (Method: Foot Group Movement).......")

    # ── Debug Configuration ──────────────────────────────────────────
    # Set debug_foot_locking to True to print detailed per-frame info
    # for the right foot within a window around debug_target_frame.
    debug_foot_locking = True
    debug_target_frame = 165
    debug_frame_window = 15  # Print debug info for frames ±15 around target

    # ── Read UI Properties ───────────────────────────────────────────
    scene = context.scene
    props = scene.freemocap_ui_properties.foot_locking_properties

    # Determine which feet to process
    if props.fgm_target_foot == 'both_feet':
        target_foot_list = ['left_foot', 'right_foot']
    else:
        target_foot_list = [props.fgm_target_foot]

    # Foot locking algorithm parameters
    z_threshold = props.fgm_z_threshold
    ground_level = props.fgm_ground_level
    knee_hip_compensation_coefficient = props.fgm_knee_hip_compensation_coefficient
    xy_radius = props.fgm_xy_radius
    moving_average_window = props.fgm_moving_average_window
    min_lock_frames = props.fgm_frame_window_min_size
    blend_frames = props.fgm_initial_attenuation_count
    compensate_upper_body = props.fgm_compensate_upper_body
    negative_height_limit = props.fgm_negative_height_limit

    # ── Load All Marker Data ─────────────────────────────────────────
    # Get the top-level parent empty that contains all marker empties
    data_parent_empty = bpy.data.objects[
        scene.freemocap_properties.scope_data_parent
    ]

    # Build a dictionary mapping marker names to their fcurve data.
    # Each entry contains:
    #   'object': the Blender empty object
    #   'fcurves': a numpy array of shape (3, num_frames) with XYZ positions
    markers = {}
    for child in data_parent_empty.children_recursive:
        if child.type == 'EMPTY' and 'empties_parent' in child.name:
            for marker in child.children:
                if marker.type == 'EMPTY':
                    # Find the location fcurves for X, Y, Z axes
                    fcurve_x = marker.animation_data.action.fcurves.find(
                        "location", index=0
                    )
                    fcurve_y = marker.animation_data.action.fcurves.find(
                        "location", index=1
                    )
                    fcurve_z = marker.animation_data.action.fcurves.find(
                        "location", index=2
                    )

                    # Skip markers without complete location fcurves
                    if fcurve_x is None or fcurve_y is None or fcurve_z is None:
                        continue

                    # Extract keyframe values into a numpy array (3 x num_frames)
                    fcurve_data = np.array([
                        [kp.co[1] for kp in fcurve_x.keyframe_points],
                        [kp.co[1] for kp in fcurve_y.keyframe_points],
                        [kp.co[1] for kp in fcurve_z.keyframe_points],
                    ])

                    markers[marker.name] = {
                        'object': marker,
                        'fcurves': fcurve_data,
                    }

    # ── Frame Range ──────────────────────────────────────────────────
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    # last_frame is the relative index of the last frame (0-based)
    last_frame = end_frame - start_frame

    # Accumulate all frames that were modified across both feet
    overall_changed_frames = []

    # ── Core Foot Locking Function ───────────────────────────────────
    def apply_foot_lock(
        markers,
        heel_name,
        toe_name,
        ankle_name,
        compensation_markers,
        frame_start,
        frame_end,
        z_threshold,
        xy_radius,
        moving_average_window,
        min_lock_frames,
        blend_frames,
        knee_hip_compensation_coefficient,
        negative_height_limit,
    ):
        """
        Apply foot locking to a single foot (heel + toe pair).

        This function:
        1. Identifies candidate locked frames based on Z height and XY
           stillness criteria.
        2. Groups them into contiguous blocks.
        3. Blends positions with quadratic easing at block edges.
        4. Preserves bone length between heel and toe.
        5. Applies anti-digging constraints.
        6. Compensates knee/hip markers.

        Returns:
            list: Sorted list of frame indices that were modified.
        """

        def get_position(marker_name, frame):
            """
            Retrieve the 3D position of a marker at a given frame
            from the fcurve data arrays.
            """
            return Vector((
                markers[marker_name]['fcurves'][0, frame],
                markers[marker_name]['fcurves'][1, frame],
                markers[marker_name]['fcurves'][2, frame],
            ))

        def set_position(marker_name, frame, position):
            """
            Write a 3D position back into the fcurve data arrays
            for a marker at a given frame.
            """
            markers[marker_name]['fcurves'][0, frame] = position.x
            markers[marker_name]['fcurves'][1, frame] = position.y
            markers[marker_name]['fcurves'][2, frame] = position.z

        # ── Phase 1: Identify Locked Frames ──────────────────────────
        # For each marker (heel and toe), determine which frames should
        # be considered "locked" (foot stationary on the ground).
        # A frame is a candidate if:
        #   - Its Z position is below z_threshold
        #   - Its XY position is within xy_radius of the local
        #     moving average
        # Candidates must form a consecutive run of at least
        # min_lock_frames to be confirmed as locked.

        # Dictionaries mapping frame -> True for locked frames
        lock_states = {heel_name: {}, toe_name: {}}
        # Dictionaries mapping frame -> target locked position (Vector)
        target_positions = {heel_name: {}, toe_name: {}}

        for marker_name in [heel_name, toe_name]:
            # Accumulates consecutive candidate frames.
            # If the chain breaks before reaching min_lock_frames,
            # it is cleared.
            candidate_frames = []

            for frame in range(frame_start, frame_end + 1):
                position = get_position(marker_name, frame)

                # Calculate the moving average window boundaries
                window_start = max(frame_start, frame - moving_average_window)
                window_end = min(frame_end, frame + moving_average_window)
                window_size = window_end - window_start + 1

                # Calculate the XY average position within the window
                avg_x = sum(
                    markers[marker_name]['fcurves'][0, i]
                    for i in range(window_start, window_end + 1)
                ) / window_size
                avg_y = sum(
                    markers[marker_name]['fcurves'][1, i]
                    for i in range(window_start, window_end + 1)
                ) / window_size

                # Check if the marker is below the Z threshold
                is_below_z_threshold = position.z < z_threshold

                # Check if the marker's XY distance from the window
                # average is within the allowed radius
                xy_distance = math.sqrt(
                    (position.x - avg_x) ** 2
                    + (position.y - avg_y) ** 2
                )
                is_within_xy_radius = xy_distance <= xy_radius

                if is_below_z_threshold and is_within_xy_radius:
                    # Frame is a lock candidate
                    candidate_frames.append(frame)
                    # Target position: XY from the window average,
                    # Z exactly at ground level
                    target_positions[marker_name][frame] = Vector((
                        avg_x,
                        avg_y,
                        ground_level,
                    ))
                else:
                    # Chain broken — clear all accumulated candidates
                    candidate_frames.clear()

                # Once we accumulate enough consecutive candidates,
                # retroactively mark all of them as locked
                if len(candidate_frames) >= min_lock_frames:
                    for candidate_frame in candidate_frames:
                        lock_states[marker_name][candidate_frame] = True

                # Debug output for right foot frames near the target
                if (
                    debug_foot_locking
                    and 'right' in marker_name
                    and abs(frame - debug_target_frame) <= debug_frame_window
                ):
                    z_status = 'OK' if is_below_z_threshold else 'FAIL'
                    xy_status = 'OK' if is_within_xy_radius else 'FAIL'
                    is_locked = lock_states.get(
                        marker_name, {}
                    ).get(frame, False)
                    print(
                        f"[DEBUG CANDIDATE F{frame}] {marker_name}: "
                        f"pos.z={position.z:.5f} "
                        f"(th={z_threshold:.5f})[{z_status}], "
                        f"xy_dist={xy_distance:.5f} "
                        f"(th={xy_radius:.5f})[{xy_status}], "
                        f"accum_candidates={len(candidate_frames)}, "
                        f"locked={is_locked}"
                    )

        # ── Phase 2: Group Locked Frames into Contiguous Blocks ──────

        def get_contiguous_blocks(marker_name):
            """
            Given a marker's lock_states dictionary, return a list of
            (block_start, block_end) tuples representing contiguous
            runs of locked frames.
            """
            locked_frames = [
                frame
                for frame in range(frame_start, frame_end + 1)
                if lock_states[marker_name].get(frame, False)
            ]
            blocks = []
            if locked_frames:
                current_block = [locked_frames[0]]
                for frame in locked_frames[1:]:
                    if frame == current_block[-1] + 1:
                        # Contiguous — extend the current block
                        current_block.append(frame)
                    else:
                        # Gap found — close the current block
                        blocks.append((
                            current_block[0],
                            current_block[-1],
                        ))
                        current_block = [frame]
                # Close the final block
                blocks.append((current_block[0], current_block[-1]))
            return blocks

        heel_blocks = get_contiguous_blocks(heel_name)
        toe_blocks = get_contiguous_blocks(toe_name)

        # Debug: print discovered blocks for the right foot
        if debug_foot_locking and 'right' in heel_name:
            print(f"\n[DEBUG] Heel blocks:")
            for block in heel_blocks:
                print(f"  {block}")
            print(f"[DEBUG] Toe blocks:")
            for block in toe_blocks:
                print(f"  {block}")
            print()

        # ── Phase 3: Calculate Blend Weights ─────────────────────────

        def get_blend_weight(frame, blocks):
            """
            Calculate the blend weight for a frame given its lock blocks.

            The weight is 0.0 outside any block, ramps up quadratically
            from the block edges over blend_frames, and is 1.0 in the
            interior of the block. This creates smooth transitions
            at lock boundaries.

            Returns:
                float: Weight between 0.0 (no locking) and 1.0
                       (fully locked).
            """
            best_weight = 0.0
            for block_start, block_end in blocks:
                if block_start <= frame <= block_end:
                    # Maximum blend zone is half the block length
                    max_blend = min(
                        blend_frames,
                        (block_end - block_start) // 2,
                    )
                    # Distance from the nearest block edge
                    distance_from_edge = min(
                        frame - block_start,
                        block_end - frame,
                    )
                    if distance_from_edge <= max_blend and max_blend > 0:
                        # Quadratic ease-in from the edge
                        linear_t = (distance_from_edge + 1) / (max_blend + 1)
                        quadratic_weight = linear_t * linear_t
                        if quadratic_weight > best_weight:
                            best_weight = quadratic_weight
                    else:
                        # Fully inside the block interior
                        best_weight = 1.0
            return best_weight

        # ── Phase 4: Build the Set of Frames to Process ──────────────
        # Include all frames from lock blocks plus any frame where
        # the heel or toe dips below ground level (anti-digging).
        all_changed_frames = set()

        # Add all frames from heel and toe lock blocks
        for block_start, block_end in heel_blocks + toe_blocks:
            for frame in range(block_start, block_end + 1):
                all_changed_frames.add(frame)

        # Ensure we process any frames that dip below ground level,
        # even if they are not part of a lock block.
        # This guarantees the anti-digging constraint is always applied.
        for frame in range(frame_start, frame_end + 1):
            heel_z = get_position(heel_name, frame).z
            toe_z = get_position(toe_name, frame).z
            if heel_z < ground_level or toe_z < ground_level:
                all_changed_frames.add(frame)

        changed_frames = sorted(list(all_changed_frames))

        # ── Phase 5: Apply Locking, Length Preservation & Constraints ─
        for frame in changed_frames:
            # Get the blend weights for this frame
            heel_weight = get_blend_weight(frame, heel_blocks)
            toe_weight = get_blend_weight(frame, toe_blocks)

            # Read original positions
            original_heel = get_position(heel_name, frame)
            original_toe = get_position(toe_name, frame)
            original_ankle = get_position(ankle_name, frame)

            # Fallback locked positions: same XY as original,
            # but Z set to ground level. Used when a frame is outside
            # any lock block but still needs anti-digging.
            fallback_heel = Vector((
                original_heel.x,
                original_heel.y,
                ground_level,
            ))
            fallback_toe = Vector((
                original_toe.x,
                original_toe.y,
                ground_level,
            ))

            # Get the locked target position (from Phase 1) or fallback
            locked_heel = target_positions[heel_name].get(
                frame, fallback_heel
            )
            locked_toe = target_positions[toe_name].get(
                frame, fallback_toe
            )

            # Blend between original and locked positions
            # using the per-marker blend weights
            target_heel = original_heel.lerp(locked_heel, heel_weight)
            target_toe = original_toe.lerp(locked_toe, toe_weight)

            # ── Bone Length Preservation ──────────────────────────────
            # Ensure the distance between heel and toe remains exactly
            # the same as the original, preventing stretching/squishing.
            original_foot_vector = original_toe - original_heel
            foot_length = original_foot_vector.length

            # Direction of the target heel-to-toe vector
            target_foot_vector = target_toe - target_heel
            if target_foot_vector.length > 0:
                target_direction = target_foot_vector.normalized()
            else:
                # Degenerate case: fall back to original direction
                if foot_length > 0:
                    target_direction = original_foot_vector.normalized()
                else:
                    target_direction = Vector((0, 1, 0))

            # ── Pivot Point Calculation ──────────────────────────────
            # The pivot point determines where on the heel-toe line
            # we anchor the reconstruction. It is biased toward
            # whichever marker is more heavily locked.
            if heel_weight + toe_weight > 0:
                pivot_weight = toe_weight / (heel_weight + toe_weight)
            else:
                pivot_weight = 0.5

            # The pivot position is a weighted interpolation between
            # the blended target heel and toe
            pivot_position = target_heel.lerp(target_toe, pivot_weight)

            # Reconstruct heel and toe from the pivot so that the
            # original bone length is exactly preserved
            final_heel = (
                pivot_position
                - target_direction * (foot_length * pivot_weight)
            )
            final_toe = (
                pivot_position
                + target_direction * (foot_length * (1.0 - pivot_weight))
            )

            # ── Ankle Position via Rigid Rotation ────────────────────
            # Maintain the ankle's rigid relationship to the foot
            # by computing the rotation from the original foot
            # direction to the target direction, then applying it
            # to the original ankle offset.
            if foot_length > 0:
                rotation = original_foot_vector.normalized().rotation_difference(
                    target_direction
                )
                final_ankle = final_heel + rotation @ (
                    original_ankle - original_heel
                )
            else:
                final_ankle = original_ankle

            # ── Soft Anti-Digging Constraint ─────────────────────────
            # If the foot structure dips below ground level, push it
            # up. However, to avoid unnaturally lifting the entire
            # leg when a marker is deeply negative (e.g. bad tracking),
            # the vertical lift is capped at negative_height_limit.
            # Any remaining depth beyond the cap is compensated by
            # rotating the foot around the ankle to pitch the
            # markers up to ground level.
            lowest_z = min(final_heel.z, final_toe.z)

            if lowest_z < ground_level:
                # Total compensation needed to reach ground level
                total_compensation = ground_level - lowest_z
                # Cap the vertical lift
                max_lift = negative_height_limit
                actual_lift = min(total_compensation, max_lift)

                # Apply the capped vertical lift to all foot markers
                final_heel.z += actual_lift
                final_toe.z += actual_lift
                final_ankle.z += actual_lift

                # If the lift was not enough (marker was too deep),
                # rotate the foot around the ankle to bring the
                # remaining markers up to ground level
                if total_compensation > max_lift + 1e-5:
                    # The target Z for heel/toe relative to the ankle
                    relative_target_z = ground_level - final_ankle.z

                    # Compute the foot's XY direction (projected onto
                    # the horizontal plane) to determine rotation axis
                    foot_xy_direction = Vector((
                        final_toe.x - final_heel.x,
                        final_toe.y - final_heel.y,
                        0,
                    ))

                    if foot_xy_direction.length > 0:
                        foot_xy_direction.normalize()
                        # Rotation axis is perpendicular to the foot
                        # direction in the horizontal plane
                        rotation_axis = Vector((
                            foot_xy_direction.y,
                            -foot_xy_direction.x,
                            0,
                        ))

                        def compute_pitch_angle(
                            vertical_component,
                            horizontal_component,
                            target_z_value,
                        ):
                            """
                            Solve for the pitch angle theta such that:
                              vertical_component * cos(theta)
                              + horizontal_component * sin(theta)
                              = target_z_value

                            This is the standard A*cos + B*sin = C
                            equation, solved via R*cos(theta - alpha) = C.

                            Returns the solution with smallest absolute
                            angle, or 0.0 if no solution exists.
                            """
                            radius = math.sqrt(
                                vertical_component ** 2
                                + horizontal_component ** 2
                            )
                            if radius < abs(target_z_value) or radius == 0:
                                # No solution exists
                                return 0.0
                            alpha = math.atan2(
                                horizontal_component,
                                vertical_component,
                            )
                            clamped_ratio = max(
                                -1.0,
                                min(1.0, target_z_value / radius),
                            )
                            theta_1 = alpha + math.acos(clamped_ratio)
                            theta_2 = alpha - math.acos(clamped_ratio)

                            # Normalize angles to [-pi, pi]
                            def normalize_angle(angle):
                                while angle > math.pi:
                                    angle -= 2 * math.pi
                                while angle < -math.pi:
                                    angle += 2 * math.pi
                                return angle

                            theta_1 = normalize_angle(theta_1)
                            theta_2 = normalize_angle(theta_2)

                            # Return the solution with smallest magnitude
                            if abs(theta_1) < abs(theta_2):
                                return theta_1
                            return theta_2

                        # Collect candidate pitch angles for each
                        # marker that is still below ground
                        candidate_angles = []

                        # Vectors from ankle to heel and toe
                        ankle_to_heel = final_heel - final_ankle
                        ankle_to_toe = final_toe - final_ankle

                        if final_heel.z < ground_level:
                            # Project ankle-to-heel onto the foot
                            # XY direction for the horizontal component
                            heel_horizontal = (
                                foot_xy_direction.x * ankle_to_heel.x
                                + foot_xy_direction.y * ankle_to_heel.y
                            )
                            candidate_angles.append(
                                compute_pitch_angle(
                                    ankle_to_heel.z,
                                    heel_horizontal,
                                    relative_target_z,
                                )
                            )

                        if final_toe.z < ground_level:
                            # Project ankle-to-toe onto the foot
                            # XY direction for the horizontal component
                            toe_horizontal = (
                                foot_xy_direction.x * ankle_to_toe.x
                                + foot_xy_direction.y * ankle_to_toe.y
                            )
                            candidate_angles.append(
                                compute_pitch_angle(
                                    ankle_to_toe.z,
                                    toe_horizontal,
                                    relative_target_z,
                                )
                            )

                        if candidate_angles:
                            # Filter for angles that bring BOTH markers
                            # above ground level
                            valid_angles = []
                            for angle in candidate_angles:
                                test_rotation = mathutils.Quaternion(
                                    rotation_axis, angle
                                )
                                test_heel = test_rotation @ ankle_to_heel
                                test_toe = test_rotation @ ankle_to_toe
                                if (
                                    test_heel.z >= relative_target_z - 1e-4
                                    and test_toe.z >= relative_target_z - 1e-4
                                ):
                                    valid_angles.append(angle)

                            if valid_angles:
                                # Pick the smallest valid rotation
                                best_angle = min(
                                    valid_angles, key=abs
                                )
                            else:
                                # No perfect solution — pick the angle
                                # that maximizes the lowest marker Z
                                best_angle = max(
                                    candidate_angles,
                                    key=lambda a: min(
                                        (
                                            mathutils.Quaternion(
                                                rotation_axis, a
                                            ) @ ankle_to_heel
                                        ).z,
                                        (
                                            mathutils.Quaternion(
                                                rotation_axis, a
                                            ) @ ankle_to_toe
                                        ).z,
                                    ),
                                )

                            # Apply the best rotation
                            best_rotation = mathutils.Quaternion(
                                rotation_axis, best_angle
                            )
                            final_heel = (
                                final_ankle
                                + best_rotation @ ankle_to_heel
                            )
                            final_toe = (
                                final_ankle
                                + best_rotation @ ankle_to_toe
                            )

            # ── Debug Output ─────────────────────────────────────────
            is_debug_frame = (
                debug_foot_locking
                and 'right' in heel_name
                and abs(frame - debug_target_frame) <= debug_frame_window
            )
            if is_debug_frame:
                print(
                    f"[DEBUG BLEND F{frame}] "
                    f"heel_w={heel_weight:.4f}, "
                    f"toe_w={toe_weight:.4f}, "
                    f"pivot_w={pivot_weight:.4f}"
                )
                print(
                    f"[DEBUG BLEND F{frame}]   "
                    f"orig_h.z={original_heel.z:.5f}, "
                    f"target_h.z={target_heel.z:.5f}, "
                    f"final_h.z={final_heel.z:.5f}"
                )
                print(
                    f"[DEBUG BLEND F{frame}]   "
                    f"orig_t.z={original_toe.z:.5f}, "
                    f"target_t.z={target_toe.z:.5f}, "
                    f"final_t.z={final_toe.z:.5f}"
                )

            # ── Write Final Positions ────────────────────────────────
            set_position(heel_name, frame, final_heel)
            set_position(toe_name, frame, final_toe)
            set_position(ankle_name, frame, final_ankle)

            # ── Knee / Hip Compensation ──────────────────────────────
            # Apply the ankle displacement delta to the knee and hip
            # markers, scaled per-axis by the compensation coefficient
            # vector (X, Y, Z). Default is (0, 0, 1) meaning only
            # Z compensation is applied.
            if any(c != 0 for c in knee_hip_compensation_coefficient):
                ankle_delta = final_ankle - original_ankle
                compensation_delta = Vector((
                    ankle_delta.x * knee_hip_compensation_coefficient[0],
                    ankle_delta.y * knee_hip_compensation_coefficient[1],
                    ankle_delta.z * knee_hip_compensation_coefficient[2],
                ))
                for compensation_marker in compensation_markers:
                    original_compensation_pos = get_position(
                        compensation_marker, frame
                    )
                    set_position(
                        compensation_marker,
                        frame,
                        original_compensation_pos + compensation_delta,
                    )

        return changed_frames

    # ── Process Each Target Foot ─────────────────────────────────────
    for foot in foot_locking_markers:
        if foot not in target_foot_list:
            continue

        # Identify the heel and toe marker names from the foot config
        toe_name = None
        heel_name = None
        for base_marker in foot_locking_markers[foot]['base']:
            if 'index' in base_marker or 'toe' in base_marker:
                toe_name = base_marker
            elif 'heel' in base_marker:
                heel_name = base_marker

        # Get the ankle marker name
        ankle_name = foot_locking_markers[foot]['ankle'][0]

        # Skip if any required marker is missing
        if not heel_name or not toe_name or not ankle_name:
            continue

        # Run the foot locking algorithm for this foot
        changed_frames = apply_foot_lock(
            markers=markers,
            heel_name=heel_name,
            toe_name=toe_name,
            ankle_name=ankle_name,
            compensation_markers=foot_locking_markers[foot][
                'compensation_markers'
            ],
            frame_start=0,
            frame_end=last_frame - 1,
            z_threshold=z_threshold,
            xy_radius=xy_radius,
            moving_average_window=moving_average_window,
            min_lock_frames=min_lock_frames,
            blend_frames=blend_frames,
            knee_hip_compensation_coefficient=knee_hip_compensation_coefficient,
            negative_height_limit=negative_height_limit,
        )
        overall_changed_frames.extend(changed_frames)

    # Deduplicate the list of changed frames
    overall_changed_frames = list(set(overall_changed_frames))

    # ── Upper Body Compensation ──────────────────────────────────────
    # Recalculate the hips_center Z as the average of left and right
    # hip Z positions, then propagate that delta upward through the
    # trunk_center and the rest of the upper body marker chain.
    if compensate_upper_body:
        for changed_frame in overall_changed_frames:
            # New hips center Z = average of left and right hip Z
            new_hips_center_z = (
                markers['left_hip']['fcurves'][2, changed_frame]
                + markers['right_hip']['fcurves'][2, changed_frame]
            ) / 2

            # Calculate the Z delta to propagate to the upper body
            upper_body_delta = [
                0,
                0,
                new_hips_center_z
                - markers['hips_center']['fcurves'][2, changed_frame],
            ]

            # Update the hips_center marker
            markers['hips_center']['fcurves'][2, changed_frame] = (
                new_hips_center_z
            )

            # Propagate the delta to all upper body markers
            # starting from trunk_center
            translate_marker(
                MEDIAPIPE_HIERARCHY,
                markers,
                'trunk_center',
                upper_body_delta,
                changed_frame,
            )

    # ── Write Modified Data Back to Blender ──────────────────────────
    # Transfer the modified numpy arrays back into the Blender
    # fcurve keyframe points using the efficient foreach_set method.
    for marker_name, marker_data in markers.items():
        for axis_idx in range(3):
            fcurve = marker_data['object'].animation_data.action.fcurves.find(
                "location", index=axis_idx
            )
            if fcurve is not None:
                # Build a flat array of [frame0, val0, frame1, val1, ...]
                num_keyframes = len(marker_data['fcurves'][axis_idx])
                co = np.empty(2 * num_keyframes, dtype=np.float32)
                co[0::2] = np.arange(num_keyframes)  # Frame indices
                co[1::2] = marker_data['fcurves'][axis_idx]  # Values
                fcurve.keyframe_points.foreach_set("co", co)
                fcurve.update()

    # Force a viewport refresh by setting the current frame
    scene.frame_current = scene.frame_current
