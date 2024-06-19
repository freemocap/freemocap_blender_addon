import numpy as np
from skelly_blender.core.custom_types import Trajectories, SegmentStats

from skelly_blender.core.pure_python.freemocap_data.freemocap_recording_data import load_freemocap_test_recording
from skelly_blender.core.pure_python.skeleton_model.skeleton_types import SkeletonTypes
from skelly_blender.core.pure_python.utility_classes.sample_statistics import DescriptiveStatistics
from skelly_blender.system.print_table_from_dicts import print_table


def calculate_segment_length_stats(keypoint_trajectories: Trajectories,
                                   skeleton_definition: SkeletonTypes) -> SegmentStats:
    segment_stats = {}
    segments = skeleton_definition.value.get_segments()
    for segment in segments:
        parent_name = segment.value.parent.name.lower()
        child_name = segment.value.child.name.lower()
        print(f"Calculating segment length for {segment.name} as distance between keypoints - `{parent_name}` and `{child_name}`")
        length_stats = calculate_distance_between_trajectories(
            trajectory_1=keypoint_trajectories[parent_name].trajectory_data,
            trajectory_2=keypoint_trajectories[child_name].trajectory_data
        )

        segment_stats[segment.name.lower()] = DescriptiveStatistics.from_samples(length_stats)

    return segment_stats


def calculate_distance_between_trajectories(trajectory_1: np.ndarray,
                                            trajectory_2: np.ndarray) -> np.ndarray:
    """
    Compute the Euclidean distances between corresponding entries of two 3D trajectories.

    Parameters
    ----------
    trajecotry_1 : np.ndarray
        The first trajectory, a 2D array of shape (n, 3) where n is the number of points.
    trajecotry_2 : np.ndarray
        The second trajectory, a 2D array of shape (n, 3) where n is the number of points.

    Returns
    -------
    np.ndarray
        A 1D array of length n containing the distances between corresponding points in the two trajectories.

    Raises
    ------
    ValueError
        If the input arrays do not have the same shape.

    Examples
    --------
    >>> trajecotry_1 = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    >>> trajecotry_2 = np.array([[1, 0, 0], [0, 1, 1], [2, 3, 2]])
    >>> calculate_distance_between_trajectories(trajecotry_1, trajecotry_2) # Expected output: array([1, 1.41421356, 1])
    """
    if trajectory_1.shape != trajectory_2.shape:
        raise ValueError(
            f"Both trajectories must have the same shape, Trajectory 1 shape: {trajectory_1.shape}, Trajectory 2 shape: {trajectory_2.shape}")
    if np.sum(np.isnan(trajectory_1)) == trajectory_1.size:
        raise ValueError("Trajectory 1 is all NaN")
    if np.sum(np.isnan(trajectory_2)) == trajectory_2.size:
        raise ValueError("Trajectory 2 is all NaN")


    distances =  np.linalg.norm(trajectory_1 - trajectory_2, axis=1)
    if distances.shape[0] != trajectory_1.shape[0]:
        raise ValueError(
            f"Distances array shape {distances.shape} does not match trajectory shape {trajectory_1.shape}")
    if all(np.isnan(distances)):
        raise ValueError("All distances are NaN")
    if all(np.isinf(distances)):
        raise ValueError("All distances are infinite")
    return distances


def print_length_stats_table(segment_lengths: SegmentStats, squash_less_than=1e-3):
    stats = []
    for name, segment in segment_lengths.items():
        segment_dict = {'segment': name}
        segment_dict.update(segment.to_dict())
        for key in list(segment_dict.keys()):
            if not isinstance(segment_dict[key], str) and segment_dict[key] < squash_less_than:
                segment_dict[key] = 0.0
        stats.append(segment_dict)
    print_table(stats)


if __name__ == "__main__":

    recording_data = load_freemocap_test_recording()
    keypoint_trajectories_outer = recording_data.body.map_to_keypoints()
    segment_lengths = calculate_segment_length_stats(keypoint_trajectories=keypoint_trajectories_outer,
                                                     skeleton_definition=SkeletonTypes.BODY_ONLY)

    print_length_stats_table(segment_lengths)
