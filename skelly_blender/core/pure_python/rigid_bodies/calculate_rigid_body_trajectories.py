from copy import deepcopy
from typing import Tuple

import numpy as np

from skelly_blender.core.pure_python.generic_type_hints import KeypointTrajectories, RigidSegmentDefinitions, SegmentStats
from skelly_blender.core.pure_python.rigid_bodies.calculate_segment_lengths import calculate_segment_length_stats, \
    print_length_stats_table
from skelly_blender.core.pure_python.rigid_bodies.rigid_segment_definition import RigidSegmentDefinition
from skelly_blender.core.pure_python.skeleton_model.skeleton_types import SkeletonTypes


def calculate_rigid_body_trajectories(keypoint_trajectories: KeypointTrajectories,
                                      skeleton_definition: SkeletonTypes,
                                      scale: float = 0.001) -> Tuple[
    KeypointTrajectories, RigidSegmentDefinitions]:
    print(
        'Enforce "Rigid Bodies Assumption" by altering bone lengths to ensure they are the same length on each frame...')

    # Update the information of the virtual bones
    og_segment_length_stats = calculate_segment_length_stats(keypoint_trajectories=keypoint_trajectories,
                                                             skeleton_definition=skeleton_definition)
    print("Original body segment lengths 👇")
    print_length_stats_table(segment_lengths=og_segment_length_stats)
    print("Original body segment lengths 👆")

    rigidified_keypoints = rigidify_keypoint_trajectories(keypoint_trajectories=deepcopy(keypoint_trajectories),
                                                          segment_length_stats=og_segment_length_stats,
                                                          skeleton_definition=skeleton_definition)
    rigidified_segment_length_stats = calculate_segment_length_stats(keypoint_trajectories=rigidified_keypoints,
                                                                     skeleton_definition=skeleton_definition)

    rigid_segment_definitions = {segment.name.lower(): RigidSegmentDefinition(name=segment.name.lower(),
                                                                              length=rigidified_segment_length_stats[
                                                                                         segment.name.lower()].median * scale,
                                                                              parent=segment.value.parent.name.lower(),
                                                                              child=segment.value.child.name.lower()
                                                                              )
                                 for segment in skeleton_definition.value.get_segments()}

    print("Rigidified body segment lengths 👇")
    print_length_stats_table(segment_lengths=rigidified_segment_length_stats)
    print("Rigidified body segment lengths 👆")

    return rigidified_keypoints, rigid_segment_definitions


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
        for child_keypoint in children:
            child_name = child_keypoint.name.lower()
            child_keypoint = keypoint_trajectories[child_name]
            child_keypoint.trajectory_data += translations

        for name, trajectory in keypoint_trajectories.items():
            if np.sum(np.isnan(trajectory.trajectory_data)) == trajectory.trajectory_data.size:
                raise ValueError(f"Trajectory {name} is all NaN")

    return keypoint_trajectories


if __name__ == "__main__":
    from skelly_blender.core.pure_python.load_data.freemocap_recording_data import load_freemocap_test_recording
    recording_data = load_freemocap_test_recording()
    keypoint_trajectories_outer = recording_data.body.map_to_keypoints()
    keypoint_trajectories, og_segment_lengths = calculate_rigid_body_trajectories(
        keypoint_trajectories=keypoint_trajectories_outer,
        skeleton_definition=SkeletonTypes.BODY_ONLY)
