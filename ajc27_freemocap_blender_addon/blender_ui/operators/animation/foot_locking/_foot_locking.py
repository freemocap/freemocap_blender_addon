import bpy
import numpy as np
import math

from ajc27_freemocap_blender_addon.data_models.bones.bone_definitions import get_bone_definitions
from ajc27_freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy

from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.foot_locking_markers import foot_locking_markers
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.helpers.basic_functions import translate_marker, quadratic_function, error_function
from ajc27_freemocap_blender_addon.blender_ui.operators.animation.foot_locking.helpers.minimize_functions import gradient_descent_central

MEDIAPIPE_HIERARCHY = get_mediapipe_hierarchy()

class FREEMOCAP_OT_foot_locking(bpy.types.Operator):
    bl_idname = 'freemocap._foot_locking'
    bl_label = 'Foot Locking'
    bl_description = "Foot Locking"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Applying Foot Locking.......")

        scene = context.scene
        props = context.scene.freemocap_ui_properties.foot_locking_properties

        #  Get the bone definitions
        BONE_DEFINITIONS = get_bone_definitions()

        # Prepare the target foot list
        if props.target_foot == 'both_feet':
            target_foot_list = ['left_foot', 'right_foot']
        else:
            target_foot_list = [props.target_foot]

        # Prepare the target base markers
        if props.target_base_markers == 'foot_index_and_heel':
            target_base_markers_list = ['foot_index', 'heel']
        else:
            target_base_markers_list = [props.target_base_markers]

        z_threshold = props.z_threshold
        ground_level = props.ground_level
        frame_window_min_size = props.frame_window_min_size
        initial_attenuation_count = props.initial_attenuation_count
        final_attenuation_count = props.final_attenuation_count
        lock_xy_at_ground_level = props.lock_xy_at_ground_level
        knee_hip_compensation_coefficient = props.knee_hip_compensation_coefficient
        compensate_upper_body = props.compensate_upper_body

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
                
                        # Save the marker object and its position fcurves in the dictionary
                        markers[marker.name] = {
                            'object': marker,
                            'fcurves': fcurve_data,
                        }

        # Get the scene start and end frames
        start_frame = scene.frame_start
        end_frame = scene.frame_end

        # Get the relative last frame
        last_frame = end_frame - start_frame

        # Define the attenuation functions
        initial_attenuation = quadratic_function(
            x1=0,
            x2=(initial_attenuation_count / 2),
            x3=(initial_attenuation_count - 1),
            y1=z_threshold,
            y2=z_threshold - (z_threshold - ground_level) * 3 / 4,
            y3=ground_level)
        
        final_attenuation = quadratic_function(
            x1=0,
            x2=(final_attenuation_count / 2),
            x3=(final_attenuation_count - 1),
            y1=ground_level,
            y2=ground_level + (z_threshold - ground_level) * 3 / 4,
            y3=z_threshold)

        # Set the overall_changed_frames variable to save all the frames
        # that were changed for posterior upper body adjustment
        overall_changed_frames = []

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

            # Variable to save the changed frames for later ankle adjustment
            changed_frames = []

            for base_marker in foot_locking_markers[foot]['base']:
                if base_marker not in [foot.split('_')[0] + '_' + marker for marker in target_base_markers_list]:
                    continue

                # Set the initial variables
                frame = 0 # relative frame
                window = 0
                final_attenuation_aux = final_attenuation_count

                # Iterate through the animation frames
                while frame < last_frame:

                    if markers[base_marker]['fcurves'][2, frame] < z_threshold:
                        # Marker is under threshold the next frames are checked to conform the window
                        window += 1

                        for following_frame in range(frame + 1, last_frame):
                            if markers[base_marker]['fcurves'][2, following_frame] < z_threshold:
                                # Following marker is under threshold, the window is increased
                                window += 1
                            if following_frame == last_frame - 1 or markers[base_marker]['fcurves'][2, following_frame] >= z_threshold:
                                # Following marker is the last one or is not under threshold, the window size is checked
                                if window < frame_window_min_size:
                                    # Window is not big enough. Break the cycle and continue from the frame that was over threshold
                                    # Before continuing, make sure that no marker is below the ground level
                                    for window_frame in range(frame, frame + window):
                                        if markers[base_marker]['fcurves'][2, start_frame + window_frame] < ground_level:
                                            # Marker's z position is forced to the ground level
                                            markers[base_marker]['fcurves'][2, start_frame + window_frame] = ground_level
                                            # Add the frame to the list of changed frames
                                            changed_frames.append(start_frame + window_frame)

                                    frame = following_frame
                                    window = 0
                                    break

                                else:
                                    # Window is big enough so the locking logic is applied
                                    # Initial attenuation is applied
                                    for locking_frame in range(frame, frame + initial_attenuation_count):
                                        # Get the z position from the initial attenuation function
                                        new_z_position = round(initial_attenuation(locking_frame - frame), 5)
                                        # Change the marker's z position
                                        markers[base_marker]['fcurves'][2, start_frame + locking_frame] = new_z_position
                                        # Add the frame to the list of changed frames
                                        changed_frames.append(start_frame + locking_frame)

                                    # Check if the window ends at the last frame. If so the final attenuation aux variable is set to zero
                                    if following_frame == last_frame - 1:
                                        final_attenuation_aux = 0

                                    # For the frames between the initial attenuation and the final attenuation the z position is set to the ground level
                                    for locking_frame in range(frame + initial_attenuation_count, frame + (window - final_attenuation_aux)):
                                        markers[base_marker]['fcurves'][2, start_frame + locking_frame] = ground_level
                                        # Add the frame to the list of changed frames
                                        changed_frames.append(start_frame + locking_frame)

                                    # Final attenuation is applied if final_attenuation_count is greater than zero
                                    for locking_frame in range(frame + (window - final_attenuation_aux), frame + window):
                                        # Get the z position from the final attenuation function
                                        new_z_position = round(final_attenuation(locking_frame - (frame + window - final_attenuation_aux)), 5)
                                        # Change the marker's z position
                                        markers[base_marker]['fcurves'][2, start_frame + locking_frame] = new_z_position
                                        # Add the frame to the list of changed frames
                                        changed_frames.append(start_frame + locking_frame)

                                    frame = following_frame
                                    window = 0
                                    break

                    frame += 1

            print(f"Foot.R median length:{BONE_DEFINITIONS['heel.02.L'].median}, foot.L median length:{BONE_DEFINITIONS['foot.L'].median}")
            # Adjust the ankle marker position in the previous modified frames so the median
            # ankle-foot_index and ankle-heel distances are equal to the median lengths before the change
            for changed_frame in list(set(changed_frames)):
                # Get the initial position variables of the ankle z position's optimization problem
                base_marker_0_x = markers[foot_locking_markers[foot]['base'][0]]['fcurves'][0, changed_frame]
                base_marker_0_y = markers[foot_locking_markers[foot]['base'][0]]['fcurves'][1, changed_frame]
                base_marker_0_z = markers[foot_locking_markers[foot]['base'][0]]['fcurves'][2, changed_frame]
                base_marker_1_x = markers[foot_locking_markers[foot]['base'][1]]['fcurves'][0, changed_frame]
                base_marker_1_y = markers[foot_locking_markers[foot]['base'][1]]['fcurves'][1, changed_frame]
                base_marker_1_z = markers[foot_locking_markers[foot]['base'][1]]['fcurves'][2, changed_frame]
                ankle_marker_x = markers[foot_locking_markers[foot]['ankle'][0]]['fcurves'][0, changed_frame]
                ankle_marker_y = markers[foot_locking_markers[foot]['ankle'][0]]['fcurves'][1, changed_frame]

                base_bone_0_distance = BONE_DEFINITIONS[foot_locking_markers[foot]['bones'][0]].median
                base_bone_1_distance = BONE_DEFINITIONS[foot_locking_markers[foot]['bones'][1]].median

                #  Get the current ankle z position
                current_ankle_pos = markers[foot_locking_markers[foot]['ankle'][0]]['fcurves'][2, changed_frame]

                # Set the initial ankle z guess as the actual ankle z
                # position. If the initial ankle z guess is not higher than
                # both of the base markers z positions then set the initial
                # ankle z guess to the highest base marker z position plus
                # a margin
                initial_ankle_z_guess = max(
                    current_ankle_pos,
                    max([base_marker_0_z,base_marker_1_z]) + 0.1
                )

                gdc_optimized_ankle_z = gradient_descent_central(
                    error_function,
                    initial_ankle_z_guess,
                    args=(ankle_marker_x,
                        ankle_marker_y,
                        base_marker_0_x,
                        base_marker_0_y,
                        base_marker_0_z,
                        base_marker_1_x,
                        base_marker_1_y,
                        base_marker_1_z,
                        base_bone_0_distance,
                        base_bone_1_distance),
                    learning_rate=0.0001,
                    tolerance=1e-7,
                    max_iterations=5000
                )

                optimized_ankle_z = gdc_optimized_ankle_z

                # Set the new ankle z position
                markers[foot_locking_markers[foot]['ankle'][0]]['fcurves'][2, changed_frame] = optimized_ankle_z

                if knee_hip_compensation_coefficient != 0:
                    compensation_z = optimized_ankle_z - current_ankle_pos

                    # Change the compensation markers' z position
                    for compensation_marker in foot_locking_markers[foot]['compensation_markers']:
                        marker_z_position = markers[compensation_marker]['fcurves'][2, changed_frame]
                        markers[compensation_marker]['fcurves'][2, changed_frame] = marker_z_position + compensation_z * knee_hip_compensation_coefficient

            # Update the overall_changed_frames list
            overall_changed_frames += list(set(changed_frames))

            if compensate_upper_body:
                # Compensate the upper body markers starting from the hips_center

                # Iterate through the overall_changed_frames list
                for changed_frame in list(set(overall_changed_frames)):
                    # Get the new hips_center z coordinate as the average of the
                    # left and right hip z coordinates
                    new_hips_center_z = (
                        markers['left_hip']['fcurves'][2, changed_frame - start_frame]
                        + markers['right_hip']['fcurves'][2, changed_frame - start_frame]
                        ) / 2
                    
                    # Get the z delta to translate later the rest of the markers chain
                    delta_list = [
                        0,
                        0,
                        new_hips_center_z - markers['hips_center']['fcurves'][2, changed_frame - start_frame]
                    ]

                    # Set the new hips_center z position
                    markers['hips_center']['fcurves'][2, changed_frame - start_frame] = new_hips_center_z

                    # Translate the rest of the upper body markers starting from the trunk_center
                    translate_marker(
                        MEDIAPIPE_HIERARCHY,
                        markers,
                        'trunk_center',
                        delta_list,
                        changed_frame - start_frame,
                    )

        # Write the markers dictionary fcurve data to the objects fcurves
        for marker_name, marker_data in markers.items():
            for axis_idx in range(3):
                fcurve = marker_data['object'].animation_data.action.fcurves.find("location", index=axis_idx)

                # Create a flattened array of [frame0, value0, frame1, value1, ...]
                co = np.empty(2 * len(marker_data['fcurves'][axis_idx]), dtype=np.float32)
                co[0::2] = np.arange(len(marker_data['fcurves'][axis_idx]))  # Frame numbers
                co[1::2] = marker_data['fcurves'][axis_idx]  # Axis values

                # Assign all keyframes at once
                fcurve.keyframe_points.foreach_set("co", co)
                fcurve.update()  # Finalize changes

        # Set the scene frame as the current frame just to update the viewport
        scene.frame_current = scene.frame_current

        return {'FINISHED'}

