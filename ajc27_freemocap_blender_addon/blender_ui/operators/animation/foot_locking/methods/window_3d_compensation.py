import bpy
import numpy as np
import math

from ajc27_freemocap_blender_addon.data_models.bones.bone_definitions import get_bone_definitions
from ajc27_freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.foot_locking_markers import foot_locking_markers
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.helpers.basic_functions import translate_marker_3d, translate_marker, quadratic_function, error_function_3d
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.helpers.minimize_functions import gradient_descent_3d

MEDIAPIPE_HIERARCHY = get_mediapipe_hierarchy()

def run_window_3d_compensation(context):
    print("Applying Foot Locking (Method: Window 3D Compensation).......")
    scene = context.scene
    props = context.scene.freemocap_ui_properties.foot_locking_properties

    # Get the bone definitions
    BONE_DEFINITIONS = get_bone_definitions()

    # Prepare the target foot list
    if props.w3d_target_foot == 'both_feet':
        target_foot_list = ['left_foot', 'right_foot']
    else:
        target_foot_list = [props.w3d_target_foot]

    # Prepare the target base markers
    if props.w3d_target_base_markers == 'foot_index_and_heel':
        target_base_markers_list = ['foot_index', 'heel']
    else:
        target_base_markers_list = [props.w3d_target_base_markers]

    z_threshold = props.w3d_z_threshold
    ground_level = props.w3d_ground_level
    frame_window_min_size = props.w3d_frame_window_min_size
    initial_attenuation_count = props.w3d_initial_attenuation_count
    final_attenuation_count = props.w3d_final_attenuation_count
    lock_xy_at_ground_level = props.w3d_lock_xy_at_ground_level
    knee_hip_compensation_coefficient = props.w3d_knee_hip_compensation_coefficient
    compensate_upper_body = props.w3d_compensate_upper_body

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

    # Get the scene start and end frames
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    last_frame = end_frame - start_frame

    # Define the attenuation functions for Z
    z_initial_attenuation = quadratic_function(
        x1=0,
        x2=(initial_attenuation_count / 2),
        x3=(initial_attenuation_count - 1),
        y1=z_threshold,
        y2=z_threshold - (z_threshold - ground_level) * 3 / 4,
        y3=ground_level)
    
    z_final_attenuation = quadratic_function(
        x1=0,
        x2=(final_attenuation_count / 2),
        x3=(final_attenuation_count - 1),
        y1=ground_level,
        y2=ground_level + (z_threshold - ground_level) * 3 / 4,
        y3=z_threshold)
        
    overall_changed_frames = []
    
    # Pre-calculate sequence wide average XY distance between heel and foot_index for both feet
    avg_xy_dists = {}
    if lock_xy_at_ground_level and 'foot_index' in target_base_markers_list and 'heel' in target_base_markers_list:
        for foot in target_foot_list:
            base_m0 = foot_locking_markers[foot]['base'][0]
            base_m1 = foot_locking_markers[foot]['base'][1]
            if base_m0 in markers and base_m1 in markers:
                dists = []
                for f in range(last_frame):
                    p0 = markers[base_m0]['fcurves'][:2, f]
                    p1 = markers[base_m1]['fcurves'][:2, f]
                    dists.append(np.linalg.norm(p0 - p1))
                avg_xy_dists[foot] = np.mean(dists)

    for foot in foot_locking_markers:
        if foot not in target_foot_list:
            continue

        # Update the median value of the foot bones for later ankle adjustment
        for bone in foot_locking_markers[foot]['bones']:
            bone_lengths = []
            for frame in range(markers[BONE_DEFINITIONS[bone].head]['fcurves'].shape[1]):
                bone_lengths.append(
                    math.dist(
                        markers[BONE_DEFINITIONS[bone].head]['fcurves'][:, frame],
                        markers[BONE_DEFINITIONS[bone].tail]['fcurves'][:, frame]
                    )
                )
            BONE_DEFINITIONS[bone].median = np.median(bone_lengths)

        changed_frames = []

        # Find lock windows analyzing heel and foot_index Z coordinates
        for base_marker in foot_locking_markers[foot]['base']:
            if base_marker not in [foot.split('_')[0] + '_' + marker for marker in target_base_markers_list]:
                continue

            frame = 0 
            window = 0
            final_attenuation_aux = final_attenuation_count

            while frame < last_frame:
                if markers[base_marker]['fcurves'][2, frame] < z_threshold:
                    window += 1
                    for following_frame in range(frame + 1, last_frame):
                        if markers[base_marker]['fcurves'][2, following_frame] < z_threshold:
                            window += 1
                        if following_frame == last_frame - 1 or markers[base_marker]['fcurves'][2, following_frame] >= z_threshold:
                            if window < frame_window_min_size:
                                # Ensure no marker dips under ground level
                                for window_frame in range(frame, frame + window):
                                    if markers[base_marker]['fcurves'][2, window_frame] < ground_level:
                                        markers[base_marker]['fcurves'][2, window_frame] = ground_level
                                        changed_frames.append(window_frame)
                                frame = following_frame
                                window = 0
                                break
                            else:
                                # Apply Z attenuation
                                for locking_frame in range(frame, frame + initial_attenuation_count):
                                    new_z = round(z_initial_attenuation(locking_frame - frame), 5)
                                    markers[base_marker]['fcurves'][2, locking_frame] = new_z
                                    changed_frames.append(locking_frame)

                                if following_frame == last_frame - 1:
                                    final_attenuation_aux = 0

                                for locking_frame in range(frame + initial_attenuation_count, frame + (window - final_attenuation_aux)):
                                    markers[base_marker]['fcurves'][2, locking_frame] = ground_level
                                    changed_frames.append(locking_frame)

                                for locking_frame in range(frame + (window - final_attenuation_aux), frame + window):
                                    new_z = round(z_final_attenuation(locking_frame - (frame + window - final_attenuation_aux)), 5)
                                    markers[base_marker]['fcurves'][2, locking_frame] = new_z
                                    changed_frames.append(locking_frame)
                                    
                                # XY Locking calculation for base markers during the flat part of the window
                                if lock_xy_at_ground_level:
                                    start_flat = frame + initial_attenuation_count
                                    end_flat = frame + (window - final_attenuation_aux)
                                    if end_flat > start_flat:
                                        target_m0 = foot_locking_markers[foot]['base'][0]
                                        target_m1 = foot_locking_markers[foot]['base'][1]
                                        
                                        avg_xy_0 = np.mean(markers[target_m0]['fcurves'][:2, start_flat:end_flat], axis=1)
                                        avg_xy_1 = np.mean(markers[target_m1]['fcurves'][:2, start_flat:end_flat], axis=1)

                                        # Enforce the global average distance proportionally on the calculated means
                                        if foot in avg_xy_dists:
                                            expected_dist = avg_xy_dists[foot]
                                            current_dist = np.linalg.norm(avg_xy_0 - avg_xy_1)
                                            if current_dist > 0.0001: # Avoid div by zero
                                                center = (avg_xy_0 + avg_xy_1) / 2.0
                                                dir0 = (avg_xy_0 - center)
                                                dir1 = (avg_xy_1 - center)
                                                
                                                avg_xy_0 = center + (dir0 / np.linalg.norm(dir0)) * (expected_dist / 2.0)
                                                avg_xy_1 = center + (dir1 / np.linalg.norm(dir1)) * (expected_dist / 2.0)
                                                
                                        # To apply this smoothly, we make local quadratic functions for XY matching the Z envelope
                                        for idx, mx in enumerate([target_m0, target_m1]):
                                            # We only process the mx which matches the current base_marker loop!
                                            if mx != base_marker:
                                                continue
                                                
                                            target_xy = avg_xy_0 if idx == 0 else avg_xy_1
                                            start_xy = markers[mx]['fcurves'][:2, frame]
                                            
                                            # If final attenuation doesn't exist (window touches end of sequence), use current target_xy
                                            end_xy = markers[mx]['fcurves'][:2, frame+window] if frame+window < last_frame else target_xy
                                            
                                            xy_initial_attn_X = quadratic_function(0, initial_attenuation_count/2, initial_attenuation_count-1, start_xy[0], start_xy[0] - (start_xy[0]-target_xy[0])*3/4, target_xy[0])
                                            xy_initial_attn_Y = quadratic_function(0, initial_attenuation_count/2, initial_attenuation_count-1, start_xy[1], start_xy[1] - (start_xy[1]-target_xy[1])*3/4, target_xy[1])
                                            
                                            if final_attenuation_aux > 0:
                                                xy_final_attn_X = quadratic_function(0, final_attenuation_aux/2, final_attenuation_aux-1, target_xy[0], target_xy[0] + (end_xy[0]-target_xy[0])*3/4, end_xy[0])
                                                xy_final_attn_Y = quadratic_function(0, final_attenuation_aux/2, final_attenuation_aux-1, target_xy[1], target_xy[1] + (end_xy[1]-target_xy[1])*3/4, end_xy[1])

                                            # Apply Attenuations to XY
                                            for locking_frame in range(frame, frame + initial_attenuation_count):
                                                markers[mx]['fcurves'][0, locking_frame] = xy_initial_attn_X(locking_frame - frame)
                                                markers[mx]['fcurves'][1, locking_frame] = xy_initial_attn_Y(locking_frame - frame)
                                            for locking_frame in range(frame + initial_attenuation_count, frame + (window - final_attenuation_aux)):
                                                markers[mx]['fcurves'][0, locking_frame] = target_xy[0]
                                                markers[mx]['fcurves'][1, locking_frame] = target_xy[1]
                                            if final_attenuation_aux > 0:
                                                for locking_frame in range(frame + (window - final_attenuation_aux), frame + window):
                                                    markers[mx]['fcurves'][0, locking_frame] = xy_final_attn_X(locking_frame - (frame + window - final_attenuation_aux))
                                                    markers[mx]['fcurves'][1, locking_frame] = xy_final_attn_Y(locking_frame - (frame + window - final_attenuation_aux))

                                frame = following_frame
                                window = 0
                                break
                frame += 1

        print(f"Foot.R median length:{BONE_DEFINITIONS['foot.R'].median}, foot.L median length:{BONE_DEFINITIONS['foot.L'].median}")
        
        # 3D Ankle Compensation Pass
        for changed_frame in list(set(changed_frames)):
            base_m0 = foot_locking_markers[foot]['base'][0]
            base_m1 = foot_locking_markers[foot]['base'][1]
            ankle_m = foot_locking_markers[foot]['ankle'][0]
            
            p_A = markers[base_m0]['fcurves'][:, changed_frame] # 3D vector
            p_B = markers[base_m1]['fcurves'][:, changed_frame] # 3D vector
            orig_ankle_pos = markers[ankle_m]['fcurves'][:, changed_frame].copy() # 3D vector
            
            bone_dist_A = BONE_DEFINITIONS[foot_locking_markers[foot]['bones'][0]].median
            bone_dist_B = BONE_DEFINITIONS[foot_locking_markers[foot]['bones'][1]].median
            
            initial_guess = orig_ankle_pos.copy()
            # Push initial guess Z lightly upwards just to give a better geometry solving start
            initial_guess[2] = max(initial_guess[2], max(p_A[2], p_B[2]) + 0.1)

            optimized_pos = gradient_descent_3d(
                error_function_3d,
                initial_guess,
                args=(p_A, p_B, bone_dist_A, bone_dist_B),
                learning_rate=0.0001,
                tolerance=1e-7,
                max_iterations=5000
            )

            markers[ankle_m]['fcurves'][:, changed_frame] = optimized_pos

            if any(c != 0 for c in knee_hip_compensation_coefficient):
                # Get the XYZ compensation delta, apply per-axis coefficients
                raw_delta = optimized_pos - orig_ankle_pos
                compensation_delta = np.array([
                    raw_delta[0] * knee_hip_compensation_coefficient[0],
                    raw_delta[1] * knee_hip_compensation_coefficient[1],
                    raw_delta[2] * knee_hip_compensation_coefficient[2],
                ])

                # Change the compensation markers' position directly without propagating to children
                for compensation_marker in foot_locking_markers[foot]['compensation_markers']:
                    markers[compensation_marker]['fcurves'][:, changed_frame] += compensation_delta
        
        overall_changed_frames += list(set(changed_frames))
        
        # We process upper body compensation after both feet loops have passed below

    # End of left/right foot loop!
    if compensate_upper_body:
        # Standard upper body Z offset via hips center logic
        for changed_frame in list(set(overall_changed_frames)):
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
            co = np.empty(2 * len(marker_data['fcurves'][axis_idx]), dtype=np.float32)
            co[0::2] = np.arange(len(marker_data['fcurves'][axis_idx]))  
            co[1::2] = marker_data['fcurves'][axis_idx]  
            fcurve.keyframe_points.foreach_set("co", co)
            fcurve.update()  

    scene.frame_current = scene.frame_current
