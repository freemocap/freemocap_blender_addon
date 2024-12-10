from copy import deepcopy
from typing import Dict

import numpy as np

from freemocap_blender_addon.data_models.bones.bone_definitions import get_bone_definitions
from freemocap_blender_addon.data_models.bones.bone_definition_models import BoneDefinition, BoneStatistics
from freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy
from .calculate_body_dimensions import calculate_body_dimensions
from ..enforce_rigid_bodies.calculate_bone_length_statistics import calculate_bone_length_statistics
from ...handler import FreemocapDataHandler


def print_bone_stats(bone_stats:  Dict[str, BoneStatistics]) -> None:
    print('Bone Length Statistics:')
    csv_header = ""
    csv_data = ""
    for bone_name, bone_stats in bone_stats.items():
        if not csv_header:
            csv_header  = bone_stats.as_fixed_width_string_header()
        csv_data += bone_stats.as_fixed_width_string() + "\n"
    print(csv_header)
    print(csv_data)


def enforce_rigid_bodies(handler: FreemocapDataHandler) -> FreemocapDataHandler:
    print(
        'Enforce "Rigid Bodies Assumption" by altering bone lengths to ensure they are the same length on each frame...')
    original_trajectories = handler.trajectories
    updated_trajectories = deepcopy(original_trajectories)
    mediapipe_heirarchy = get_mediapipe_hierarchy()

    bone_definition_template: Dict[str, BoneDefinition] = get_bone_definitions()

    # Update the information of the virtual bones
    measured_bone_stats = calculate_bone_length_statistics(trajectories=original_trajectories,
                                                           bone_definitions=bone_definition_template)

    print(f'Measured Bone Length Stats: \n\n {print_bone_stats(measured_bone_stats)}')

    # Iterate through the lengths array of each bone and adjust the coordinates of the tail empty and its children so that the bone length is the same as the median

    for name, bone in measured_bone_stats.items():
        desired_length = bone.median

        bone_head = bone.definition.head
        bone_tail = bone.definition.tail
        print(f"Enforcing rigid length for bone: {name} (head: {bone_head}, tail: {bone_tail}) to {desired_length}m...")

        for frame_number, raw_length in enumerate(bone.lengths):
            if np.isnan(raw_length) or raw_length == 0:
                continue

            head_position = original_trajectories[bone_head][frame_number, :]
            tail_position = original_trajectories[bone_tail][frame_number, :]

            bone_vector = tail_position - head_position

            # Get the normalized bone vector by dividing the bone_vector by its length
            bone_vector_norm = bone_vector / raw_length

            # Calculate the new tail position delta by multiplying the normalized bone vector by the difference of desired_length and original_length
            position_delta = bone_vector_norm * (desired_length - raw_length)

            updated_trajectories = translate_trajectory_and_its_children(name=bone_tail,
                                                                         position_delta=position_delta,
                                                                         frame_number=frame_number,
                                                                         updated_trajectories=updated_trajectories,
                                                                         hierarchy=mediapipe_heirarchy)



    # Update the handler with the updated trajectories
    for name, trajectory in updated_trajectories.items():
        handler.set_trajectory(name=name, data=trajectory)

    # Update the information of the virtual bones
    rigid_bone_stats = calculate_bone_length_statistics(trajectories=updated_trajectories,
                                                        bone_definitions=bone_definition_template)

    print(f'Updated Bone Length Stats: \n\n {print_bone_stats(rigid_bone_stats)}')
    print('Bone lengths enforced successfully!')


    handler.mark_processing_stage(name='enforced_rigid_bones',
                                  metadata={"bone_statistics": {'measured': {bone_name: bone.as_dict() for bone_name, bone in measured_bone_stats.items()},
                                                                'rigid': {bone_name: bone.as_dict() for bone_name, bone in rigid_bone_stats.items()}},
                                            "body_dimensions": calculate_body_dimensions(bone_stats=rigid_bone_stats),
                                            "skeleton_hierarchy": mediapipe_heirarchy},
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
