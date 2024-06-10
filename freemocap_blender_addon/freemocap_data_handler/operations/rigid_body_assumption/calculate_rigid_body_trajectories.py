from typing import Dict

import numpy as np

from freemocap_blender_addon.freemocap_data.freemocap_data_component import GenericTrackedPoints
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.skeleton_abc import SkeletonABC
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories
from ..rigid_body_assumption.calculate_segment_lengths import calculate_segment_lengths


def calculate_rigid_body_trajectories(og_keypoint_trajectories: KeypointTrajectories,
                                      skeleton_definition: SkeletonTypes) -> KeypointTrajectories:
    print(
        'Enforce "Rigid Bodies Assumption" by altering bone lengths to ensure they are the same length on each frame...')

    # Update the information of the virtual bones
    og_segment_lengths = calculate_segment_lengths(keypoint_trajectories=og_keypoint_trajectories,
                                                   skeleton_definition=skeleton_definition)

    # Print the current bones length median, standard deviation and coefficient of variation
    log_bone_statistics(bones=og_segment_lengths, type='original')

    # Iterate through the lengths array of each bone and check if the length is outside the interval defined by x*stdev with x as a factor
    # If the bone length is outside the interval, adjust the coordinates of the tail empty and its children so the new bone length is at the border of the interval

    for name, bone in og_segment_lengths.items():
        print(f"Enforcing rigid length for bone: {name}...")

        desired_length = bone.median

        head_name = bone.head
        tail_name = bone.tail

        for frame_number, raw_length in enumerate(bone.lengths):
            if np.isnan(raw_length) or raw_length == 0:
                continue

            head_position = original_trajectories[head_name][frame_number, :]
            tail_position = original_trajectories[tail_name][frame_number, :]

            bone_vector = tail_position - head_position

            # Get the normalized bone vector by dividing the bone_vector by its length
            try:
                bone_vector_norm = bone_vector / raw_length
            except ZeroDivisionError:
                raw_length = 0.0001
                bone_vector_norm = bone_vector / raw_length

            # Calculate the new tail position delta by multiplying the normalized bone vector by the difference of desired_length and original_length
            position_delta = bone_vector_norm * (desired_length - raw_length)

            updated_trajectories = translate_trajectory_and_its_children(name=tail_name,
                                                                         position_delta=position_delta,
                                                                         frame_number=frame_number,
                                                                         updated_trajectories=updated_trajectories)

    print('Bone lengths enforced successfully!')

    # Update the information of the virtual bones
    updated_bones = calculate_segment_lengths(trajectories=updated_trajectories, bone_definitions=og_segment_lengths)

    # Print the current bones length median, standard deviation and coefficient of variation
    log_bone_statistics(bones=updated_bones, type='updated')

    print('Updating freemocap data handler with the new trajectories...')
    for name, trajectory in updated_trajectories.items():
        handler.set_trajectory(name=name, data=trajectory)

    return handler


def translate_trajectory_and_its_children(name: str,
                                          position_delta: np.ndarray,
                                          frame_number: int,
                                          updated_trajectories: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    # recursively translate the tail empty and its children by the position delta.
    try:
        updated_trajectories[name][frame_number, :] = updated_trajectories[name][frame_number, :] + position_delta

        if name in MEDIAPIPE_HIERARCHY.keys():
            for child_name in MEDIAPIPE_HIERARCHY[name]['children']:
                translate_trajectory_and_its_children(name=child_name,
                                                      position_delta=position_delta,
                                                      frame_number=frame_number,
                                                      updated_trajectories=updated_trajectories)
    except Exception as e:
        print(f"Error while adjusting trajectory `{name}` and its children:\n error:\n {e}")
        print(e)
        raise Exception(f"Error while adjusting trajectory and its children: {e}")

    return updated_trajectories


def log_bone_statistics(bones: Dict[str, BoneDefinition], type: str):
    log_string = f'\n\n[{type}] Bone Length Statistics:\n'
    header_string = f"{'BONE':<15} {'MEDIAN (cm)':>12} {'STDEV (cm)':>12} {'CV (%)':>12}"
    log_string += header_string + '\n'
    for name, bone in bones.items():
        # Get the statistic values
        median_string = str(round(bone.median * 100, 7))
        stdev_string = str(round(bone.stddev * 100, 7))
        try:
            cv_string = str(round(bone.stddev / bone.median * 100, 4))
        except ZeroDivisionError:
            cv_string = 'N/A'
        log_string += f"{name:<15} {median_string:>12} {stdev_string:>12} {cv_string:>12}\n"

    print(log_string)
