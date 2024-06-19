from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import numpy as np

from skelly_blender.core.custom_type_hints import TrackedPointName, KeypointMappingType
from skelly_blender.core.utility_classes.blenderizable_enum import BlenderizableEnum
from skelly_blender.core.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class KeypointMapping(TypeSafeDataclass):
    """
    A KeypointMapping provides information on how to map a keypoint to data from a TrackingDataSource trajectory.
    It can represent:
     a single keypoint (maps to the keypoint)
     a list of keypoints (maps to the geometric mean of the keypoints),
     a dictionary of keypoints with weights (maps to the weighted sum of the tracked points), or
     a dictionary of keypoints with offsets (maps to the tracked point with an offset defined in the local reference frame of the Segment).

    params:
    tracked_points: List[TrackedPointName] - The list of tracked points that will be combined to create the mapping to a keypoint.
    weights: List[float] - The weights of the tracked points (must sum to 1 and have the same length as tracked_points).
    offset: Tuple[float, float, float] - The offset of the keypoint in the local reference from of the Segment. #TODO - implement and double check logic
    """
    tracked_points: List[TrackedPointName]
    weights: List[float]

    @classmethod
    def create(cls, mapping: KeypointMappingType):

        if isinstance(mapping, str):
            tracked_points = [mapping]
            weights = [1]
        elif isinstance(mapping, list):  # TODO - fancy types
            tracked_points = mapping
            weights = [1 / len(mapping)] * len(mapping)

        elif isinstance(mapping, dict):
            tracked_points = list(mapping.keys())
            weights = list(mapping.values())
        else:
            raise ValueError("Mapping must be a TrackedPointName, TrackedPointList, or WeightedTrackedPoints")

        if np.sum(weights) != 1:
            raise ValueError("The sum of the weights must be 1")
        if len(tracked_points) != len(weights):
            raise ValueError("The number of tracked points must match the number of weights")

        return cls(tracked_points=tracked_points, weights=weights)

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

        if np.sum(np.isnan(trajectories_frame_xyz)) == trajectories_frame_xyz.size:
            raise ValueError("All trajectories are NaN")

        return trajectories_frame_xyz


class KeypointMappingsEnum(BlenderizableEnum):
    """An Enum that can hold different types of keypoint mappings."""

    def __new__(cls, value: KeypointMappingType):
        obj = object.__new__(cls)
        obj._value_ = KeypointMapping.create(mapping=value)
        return obj
