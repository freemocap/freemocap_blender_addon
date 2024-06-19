import numpy as np


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
