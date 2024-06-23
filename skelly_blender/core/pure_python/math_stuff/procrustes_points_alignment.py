from dataclasses import dataclass

import numpy as np


@dataclass
class ProcrustesAnalysisResult:
    rotation_matrix: np.ndarray
    translation_vector: np.ndarray
    scaling_factor: float
    aligned_points: np.ndarray
    alignment_error: np.ndarray


def procrustes_points_alignment(source_points: np.ndarray,
                                target_points: np.ndarray) -> ProcrustesAnalysisResult:
    """
    Perform Procrustes analysis to align two sets of points.

    This function computes the optimal alignment of two sets of points by applying
    translation, scaling, and rotation to the source points to best match the target points.

    More info: https://en.wikipedia.org/wiki/Procrustes_analysis
    Parameters
    ----------
    source_points : np.ndarray
        An array of shape (N, D) representing the source points, where N is the number of points and D is the dimension.
    target_points : np.ndarray
        An array of shape (N, D) representing the target points, where N is the number of points and D is the dimension.

    Returns
    -------
    rotation_matrix : np.ndarray
        An array of shape (D, D) representing the rotation matrix.
    translation_vector : np.ndarray
        An array of shape (D,) representing the translation vector.
    scaling_factor : float
        A scalar value representing the scaling factor.
    aligned_points : np.ndarray
        An array of shape (N, D) representing the aligned source points.
    alignment_error : np.ndarray
        An array of shape (N, D) representing the alignment error for each point.

    Raises
    ------
    ValueError
        If the input arrays do not have the same shape or if the number of points is less than 2.

    Notes
    -----
    This function uses a classical Procrustes analysis method to align the points.

    Example
    -------
    >>> source_points = np.array([[1, 2], [3, 4], [5, 6]])
    >>> target_points = np.array([[2, 4], [6, 8], [10, 12.1]])
    >>> rotation_matrix, translation_vector, scaling_factor, aligned_points, alignment_error = procrustes_points_alignment(source_points, target_points)
    >>> rotation_matrix
    array([[1., 0.],
           [0., 1.]])
    >>> translation_vector
    array([1., 2.])
    >>> scaling_factor
    2.0
    >>> aligned_points
    array([[ 2.,  4.],
           [ 6.,  8.],
           [10., 12.1]])
    >>> alignment_error
    array([[0., 0.],
           [0., 0.],
           [0., 0.1]])
    """
    if source_points.shape != target_points.shape:
        raise ValueError("Source and target points must have the same shape.")

    num_points, dim = source_points.shape
    if num_points < 2:
        raise ValueError("At least two points are required to compute the transformation.")

    # Compute the centroids (mean points) of the source and target points
    centroid_source = np.mean(source_points, axis=0)
    centroid_target = np.mean(target_points, axis=0)

    # Center the points by subtracting their respective centroids
    centered_source = source_points - centroid_source
    centered_target = target_points - centroid_target

    # Compute the Frobenius norm (a measure of the size) of the centered points
    norm_source = np.linalg.norm(centered_source)
    norm_target = np.linalg.norm(centered_target)

    # Scale the points by dividing by their Frobenius norm
    scaled_source = centered_source / norm_source
    scaled_target = centered_target / norm_target

    # Compute the cross-covariance matrix
    covariance_matrix = np.dot(scaled_source.T, scaled_target)

    # Perform Singular Value Decomposition (SVD) on the covariance matrix
    U, _, Vt = np.linalg.svd(covariance_matrix)

    # Compute the rotation matrix as the product of U and Vt
    rotation_matrix = np.dot(Vt.T, U.T)

    # Ensure a proper rotation (det(rotation_matrix) should be 1, not -1)
    if np.linalg.det(rotation_matrix) < 0:
        Vt[-1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)

    # Compute the scaling factor as the ratio of the norms of the target and source points
    scaling_factor = norm_target / norm_source

    # Compute the translation vector to align the centroids
    translation_vector = centroid_target - scaling_factor * np.dot(centroid_source, rotation_matrix)

    # Apply the computed transformation to the source points
    aligned_points = scaling_factor * np.dot(source_points, rotation_matrix) + translation_vector

    # Compute the alignment error for each point
    alignment_error = np.abs(aligned_points - target_points)

    return ProcrustesAnalysisResult(rotation_matrix=rotation_matrix,
                                    translation_vector=translation_vector,
                                    scaling_factor=scaling_factor,
                                    aligned_points=aligned_points,
                                    alignment_error=alignment_error)


if __name__ == "__main__":
    source_points = np.array([[1, 2, 1], [3, 4, 1], [5, 6, 1]])
    target_points = np.array([[2, 4, 2], [6, 8, 2], [10, 12.01, 2]])
    result= procrustes_points_alignment(
        source_points, target_points)
    print("Rotation Matrix:\n", result.rotation_matrix)
    print("Translation Vector:\n", result.translation_vector)
    print("Scaling Factor:\n", result.scaling_factor)
    print("Aligned Points:\n", result.aligned_points)
    print("Alignment Error:\n", result.alignment_error)
