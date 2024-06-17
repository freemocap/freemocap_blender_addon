from abc import ABC
from dataclasses import dataclass

import numpy as np

from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class KeypointDefinition(TypeSafeDataclass, ABC):
    """
    A Keypoint is a named "key" location on a skeleton, used to define the position of a rigid body or linkage.
    In marker-based motion capture, keypoints could correspond to markers placed on the body.
    In markerless motion capture, keypoints could correspond to a tracked point in the image.
    When a Keypoint is hydrated with data, it becomes a Trajectory.

    `definition` is a human-oriented description of the keypoint's location (e.g. an anatomical
    description of a landmark on a bone).
    """
    name: str
    definition: str

    def __post_init__(self):
        print(f"Keypoint: {self.name} instantiated with definition {self.definition}")

    def __str__(self):
        return f"Keypoint: {self.name}"


@dataclass
class KeypointTrajectory(TypeSafeDataclass, ABC):
    """
    A KeypointTrajectory is a Keypoint that has been hydrated with data.
    """
    name: str
    trajectory_data: np.ndarray

    def __post_init__(self):
        if not len(self.trajectory_data.shape) == 2:
            raise ValueError("Data shape should be (frame, xyz)")
        if not self.trajectory_data.shape[1] == 3:
            raise ValueError("Trajectory data should be 3D (xyz)")

        print(f"Initialized: {self}")

    def __str__(self):
        out_str = f"KeypointTrajectory: {self.name} (Trajectory shape: {self.trajectory_data.shape})"
        return out_str
