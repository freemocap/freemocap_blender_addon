import math
from typing import Dict

import numpy as np


def estimate_good_frame(trajectories_with_error: Dict[str, np.ndarray],
                        velocity_threshold: float = 0.1,
                        ignore_first_n_frames: int = 30):
    trajectory_names = list(trajectories_with_error.keys())
    all_good_frames = None
    all_velocities = {}
    all_errors = {}

    for trajectory_name in trajectory_names:
        trajectory_velocity_frame_xyz = np.diff(trajectories_with_error[trajectory_name]['trajectory'], axis=0)
        trajectory_velocity_frame_xyz = np.insert(trajectory_velocity_frame_xyz, 0, np.nan, axis=0)
        trajectory_velocity_frame_magnitude = np.sqrt(np.sum(trajectory_velocity_frame_xyz ** 2, axis=1))
        all_velocities[trajectory_name] = trajectory_velocity_frame_magnitude

        trajectory_reprojection_error = trajectories_with_error[trajectory_name]['error']
        all_errors[trajectory_name] = trajectory_reprojection_error

        # define threshold for 'standing still'
        velocity_threshold = np.nanpercentile(trajectory_velocity_frame_magnitude,
                                              q=velocity_threshold * 100)

        # Get the indices of the good frames
        velocity_above_threshold = [index for index, velocity in enumerate(trajectory_velocity_frame_magnitude) if
                                    velocity > velocity_threshold]
        reprojection_error_not_nan = [index for index, error in enumerate(trajectory_reprojection_error) if
                                      not math.isnan(error)]
        floating_point_error = math.ulp(
            1.0) * 10  # 10 times the floating point error, any velocity below this is considered zero
        velocity_not_zero = [index for index, velocity in enumerate(trajectory_velocity_frame_magnitude) if
                             velocity > floating_point_error]

        # To get the good_frames_indices, we need the intersection of the other three lists:
        good_frames_indices = list(
            set(velocity_above_threshold) & set(reprojection_error_not_nan) & set(velocity_not_zero))

        # If no good frames found, skip this trajectory
        if len(good_frames_indices) == 0:
            continue

        # intersect good_frames_indices with all_good_frames
        if all_good_frames is None:
            all_good_frames = set(good_frames_indices)
        else:
            all_good_frames = all_good_frames.intersection(set(good_frames_indices))

    # If no good frames found in any trajectory, raise an Exception
    if  all_good_frames is None:
        raise Exception("No good frames found! Please check your data.")

    # Convert the set to a list
    all_good_frames = list(all_good_frames)

    all_velocities_on_good_frames = np.array([all_velocities[name][all_good_frames] for name in trajectory_names])
    mean_velocities_on_good_frames = np.mean(all_velocities_on_good_frames, axis=0)
    # reprojection_errors_on_good_frames = np.array([all_errors[name][all_good_frames] for name in trajectory_names])

    # normalize the values by their minimum (best) value
    good_frames_velocities_normalized = all_velocities_on_good_frames / np.min(all_velocities_on_good_frames)
    # good_frames_errors_normalized = reprojection_errors_on_good_frames / np.min(reprojection_errors_on_good_frames)

    # Find the index of the good frame with the lowest velocity and lowest error
    combined_error = mean_velocities_on_good_frames# + good_frames_errors_normalized
    best_frame = all_good_frames[np.argmin(combined_error)]

    return best_frame
