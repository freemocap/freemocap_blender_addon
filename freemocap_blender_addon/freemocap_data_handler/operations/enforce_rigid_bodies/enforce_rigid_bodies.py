from copy import deepcopy
from typing import Dict

import numpy as np

from freemocap_blender_addon.data_models.bones.bone_definitions import BoneDefinition, get_bone_definitions
from freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy
from .calculate_body_dimensions import calculate_body_dimensions
from ..enforce_rigid_bodies.calculate_bone_length_statistics import calculate_bone_length_statistics
from ...handler import FreemocapDataHandler


def enforce_rigid_bodies(handler: FreemocapDataHandler) -> FreemocapDataHandler:
    print(
        'Enforce "Rigid Bodies Assumption" by altering bone lengths to ensure they are the same length on each frame...')
    original_trajectories = handler.trajectories
    updated_trajectories = deepcopy(original_trajectories)
    mediapipe_heirarchy = get_mediapipe_hierarchy()

    bone_definition_template = get_bone_definitions()
    # Update the information of the virtual bones
    measured_bones = calculate_bone_length_statistics(trajectories=original_trajectories,
                                             bone_definitions=bone_definition_template)

    # Print the current bones length median, standard deviation and coefficient of variation
    log_bone_statistics(bones=measured_bones, type='measured')

    # Iterate through the lengths array of each bone and adjust the coordinates of the tail empty and its children so that the bone length is the same as the median

    for name, bone in measured_bones.items():
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
            bone_vector_norm = bone_vector / raw_length

            # Calculate the new tail position delta by multiplying the normalized bone vector by the difference of desired_length and original_length
            position_delta = bone_vector_norm * (desired_length - raw_length)

            updated_trajectories = translate_trajectory_and_its_children(name=tail_name,
                                                                         position_delta=position_delta,
                                                                         frame_number=frame_number,
                                                                         updated_trajectories=updated_trajectories,
                                                                         hierarchy=mediapipe_heirarchy)

    print('Bone lengths enforced successfully!')

    # Update the information of the virtual bones
    updated_bones = calculate_bone_length_statistics(trajectories=updated_trajectories, bone_definitions=measured_bones)

    # Print the current bones length median, standard deviation and coefficient of variation
    log_bone_statistics(bones=updated_bones, type='updated')

    print('Updating freemocap data handler with the new trajectories...')
    for name, trajectory in updated_trajectories.items():
        handler.set_trajectory(name=name, data=trajectory)

    handler.mark_processing_stage(name='enforced_rigid_bones',
                                  metadata={"rigid_bone_data": updated_bones,
                                            "measured_bone_data": measured_bones,
                                            "body_dimensions": calculate_body_dimensions(bones_info=updated_bones),
                                            "skeleton_hierarchy": get_mediapipe_hierarchy()},
                                  )
    return handler


def translate_trajectory_and_its_children(name: str,
                                          position_delta: np.ndarray,
                                          frame_number: int,
                                          updated_trajectories: Dict[str, np.ndarray],
                                          hierarchy: Dict[str, Dict[str, str]]) -> Dict[str, np.ndarray]:
    # recursively translate the tail empty and its children by the position delta.
    try:
        updated_trajectories[name][frame_number, :] = updated_trajectories[name][frame_number, :] + position_delta

        if name in hierarchy.keys():
            for child_name in hierarchy[name]['children']:
                translate_trajectory_and_its_children(name=child_name,
                                                      position_delta=position_delta,
                                                      frame_number=frame_number,
                                                      updated_trajectories=updated_trajectories,
                                                      hierarchy=hierarchy)
    except Exception as e:
        print(f"Error while adjusting trajectory `{name}` and its children:\n error:\n {e}")
        print(e)
        raise Exception(f"Error while adjusting trajectory and its children: {e}")

    return updated_trajectories


def log_bone_statistics(bones: Dict[str, BoneDefinition], type: str):
    log_string = f'\n\n[{type}] Bone Length Statistics:\n'
    header_string = f"{'BONE':<15} {'MEDIAN (cm)':>12} {'MAD (cm)':>12}  {'MEAN':>12} {'STDEV (cm)':>12} {'CV_STD (%)':>12} {'CV_MAD (%)':>12}"
    log_string += header_string + '\n'
    for name, bone in bones.items():
        # Get the statistic values
        median_string = str(round(bone.median * 100, 7))
        mad_string = str(round(bone.median_absolute_deviation * 100, 7))
        mean_string = str(round(bone.mean * 100, 7))
        stdev_string = str(round(bone.standard_deviation * 100, 7))
        cv_std_string = str(round(bone.coefficient_of_variation_std * 100, 7))
        cv_mad_string = str(round(bone.coefficient_of_variation_mad * 100, 7))

        log_string += f"{name:<15} {median_string:>12}  {mad_string:>12} {mean_string:>12} {stdev_string:>12} {cv_std_string:>12} {cv_mad_string:>12}\n"

    print(log_string)

