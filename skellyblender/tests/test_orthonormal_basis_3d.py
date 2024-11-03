import numpy as np
import pytest

from skellyblender.core.pure_python.utility_classes import OrthonormalBasis3D


def test_orthonormal_basis_creation():
    origin = np.array([0, 0, 0])
    x_forward = np.array([1.1, 0, 0])
    y_leftward = np.array([0, .2, 0])
    z_up = np.array([0, 0, 1])
    basis = OrthonormalBasis3D.from_reference_points(origin=origin,
                                                     x_forward=x_forward,
                                                     y_leftward=y_leftward,
                                                     z_up=z_up,
                                                     primary_axis='x')

    assert np.allclose(basis.x_hat, [1, 0, 0], atol=1e-6), "x_hat is not correct"
    assert np.allclose(basis.y_hat, [0, 1, 0], atol=1e-6), "y_hat is not correct"
    assert np.allclose(basis.z_hat, [0, 0, 1], atol=1e-6), "z_hat is not correct"


def test_orthonormal_basis_creation_again():
    origin = np.array([0, 0, 0])
    x_forward = np.array([1, 1, 0])
    y_leftward = np.array([0, .2, 0])
    z_up = np.array([0, 0, 1])
    basis = OrthonormalBasis3D.from_reference_points(origin=origin,
                                                     x_forward=x_forward,
                                                     y_leftward=y_leftward,
                                                     z_up=z_up,
                                                     primary_axis='x')

    assert np.allclose(basis.x_hat, [np.sqrt(2) / 2, np.sqrt(2) / 2, 0], atol=1e-6), "x_hat is not correct"
    assert np.allclose(basis.y_hat, [-np.sqrt(2) / 2, np.sqrt(2) / 2, 0], atol=1e-6), "y_hat is not correct"
    assert np.allclose(basis.z_hat, [0, 0, 1], atol=1e-6), "z_hat is not correct"


def test_different_primary_axis():
    origin = np.array([0, 0, 0])
    x_forward = np.array([1.1, 0, 0])
    y_leftward = np.array([0, 1, 1])
    z_up = np.array([0, 0, 1])
    basis = OrthonormalBasis3D.from_reference_points(origin=origin,
                                                     x_forward=x_forward,
                                                     y_leftward=y_leftward,
                                                     z_up=z_up,
                                                     primary_axis='y')

    assert np.allclose(basis.x_hat, [1, 0, 0], atol=1e-6), "x_hat is not correct"
    assert np.allclose(basis.y_hat, [0, np.sqrt(2) / 2, np.sqrt(2) / 2], atol=1e-6), "y_hat is not correct"
    assert np.allclose(basis.z_hat, [0, -np.sqrt(2) / 2, np.sqrt(2) / 2], atol=1e-6), "z_hat is not correct"


def test_invalid_reference_points():
    origin = np.array([0, 0, 0])
    invalid_point = np.array([0, 0])
    x_forward = np.array([1.1, 0, 0])
    y_leftward = np.array([0, .2, 0])
    z_up = np.array([0, 0, 1])

    with pytest.raises(ValueError, match="All reference points must be 3D vectors."):
        OrthonormalBasis3D.from_reference_points(origin=origin,
                                                 x_forward=invalid_point,
                                                 y_leftward=y_leftward,
                                                 z_up=z_up,
                                                 primary_axis='x')


def test_coincident_reference_points():
    origin = np.array([0, 0, 0])
    x_forward = origin
    y_leftward = np.array([0, .2, 0])
    z_up = np.array([0, 0, 1])

    with pytest.raises(ValueError, match="Reference points must not coincide with the origin."):
        OrthonormalBasis3D.from_reference_points(origin=origin,
                                                 x_forward=x_forward,
                                                 y_leftward=y_leftward,
                                                 z_up=z_up,
                                                 primary_axis='x')


def test_rotation_matrix():
    origin = np.array([0, 0, 0])
    x_forward = np.array([1.1, 0, 0])
    y_leftward = np.array([0, .2, 0])
    z_up = np.array([0, 0, 1])
    basis = OrthonormalBasis3D.from_reference_points(origin=origin,
                                                     x_forward=x_forward,
                                                     y_leftward=y_leftward,
                                                     z_up=z_up,
                                                     primary_axis='x')

    expected_rotation_matrix = np.array([[1, 0, 0],
                                         [0, 1, 0],
                                         [0, 0, 1]])

    assert np.allclose(basis.rotation_matrix, expected_rotation_matrix, atol=1e-6), "Rotation matrix is not correct"
