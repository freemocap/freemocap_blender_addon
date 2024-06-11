from copy import deepcopy
from typing import Tuple

import numpy as np

from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_segment_lengths import \
    calculate_segment_lengths, print_length_stats
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories, SegmentStats


def calculate_rigid_body_trajectories(keypoint_trajectories: KeypointTrajectories,
                                      skeleton_definition: SkeletonTypes) -> Tuple[KeypointTrajectories, SegmentStats]:
    print(
        'Enforce "Rigid Bodies Assumption" by altering bone lengths to ensure they are the same length on each frame...')

    # Update the information of the virtual bones
    og_segment_length_stats = calculate_segment_lengths(keypoint_trajectories=keypoint_trajectories,
                                                        skeleton_definition=skeleton_definition)
    print("Original body segment lengths 👇")
    print_length_stats(segment_lengths=og_segment_length_stats)
    print("Original body segment lengths 👆")

    rigidified_keypoints = rigidify_keypoint_trajectories(keypoint_trajectories=deepcopy(keypoint_trajectories),
                                                          segment_length_stats=og_segment_length_stats,
                                                          skeleton_definition=skeleton_definition)
    rigidified_segment_length_stats = calculate_segment_lengths(keypoint_trajectories=rigidified_keypoints,
                                                                skeleton_definition=skeleton_definition)
    print("Rigidified body segment lengths 👇")
    print_length_stats(segment_lengths=rigidified_segment_length_stats)
    print("Rigidified body segment lengths 👆")
    return rigidified_keypoints, og_segment_length_stats


def rigidify_keypoint_trajectories(keypoint_trajectories: KeypointTrajectories,
                                   segment_length_stats: SegmentStats,
                                   skeleton_definition: SkeletonTypes) -> KeypointTrajectories:
    # Iterate through the skeleton segments and enforce rigid body assumption by translating each child-keypoint
    # and its children so the new bone length is the same as the target length on each frame
    skeleton_segments = skeleton_definition.value.get_segments()

    for segment in skeleton_segments:
        segment_name = segment.name.lower()

        print(f"Enforcing rigid length for segment: {segment_name}...")
        if segment_name not in segment_length_stats:
            raise ValueError(f"Segment {segment_name} not found in segment lengths")

        target_length = segment_length_stats[segment_name].median
        raw_lengths = segment_length_stats[segment_name].samples

        # TODO - support compound segments with multiple children
        segment_parent_kp_name = segment.value.parent.name.lower()
        segment_child_kp_name = segment.value.child.name.lower()
        parent_trajectory = keypoint_trajectories[segment_parent_kp_name].trajectory_data
        child_trajectory = keypoint_trajectories[segment_child_kp_name].trajectory_data

        # calculate the child trajectory relative to the parent trajectory
        # (i.e. set the parent trajectory as the origin and the child trajectory as the relative position)
        child_trajectory_zeroed = child_trajectory - parent_trajectory

        # calculate the necessary scaling factors to make the child trajectory the same length as the target length
        scaling_factors = (target_length / raw_lengths) - 1

        # calculate necessary translations on each frame to make the child trajectory the same length as the target length
        translations = child_trajectory_zeroed * scaling_factors[:, np.newaxis]
        keypoint_trajectories[segment_child_kp_name].trajectory_data += translations

        # translate all child keypoints of the segment
        children = skeleton_definition.value.get_keypoint_children(keypoint_name=segment_child_kp_name)
        if len(children) == 0:
            f=9
        for child_keypoint in children:
            child_name = child_keypoint.name.lower()
            child_keypoint = keypoint_trajectories[child_name]
            child_keypoint.trajectory_data += translations
    return keypoint_trajectories


if __name__ == "__main__":
    from freemocap_blender_addon.freemocap_data.freemocap_recording_data import load_freemocap_rest_recording

    recording_data = load_freemocap_rest_recording()
    keypoint_trajectories_outer = recording_data.body.map_to_keypoints()
    keypoint_trajectories, og_segment_lengths = calculate_rigid_body_trajectories(
        keypoint_trajectories=keypoint_trajectories_outer,
        skeleton_definition=SkeletonTypes.BODY_ONLY)
