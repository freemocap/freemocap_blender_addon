from dataclasses import dataclass, field
from typing import Literal, Optional

import numpy as np

from skellyblender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class OrthonormalBasis3D(TypeSafeDataclass):
    """
    Estimates orthonormal basis vectors given reference points defining approximate directions.

    Parameters
    ----------
    origin : np.ndarray
        Origin of the basis.
    x_forward: np.ndarray
        Reference point defining the approximate forward direction (x_hat).
    y_leftward : np.ndarray
        Reference point defining the approximate leftward direction (y_hat).
    z_up : np.ndarray
        Reference point defining the approximate upward direction (z_hat).

    primary_axis : Literal["x", "y", "z"]
        The primary axis to use for the basis, this vector will remain unchanged and the two others will be adjusted to be orthogonal to it.


    Returns
    -------
    Dict[Literal["x", "y", "z"], np.ndarray]
        Orthonormal basis vectors as a dictionary with keys 'x', 'y', 'z'.

    Example
    -------
    >>> import numpy as np
    >>> origin = np.array([0, 0, 0])
    >>> x_forward
     = np.array([1.1, 0, 0])
    >>> y_leftward = np.array([0, .2, 0])
    >>> z_up = np.array([0, 0, 1])
    >>> basis = OrthonormalBasis3d.from_reference_points(origin, z_up, x_forward, y_leftward, primary='x')
    >>> basis.x_hat # Expected output: [1, 0, 0]
    >>> basis.y_hat # Expected output: [0, 1, 0]
    >>> basis.z_hat # Expected output: [0, 0, 1]
    """

    x_hat: np.ndarray
    y_hat: np.ndarray
    z_hat: np.ndarray
    origin: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0]))

    @classmethod
    def from_reference_points(cls,
                              x_forward: np.ndarray,
                              y_leftward: np.ndarray,
                              z_up: np.ndarray,
                              origin: Optional[np.ndarray],
                              primary_axis: Literal["x", "y", "z"]):

        if (origin.shape != (3,) or z_up.shape != (3,) or x_forward
                .shape != (3,) or y_leftward.shape != (3,)):
            raise ValueError("All reference points must be 3D vectors.")

        x_forward = x_forward- origin
        y_left = y_leftward - origin
        z_up = z_up - origin

        if np.allclose(x_forward, 0) or np.allclose(y_left, 0) or np.allclose(z_up, 0):
            raise ValueError("Reference points must not coincide with the origin.")

        # Hit 'em with the ol one two (follow right-hand rule):
        # 1 - cross primary onto secondary to get tertiary orthogonal to both
        # 2 - cross tertiary onto primary to get secondary orthogonal to both
        # og_primary and both cross products are all orthogonal
        if primary_axis == 'x':
            x_hat = x_forward
            z_hat = np.cross(x_hat, y_left)
            y_hat = np.cross(z_hat, x_hat)
        elif primary_axis == 'y':
            y_hat = y_left
            x_hat = np.cross(y_hat, z_up)
            z_hat = np.cross(x_hat, y_hat)
        elif primary_axis == 'z':
            z_hat = z_up
            y_hat = np.cross(z_hat, x_forward)
            x_hat = np.cross(y_hat, z_hat)
        else:
            raise ValueError("Primary must be one of 'x', 'y', or 'z'.")

        # Normalize em
        x_hat = x_hat / np.linalg.norm(x_hat)
        y_hat = y_hat / np.linalg.norm(y_hat)
        z_hat = z_hat / np.linalg.norm(z_hat)

        return cls(origin=origin,
                   x_hat=x_hat,
                   y_hat=y_hat,
                   z_hat=z_hat)

    @property
    def rotation_matrix(self) -> np.ndarray:
        return np.array([self.x_hat, self.y_hat, self.z_hat])

    def __post_init__(self):

        assert np.allclose(np.linalg.norm(self.x_hat), 1, atol=1e-6), "self.x_hat is not normalized"
        assert np.allclose(np.linalg.norm(self.y_hat), 1, atol=1e-6), "self.y_hat is not normalized"
        assert np.allclose(np.linalg.norm(self.z_hat), 1, atol=1e-6), "self.z_hat is not normalized"

        assert np.allclose(np.dot(self.z_hat, self.y_hat), 0, atol=1e-6), "self.z_hat is not orthogonal to self.y_hat"
        assert np.allclose(np.dot(self.z_hat, self.x_hat), 0, atol=1e-6), "self.z_hat is not orthogonal to self.x_hat"
        assert np.allclose(np.dot(self.y_hat, self.x_hat), 0, atol=1e-6), "self.y_hat is not orthogonal to self.x_hat"

        assert np.allclose(np.cross(self.x_hat, self.y_hat), self.z_hat,
                           atol=1e-6), "Vectors do not follow right-hand rule"
        assert np.allclose(np.cross(self.y_hat, self.z_hat), self.x_hat,
                           atol=1e-6), "Vectors do not follow right-hand rule"
        assert np.allclose(np.cross(self.z_hat, self.x_hat), self.y_hat,
                           atol=1e-6), "Vectors do not follow right-hand rule"

        assert np.allclose(self.rotation_matrix @ self.x_hat, [1, 0, 0], atol=1e-6), "x_hat is not rotated to [1, 0, 0]"
        assert np.allclose(self.rotation_matrix @ self.y_hat, [0, 1, 0], atol=1e-6), "y_hat is not rotated to [0, 1, 0]"
        assert np.allclose(self.rotation_matrix @ self.z_hat, [0, 0, 1], atol=1e-6), "z_hat is not rotated to [0, 0, 1]"

        assert np.allclose(np.linalg.det(self.rotation_matrix), 1, atol=1e-6), "rotation matrix is not a rotation matrix"


if __name__ == "__main__":
    origin = np.array([0, 0, 0])
    x_forward = np.array([1.1, 0, 0])
    y_leftward = np.array([0, .2, 0])
    z_up = np.array([0, 0, 1])
    basis = OrthonormalBasis3D.from_reference_points(origin = origin,
                                                     x_forward = x_forward,
                                                     y_leftward = y_leftward,
                                                     z_up = z_up,
                                                     primary_axis='x')
    print(basis.x_hat)  # Expected output: [1, 0, 0]
    print(basis.y_hat)  # Expected output: [0, 1, 0]
    print(basis.z_hat)  # Expected output: [0, 0, 1]
    print(basis.rotation_matrix)
    print(basis.origin)
    print(basis)
    print(basis.__repr__())
    print(basis.__post_init__())
    print(basis.rotation_matrix)