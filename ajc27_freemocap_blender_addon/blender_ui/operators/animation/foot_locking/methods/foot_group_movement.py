import bpy
import numpy as np
import math
import mathutils
from mathutils import Vector

from ajc27_freemocap_blender_addon.data_models.bones.bone_definitions import get_bone_definitions
from ajc27_freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.foot_locking_markers import foot_locking_markers
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.helpers.basic_functions import translate_marker

MEDIAPIPE_HIERARCHY = get_mediapipe_hierarchy()

def run_foot_group_movement(context):
    print("Applying Foot Locking (Method: Foot Group Movement).......")
    
    # Debug variables
    debug_foot_locking = True
    debug_target_frame = 165
    debug_frame_window = 15  # Window of 30 frames means +/- 15
    
    scene = context.scene
    props = context.scene.freemocap_ui_properties.foot_locking_properties

    if props.target_foot == 'both_feet':
        target_foot_list = ['left_foot', 'right_foot']
    else:
        target_foot_list = [props.target_foot]

    z_threshold = props.z_threshold
    ground_level = props.ground_level
    knee_hip_compensation_coefficient = props.knee_hip_compensation_coefficient
    
    xy_radius = getattr(props, 'xy_radius', 0.05)
    moving_average_window = getattr(props, 'moving_average_window', 5)
    min_lock_frames = getattr(props, 'frame_window_min_size', 10)
    blend_frames = getattr(props, 'initial_attenuation_count', 5)
    compensate_upper_body = getattr(props, 'compensate_upper_body', True)
    negative_height_limit = getattr(props, 'negative_height_limit', 0.02)

    data_parent_empty = bpy.data.objects[scene.freemocap_properties.scope_data_parent]

    # Create a dictionary with all the markers that are children of the data parent empty
    markers = {}
    for child in data_parent_empty.children_recursive:
        if child.type == 'EMPTY' and 'empties_parent' in child.name:
            for marker in child.children:
                if marker.type == 'EMPTY':
                    # Get the position fcurves
                    fcurve_x = marker.animation_data.action.fcurves.find("location", index=0)
                    fcurve_y = marker.animation_data.action.fcurves.find("location", index=1)
                    fcurve_z = marker.animation_data.action.fcurves.find("location", index=2)

                    if fcurve_x is None or fcurve_y is None or fcurve_z is None:
                        continue

                    # Get the fcurve data as numpy arrays
                    fcurve_data = np.array([
                        [kp.co[1] for kp in fcurve_x.keyframe_points],
                        [kp.co[1] for kp in fcurve_y.keyframe_points],
                        [kp.co[1] for kp in fcurve_z.keyframe_points]
                    ])
            
                    markers[marker.name] = {
                        'object': marker,
                        'fcurves': fcurve_data,
                    }

    start_frame = scene.frame_start
    end_frame = scene.frame_end
    last_frame = end_frame - start_frame
    
    overall_changed_frames = []

    def apply_foot_lock(markers, heel_name, toe_name, ankle_name, compensation_markers, frame_start, frame_end, z_threshold, xy_radius, window, min_lock_frames, blend_frames, knee_hip_compensation_coefficient, negative_height_limit):
        def get_pos(marker, f):
            return Vector((
                markers[marker]['fcurves'][0, f],
                markers[marker]['fcurves'][1, f],
                markers[marker]['fcurves'][2, f]
            ))

        def set_pos(marker, f, vec):
            markers[marker]['fcurves'][0, f] = vec.x
            markers[marker]['fcurves'][1, f] = vec.y
            markers[marker]['fcurves'][2, f] = vec.z

        lock_states = {heel_name: {}, toe_name: {}}
        target_positions = {heel_name: {}, toe_name: {}}

        for marker in [heel_name, toe_name]:
            candidate_frames = []
            for f in range(frame_start, frame_end + 1):
                pos = get_pos(marker, f)
                
                # Window boundaries
                start_w = max(frame_start, f - window)
                end_w = min(frame_end, f + window)
                
                # Calculate XY average for the window
                avg_x = sum(markers[marker]['fcurves'][0, i] for i in range(start_w, end_w + 1)) / (end_w - start_w + 1)
                avg_y = sum(markers[marker]['fcurves'][1, i] for i in range(start_w, end_w + 1)) / (end_w - start_w + 1)
                
                # Check conditions
                xy_dist = math.sqrt((pos.x - avg_x)**2 + (pos.y - avg_y)**2)
                
                cond_z = pos.z < z_threshold
                cond_xy = xy_dist <= xy_radius

                if cond_z and cond_xy:
                    candidate_frames.append(f)
                    target_positions[marker][f] = Vector((avg_x, avg_y, ground_level))
                else:
                    candidate_frames.clear()
                    
                # If we hit the minimum frame count, retroactively mark them as locked
                if len(candidate_frames) >= min_lock_frames:
                    for lock_f in candidate_frames:
                        lock_states[marker][lock_f] = True

                if debug_foot_locking and 'right' in marker and abs(f - debug_target_frame) <= debug_frame_window:
                    print(f"[DEBUG CANDIDATE F{f}] {marker}: pos.z={pos.z:.5f} (th={z_threshold:.5f})[{'OK' if cond_z else 'FAIL'}], xy_dist={xy_dist:.5f} (th={xy_radius:.5f})[{'OK' if cond_xy else 'FAIL'}], accum_candidates={len(candidate_frames)}, locked={lock_states.get(marker, {}).get(f, False)}")

        # Group into Contiguous Locked Blocks (separate for heel and toe)
        def get_blocks(marker_name):
            locked_frames = [f for f in range(frame_start, frame_end + 1) if lock_states[marker_name].get(f, False)]
            blocks = []
            if locked_frames:
                current = [locked_frames[0]]
                for f in locked_frames[1:]:
                    if f == current[-1] + 1:
                        current.append(f)
                    else:
                        blocks.append((current[0], current[-1]))
                        current = [f]
                blocks.append((current[0], current[-1]))
            return blocks

        heel_blocks = get_blocks(heel_name)
        toe_blocks = get_blocks(toe_name)

        if debug_foot_locking and 'right' in heel_name:
            print(f"\n[DEBUG] Heel blocks:")
            for b in heel_blocks: print(f"  {b}")
            print(f"[DEBUG] Toe blocks:")
            for b in toe_blocks: print(f"  {b}")
            print()

        def get_weight(f, blocks):
            best_t = 0.0
            for b_start, b_end in blocks:
                if b_start <= f <= b_end:
                    max_b = min(blend_frames, (b_end - b_start) // 2)
                    d_edge = min(f - b_start, b_end - f)
                    if d_edge <= max_b and max_b > 0:
                        t = (d_edge + 1) / (max_b + 1)
                        t_sq = t * t
                        if t_sq > best_t: best_t = t_sq
                    else:
                        best_t = 1.0
            return best_t

        all_changed = set()
        for b_start, b_end in heel_blocks + toe_blocks:
            for f in range(b_start, b_end + 1):
                all_changed.add(f)
        
        # Ensure we process any frames that might dip below ground for anti-digging
        for f in range(frame_start, frame_end + 1):
            if get_pos(heel_name, f).z < ground_level or get_pos(toe_name, f).z < ground_level:
                all_changed.add(f)
        
        changed_frames = sorted(list(all_changed))

        for f in changed_frames:
            heel_w = get_weight(f, heel_blocks)
            toe_w = get_weight(f, toe_blocks)

            orig_heel = get_pos(heel_name, f)
            orig_toe = get_pos(toe_name, f)
            orig_ankle = get_pos(ankle_name, f)

            fallback_heel = Vector((orig_heel.x, orig_heel.y, ground_level))
            fallback_toe = Vector((orig_toe.x, orig_toe.y, ground_level))

            locked_heel = target_positions[heel_name].get(f, fallback_heel)
            locked_toe = target_positions[toe_name].get(f, fallback_toe)

            target_heel = orig_heel.lerp(locked_heel, heel_w)
            target_toe = orig_toe.lerp(locked_toe, toe_w)

            # Preserve exact bone length between heel and toe
            orig_foot_vec = orig_toe - orig_heel
            foot_length = orig_foot_vec.length

            target_vec = target_toe - target_heel
            if target_vec.length > 0:
                target_dir = target_vec.normalized()
            else:
                target_dir = orig_foot_vec.normalized() if foot_length > 0 else Vector((0, 1, 0))

            if heel_w + toe_w > 0:
                # Pivot closer to the part that is more locked
                pivot_weight = toe_w / (heel_w + toe_w)
            else:
                pivot_weight = 0.5
            
            # This is the point on the target line that we keep fixed
            # It will match the blended target positions exactly based on the pivot_weight
            pivot_pos = target_heel.lerp(target_toe, pivot_weight)

            # Reconstruct heel and toe out of the fixed pivot to ensure exact distance
            final_heel = pivot_pos - target_dir * (foot_length * pivot_weight)
            final_toe = pivot_pos + target_dir * (foot_length * (1.0 - pivot_weight))

            # Maintain rigid ankle relation by calculating exact rotation applied to the bone
            if foot_length > 0:
                rotation = orig_foot_vec.normalized().rotation_difference(target_dir)
                final_ankle = final_heel + rotation @ (orig_ankle - orig_heel)
            else:
                final_ankle = orig_ankle

            # Soft Anti-Digging Constraint
            # If the structure dips below ground, push it up, but limit body lift to negative_height_limit.
            lowest_z = min(final_heel.z, final_toe.z)
            if lowest_z < ground_level:
                comp = ground_level - lowest_z
                max_lift = negative_height_limit
                actual_comp = min(comp, max_lift)
                
                final_heel.z += actual_comp
                final_toe.z += actual_comp
                final_ankle.z += actual_comp
                
                if comp > max_lift + 1e-5:
                    # Still dipping. Rotate foot around final_ankle to bring base markers up.
                    target_z = ground_level - final_ankle.z
                    dir_xy = Vector((final_toe.x - final_heel.x, final_toe.y - final_heel.y, 0))
                    if dir_xy.length > 0:
                        dir_xy.normalize()
                        axis = Vector((dir_xy.y, -dir_xy.x, 0))
                        
                        def get_pitch_angle(A, B, C):
                            R = math.sqrt(A**2 + B**2)
                            if R < abs(C) or R == 0:
                                return 0.0
                            alpha = math.atan2(B, A)
                            val = max(-1.0, min(1.0, C / R))
                            th1 = alpha + math.acos(val)
                            th2 = alpha - math.acos(val)
                            def norm(a):
                                while a > math.pi: a -= 2*math.pi
                                while a < -math.pi: a += 2*math.pi
                                return a
                            th1, th2 = norm(th1), norm(th2)
                            return th1 if abs(th1) < abs(th2) else th2

                        thetas = []
                        vh = final_heel - final_ankle
                        vt = final_toe - final_ankle
                        
                        if final_heel.z < ground_level:
                            Lh = dir_xy.x * vh.x + dir_xy.y * vh.y
                            thetas.append(get_pitch_angle(vh.z, Lh, target_z))
                        if final_toe.z < ground_level:
                            Lt = dir_xy.x * vt.x + dir_xy.y * vt.y
                            thetas.append(get_pitch_angle(vt.z, Lt, target_z))
                            
                        if thetas:
                            valid_thetas = []
                            for th in thetas:
                                rot = mathutils.Quaternion(axis, th)
                                test_h = rot @ vh
                                test_t = rot @ vt
                                if test_h.z >= target_z - 1e-4 and test_t.z >= target_z - 1e-4:
                                    valid_thetas.append(th)
                            if valid_thetas:
                                best_theta = min(valid_thetas, key=abs)
                            else:
                                best_theta = max(thetas, key=lambda t: min((mathutils.Quaternion(axis, t) @ vh).z, (mathutils.Quaternion(axis, t) @ vt).z))
                                
                            rot = mathutils.Quaternion(axis, best_theta)
                            final_heel = final_ankle + rot @ vh
                            final_toe = final_ankle + rot @ vt

            is_debug_frame = (debug_foot_locking and 
                              'right' in heel_name and 
                              abs(f - debug_target_frame) <= debug_frame_window)
            if is_debug_frame:
                print(f"[DEBUG BLEND F{f}] heel_w={heel_w:.4f}, toe_w={toe_w:.4f}, pivot_w={pivot_weight:.4f}")
                print(f"[DEBUG BLEND F{f}]   orig_h.z={orig_heel.z:.5f}, target_h.z={target_heel.z:.5f}, final_h.z={final_heel.z:.5f}")
                print(f"[DEBUG BLEND F{f}]   orig_t.z={orig_toe.z:.5f}, target_t.z={target_toe.z:.5f}, final_t.z={final_toe.z:.5f}")

            set_pos(heel_name, f, final_heel)
            set_pos(toe_name, f, final_toe)
            set_pos(ankle_name, f, final_ankle)

            if knee_hip_compensation_coefficient != 0:
                delta = final_ankle - orig_ankle
                for comp_marker in compensation_markers:
                    orig_comp = get_pos(comp_marker, f)
                    set_pos(comp_marker, f, orig_comp + delta * knee_hip_compensation_coefficient)
        
        return changed_frames

    for foot in foot_locking_markers:
        if foot not in target_foot_list:
            continue
            
        toe_name = None
        heel_name = None
        for base_marker in foot_locking_markers[foot]['base']:
            if 'index' in base_marker or 'toe' in base_marker:
                toe_name = base_marker
            elif 'heel' in base_marker:
                heel_name = base_marker
                
        ankle_name = foot_locking_markers[foot]['ankle'][0]

        if not heel_name or not toe_name or not ankle_name:
            continue

        changed_frames = apply_foot_lock(
            markers=markers,
            heel_name=heel_name,
            toe_name=toe_name,
            ankle_name=ankle_name,
            compensation_markers=foot_locking_markers[foot]['compensation_markers'],
            frame_start=0,
            frame_end=last_frame - 1,
            z_threshold=z_threshold,
            xy_radius=xy_radius,
            window=moving_average_window,
            min_lock_frames=min_lock_frames,
            blend_frames=blend_frames,
            knee_hip_compensation_coefficient=knee_hip_compensation_coefficient,
            negative_height_limit=negative_height_limit
        )
        overall_changed_frames.extend(changed_frames)

    overall_changed_frames = list(set(overall_changed_frames))

    if compensate_upper_body:
        for changed_frame in overall_changed_frames:
            new_hips_center_z = (
                markers['left_hip']['fcurves'][2, changed_frame]
                + markers['right_hip']['fcurves'][2, changed_frame]
            ) / 2
                
            delta_list = [
                0,
                0,
                new_hips_center_z - markers['hips_center']['fcurves'][2, changed_frame]
            ]

            markers['hips_center']['fcurves'][2, changed_frame] = new_hips_center_z

            translate_marker(
                MEDIAPIPE_HIERARCHY,
                markers,
                'trunk_center',
                delta_list,
                changed_frame,
            )

    # Output back to blender actions
    for marker_name, marker_data in markers.items():
        for axis_idx in range(3):
            fcurve = marker_data['object'].animation_data.action.fcurves.find("location", index=axis_idx)
            if fcurve is not None:
                co = np.empty(2 * len(marker_data['fcurves'][axis_idx]), dtype=np.float32)
                co[0::2] = np.arange(len(marker_data['fcurves'][axis_idx]))  
                co[1::2] = marker_data['fcurves'][axis_idx]  
                fcurve.keyframe_points.foreach_set("co", co)
                fcurve.update()  

    scene.frame_current = scene.frame_current
