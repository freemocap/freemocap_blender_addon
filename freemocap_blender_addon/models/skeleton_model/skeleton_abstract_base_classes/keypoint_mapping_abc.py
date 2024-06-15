from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

import numpy as np

from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.tracked_point_keypoint_types import \
    TrackedPointName, \
    KeypointMappingType
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class KeypointMapping(TypeSafeDataclass):
    """
    A KeypointMapping provides information on how to map a keypoint to data from a TrackingDataSource trajectory.
    It can represent:
     a single keypoint (maps to the keypoint)
     a list of keypoints (maps to the geometric mean of the keypoints),
     a dictionary of keypoints with weights (maps to the weighted sum of the tracked points), or
     a dictionary of keypoints with offsets (maps to the tracked point with an offset defined in the local reference frame of the Segment).

    """
    mapping: KeypointMappingType
    tracked_points: Optional[List[TrackedPointName]] = None
    weights: Optional[List[float]] = None

    def __post_init__(self):
        if isinstance(self.mapping, str):
            self.tracked_points = [self.mapping]
            self.weights = [1]

        elif isinstance(self.mapping, list):  # TODO - fancy types
            self.tracked_points = self.mapping
            self.weights = [1 / len(self.mapping)] * len(self.mapping)

        elif isinstance(self.mapping, dict):
            self.tracked_points = list(self.mapping.keys())
            self.weights = list(self.mapping.values())
        else:
            raise ValueError("Mapping must be a TrackedPointName, TrackedPointList, or WeightedTrackedPoints")

        if np.sum(self.weights) != 1:
            raise ValueError("The sum of the weights must be 1")

    def calculate_trajectory(self, data: np.ndarray, names: List[TrackedPointName]) -> np.ndarray:
        """
        Calculate a trajectory from a mapping of tracked points and their weights.
        """
        if data.shape[1] != len(names):
            raise ValueError("Data shape does not match trajectory names length")
        if not all(tracked_point_name in names for tracked_point_name in self.tracked_points):
            raise ValueError("Not all tracked points in mapping found in trajectory names")

        number_of_frames = data.shape[0]
        number_of_dimensions = data.shape[2]
        trajectories_frame_xyz = np.zeros((number_of_frames, number_of_dimensions), dtype=np.float32)

        for tracked_point_name, weight in zip(self.tracked_points, self.weights):
            if tracked_point_name not in names:
                raise ValueError(f"Key {tracked_point_name} not found in trajectory names")

            keypoint_index = names.index(tracked_point_name)
            keypoint_xyz = data[:, keypoint_index, :]
            trajectories_frame_xyz += keypoint_xyz * weight

        return trajectories_frame_xyz


class KeypointMappingsEnum(Enum):
    """An Enum that can hold different types of keypoint mappings."""

    def __new__(cls, value: KeypointMappingType):
        obj = object.__new__(cls)
        obj._value_ = KeypointMapping(mapping=value)
        return obj
