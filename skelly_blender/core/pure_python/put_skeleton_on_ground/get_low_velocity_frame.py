import numpy as np

from skelly_blender.core.pure_python.generic_type_hints import Trajectories


def get_low_velocity_frame(trajectories: Trajectories, ignore_first_n_frames: int = 30) -> int:
    """
    Estimate the frame with the lowest combined velocity for the provided trajectories.

    Parameters
    ----------
    trajectories : KeypointTrajectories
        The keypoint trajectories containing the trajectory data.
    ignore_first_n_frames : int, optional
        The number of initial frames to ignore, by default 30

    Returns
    -------
    int
        The frame index with the lowest combined velocity.
    """
    all_velocities = []
    floating_point_error = np.finfo(float).eps * 10  # 10 times the floating point error

    for trajectory_name in list(trajectories.keys()):
        trajectory_velocity_frame_xyz = np.diff(trajectories[trajectory_name].trajectory_data, axis=0)
        trajectory_velocity_frame_xyz = np.insert(trajectory_velocity_frame_xyz, 0, np.nan, axis=0)
        trajectory_velocity_frame_magnitude = np.sqrt(np.sum(trajectory_velocity_frame_xyz ** 2, axis=1))
        trajectory_velocity_frame_magnitude[:ignore_first_n_frames] = np.nan

        all_velocities.append(trajectory_velocity_frame_magnitude)

    combined_velocity = np.nansum(all_velocities, axis=0)
    combined_velocity[combined_velocity < floating_point_error] = np.nan
    return np.nanargmin(combined_velocity)
