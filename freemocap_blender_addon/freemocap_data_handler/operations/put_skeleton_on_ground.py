from copy import deepcopy
from typing import Tuple

import numpy as np

from freemocap_blender_addon.freemocap_data_handler.operations.get_low_velocity_frame import get_low_velocity_frame
from freemocap_blender_addon.models.skeleton_model.body.body_keypoints import BodyKeypoints
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories


def put_skeleton_on_ground(keypoint_trajectories: KeypointTrajectories):
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

    center_reference_point = np.nanmean(list(original_reference_locations.values()), axis=0)

    x_forward_reference_point = np.nanmean([original_reference_locations[BodyKeypoints.RIGHT_HALLUX_TIP.name.lower()],
                                            original_reference_locations[BodyKeypoints.LEFT_HALLUX_TIP.name.lower()]],
                                           axis=0)

    y_leftward_reference_point = np.nanmean([original_reference_locations[BodyKeypoints.LEFT_HALLUX_TIP.name.lower()],
                                             original_reference_locations[BodyKeypoints.LEFT_HEEL.name.lower()]],
                                            axis=0)

    z_upward_reference_point = keypoint_trajectories[BodyKeypoints.SKULL_ORIGIN_FORAMEN_MAGNUM.name.lower()].trajectory_data[
                               good_frame, :]

    x_hat, y_hat, z_hat = estimate_orthonormal_basis(center_reference_point=center_reference_point,
                                                     x_forward_reference_point=x_forward_reference_point,
                                                     y_leftward_reference_point=y_leftward_reference_point,
                                                     z_upward_reference_point=z_upward_reference_point)
    rotation_matrix = np.array([x_hat, y_hat, z_hat])

    # TODO - move this stuff to tests
    assert np.allclose(np.linalg.norm(x_hat), 1, atol=1e-6), "x_hat is not normalized"
    assert np.allclose(np.linalg.norm(y_hat), 1, atol=1e-6), "y_hat is not normalized"
    assert np.allclose(np.linalg.norm(z_hat), 1, atol=1e-6), "z_hat is not normalized"
    assert np.allclose(np.dot(z_hat, y_hat), 0, atol=1e-6), "z_hat is not orthogonal to y_hat"
    assert np.allclose(np.dot(z_hat, x_hat), 0, atol=1e-6), "z_hat is not orthogonal to x_hat"
    assert np.allclose(np.dot(y_hat, x_hat), 0, atol=1e-6), "y_hat is not orthogonal to x_hat"
    assert np.allclose(np.cross(x_hat, y_hat), z_hat, atol=1e-6), "Vectors do not follow right-hand rule"
    assert np.allclose(np.cross(y_hat, z_hat), x_hat, atol=1e-6), "Vectors do not follow right-hand rule"
    assert np.allclose(np.cross(z_hat, x_hat), y_hat, atol=1e-6), "Vectors do not follow right-hand rule"
    assert np.allclose(rotation_matrix @ x_hat, [1, 0, 0], atol=1e-6), "x_hat is not rotated to [1, 0, 0]"
    assert np.allclose(rotation_matrix @ y_hat, [0, 1, 0], atol=1e-6), "y_hat is not rotated to [0, 1, 0]"
    assert np.allclose(rotation_matrix @ z_hat, [0, 0, 1], atol=1e-6), "z_hat is not rotated to [0, 0, 1]"
    assert np.allclose(np.linalg.det(rotation_matrix), 1, atol=1e-6), "rotation matrix is not a rotation matrix"

    # transformation_matrix = create_transformation_matrix(rotation_matrix=rotation_matrix,
    #                                                      translation_vector=-center_reference_point)

    transformed_trajectories = deepcopy(keypoint_trajectories)
    # Perform translation
    for key in transformed_trajectories.keys():
        transformed_trajectories[key].trajectory_data = transform_points(
            points=keypoint_trajectories[key].trajectory_data,
            translation_vector=-center_reference_point,
            rotation_matrix=rotation_matrix)

    return transformed_trajectories


def transform_points(points: np.ndarray,
                     translation_vector: np.ndarray,
                     rotation_matrix: np.ndarray) -> np.ndarray:
    translated_points = translate_points(points=points, translation_vector=translation_vector)
    rotated_points = rotate_points(points=translated_points, rotation_matrix=rotation_matrix)
    return rotated_points


def translate_points(points: np.ndarray, translation_vector: np.ndarray) -> np.ndarray:
    return points + translation_vector


def rotate_points(points: np.ndarray, rotation_matrix: np.ndarray) -> np.ndarray:
    return points @ rotation_matrix.T


def estimate_orthonormal_basis(center_reference_point: np.ndarray,
                               x_forward_reference_point: np.ndarray,
                               y_leftward_reference_point: np.ndarray,
                               z_upward_reference_point: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Estimates orthonormal basis vectors given reference points defining approximate directions.

    Parameters
    ----------
    center_reference_point : np.ndarray
        The central reference point (origin).
    x_forward_reference_point : np.ndarray
        Reference point in the forward x-direction.
    y_leftward_reference_point : np.ndarray
        Reference point in the left y-direction.
    z_upward_reference_point : np.ndarray
        Reference point in the upward z-direction.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        Orthonormal basis vectors (x_hat, y_hat, z_hat).

    Example
    -------
    >>> center = np.array([0, 0, 0])
    >>> x_forward = np.array([1, 0, 0])
    >>> y_left = np.array([0, 1, 0])
    >>> z_up = np.array([0, 0, 1])
    >>> x_hat, y_hat, z_hat = estimate_orthonormal_basis(center, x_forward, y_left, z_up)
    >>> x_hat
    array([1., 0., 0.])
    >>> y_hat
    array([0., 1., 0.])
    >>> z_hat
    array([0., 0., 1.])
    """

    if center_reference_point.shape != (3,) or x_forward_reference_point.shape != (3,) or \
            y_leftward_reference_point.shape != (3,) or z_upward_reference_point.shape != (3,):
        raise ValueError("All reference points must be 3D vectors.")

    x_forward = x_forward_reference_point - center_reference_point
    y_left = y_leftward_reference_point - center_reference_point
    z_up = z_upward_reference_point - center_reference_point

    # Make them orthogonal
    z_hat = np.cross(x_forward, y_left)
    y_hat = np.cross(z_hat, x_forward)
    x_hat = np.cross(y_hat, z_hat)

    # Normalize them
    x_hat = x_hat / np.linalg.norm(x_hat)
    y_hat = y_hat / np.linalg.norm(y_hat)
    z_hat = z_hat / np.linalg.norm(z_hat)

    return x_hat, y_hat, z_hat

#
# def create_transformation_matrix(rotation_matrix: np.ndarray, translation_vector: np.ndarray) -> np.ndarray:
#     """
#     Create a 4x4 transformation matrix from a 3x3 rotation matrix and a 3x1 translation vector.
#
#     Parameters
#     ----------
#     rotation_matrix : np.ndarray
#         3x3 rotation matrix.
#     translation_vector : np.ndarray
#         3x1 translation vector.
#
#     Returns
#     -------
#     np.ndarray
#         4x4 transformation matrix.
#     """
#     if not rotation_matrix.shape == (3, 3):
#         raise ValueError("Rotation matrix must be 3x3.")
#     if not translation_vector.shape == (3,):
#         raise ValueError("Translation vector must be 3x1.")
#
#     transformation_matrix = np.eye(4)
#     transformation_matrix[:3, :3] = rotation_matrix
#     transformation_matrix[:3, 3] = translation_vector
#
#     return transformation_matrix
#
#
# def transform_points(points: np.ndarray, transformation_matrix: np.ndarray) -> np.ndarray:
#     """
#     Apply a 4x4 transformation matrix to a set of 3D points.
#
#     Parameters
#     ----------
#     points : np.ndarray
#         Nx3 array of 3D points.
#     transformation_matrix : np.ndarray
#         4x4 transformation matrix.
#
#     Returns
#     -------
#     np.ndarray
#         Nx3 array of transformed 3D points.
#     """
#
#     if not points.shape[1] == 3:
#         raise ValueError("Points array must be Nx3.")
#     if not transformation_matrix.shape == (4, 4):
#         raise ValueError("Transformation matrix must be 4x4.")
#
#     # Convert points to homogeneous coordinates
#     ones = np.ones((points.shape[0], 1))
#     homogeneous_points = np.hstack([points, ones])
#
#     # Apply the transformation matrix
#     transformed_homogeneous_points = homogeneous_points @ transformation_matrix.T
#
#     # Convert back to 3D coordinates
#     transformed_points = transformed_homogeneous_points[:, :3]
#
#     return transformed_points
