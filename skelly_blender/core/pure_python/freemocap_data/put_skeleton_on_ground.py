from copy import deepcopy

import numpy as np

from skelly_blender.core.pure_python.custom_types import Trajectories
from skelly_blender.core.pure_python.freemocap_data.transform_skeleton_data.get_low_velocity_frame import \
    get_low_velocity_frame
from skelly_blender.core.pure_python.freemocap_data.transform_skeleton_data.points_transformers import transform_points
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints
from skelly_blender.core.pure_python.utility_classes.orthonormal_basis_3d import OrthonormalBasis3D


def put_skeleton_on_ground(keypoint_trajectories: Trajectories, copy_trajectories: bool = False) -> Trajectories:
    print(f"Putting freemocap data in inertial reference frame...")

    ground_reference_trajectories = {key: keypoint_trajectories[key] for key in
                                     [BodyKeypoints.RIGHT_HEEL.name.lower(),
                                      BodyKeypoints.LEFT_HEEL.name.lower(),
                                      BodyKeypoints.RIGHT_HALLUX_TIP.name.lower(),
                                      BodyKeypoints.LEFT_HALLUX_TIP.name.lower(),
                                      ]}

    good_frame = get_low_velocity_frame(trajectories=ground_reference_trajectories)

    original_reference_locations = {trajectory_name: trajectory.trajectory_data[good_frame, :]
                                    for trajectory_name, trajectory in
                                    ground_reference_trajectories.items()}

    center_reference_point = np.mean(list(original_reference_locations.values()), axis=0)

    x_forward_reference = np.mean([original_reference_locations[BodyKeypoints.RIGHT_HALLUX_TIP.name.lower()],
                                   original_reference_locations[BodyKeypoints.LEFT_HALLUX_TIP.name.lower()]],
                                  axis=0)

    y_leftward_reference = np.mean([original_reference_locations[BodyKeypoints.LEFT_HALLUX_TIP.name.lower()],
                                    original_reference_locations[BodyKeypoints.LEFT_HEEL.name.lower()]],
                                   axis=0)

    z_up_reference = keypoint_trajectories[
                         BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name.lower()].trajectory_data[
                     good_frame, :]

    basis = OrthonormalBasis3D.from_reference_points(origin=center_reference_point,
                                                     x_forward=x_forward_reference,
                                                     y_leftward=y_leftward_reference,
                                                     z_up=z_up_reference,
                                                     primary_axis='x')
    if copy_trajectories:
        # Make a deep copy of the input data to avoid modifying the original data at the time-cost of an additional copy operation
        transformed_trajectories = deepcopy(keypoint_trajectories)
    else:
        transformed_trajectories = keypoint_trajectories

    # Transform the trajectories to the new reference frame
    for key in transformed_trajectories.keys():
        transformed_trajectories[key].trajectory_data = transform_points(
            points=keypoint_trajectories[key].trajectory_data,
            translation_vector=-center_reference_point,
            rotation_matrix=basis.rotation_matrix)

    return transformed_trajectories
