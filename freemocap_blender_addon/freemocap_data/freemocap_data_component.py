from dataclasses import dataclass
from typing import List, Dict

import numpy as np

from freemocap_blender_addon.freemocap_data.data_paths.numpy_paths import HandsNpyPaths
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, ComponentType, \
    FRAME_TRAJECTORY_XYZ
from freemocap_blender_addon.models.skeleton_model.keypoint_segments_linkage_chain_abc import TrackedPointName
from freemocap_blender_addon.utilities.get_keypoint_names import get_keypoint_names, get_mapping
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class GenericTrackedPoints(TypeSafeDataclass):
    trajectory_data: np.ndarray
    trajectory_names: List[TrackedPointName]
    dimension_names: List[str]
    tracker_source: TrackerSourceType

    @property
    def number_of_frames(self):
        return self.trajectory_data.shape[0]

    @property
    def number_of_trajectories(self):
        return self.trajectory_data.shape[1]

    def __post_init__(self):
        if not len(self.trajectory_data.shape) == 3:
            raise ValueError("Data shape should be (frame, trajectory, xyz)")
        if not self.trajectory_data.shape[2] == 3:
            raise ValueError("Trajectory data should be 3D (xyz)")
        if not self.number_of_trajectories == len(self.trajectory_names):
            raise ValueError(
                f"Data frame shape {self.trajectory_data.shape} does not match trajectory names length {len(self.trajectory_names)}")

    def map_to_keypoints(self) -> Dict[str, np.ndarray]:
        mapping = get_mapping(component_type=ComponentType.BODY,
                              tracker_source=self.tracker_source)
        keypoint_trajectories = {
            keypoint_name.lower(): mapping.value.calculate_trajectory(data=self.trajectory_data,
                                                        names=self.trajectory_names)
            for keypoint_name, mapping in mapping.__members__.items()}
        return keypoint_trajectories


class BodyTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               trajectory_data: np.ndarray,
               tracker_source: TrackerSourceType,
               ):
        return cls(trajectory_data=trajectory_data,
                   trajectory_names=get_keypoint_names(component_type=ComponentType.BODY,
                                                       tracker_source=tracker_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ,
                   tracker_source=tracker_source
                   )


class FaceTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               data: np.ndarray,
               tracker_source: TrackerSourceType):
        return cls(trajectory_data=data,
                   trajectory_names=get_keypoint_names(component_type=ComponentType.FACE,
                                                       tracker_source=tracker_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ,
                   tracker_source=tracker_source
                   )


class HandTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               data: np.ndarray,
               tracker_source: TrackerSourceType,
               component_type: ComponentType):
        return cls(trajectory_data=data,
                   trajectory_names=get_keypoint_names(component_type=component_type,
                                                       tracker_source=tracker_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ,
                   tracker_source=tracker_source
                   )


@dataclass
class HandsData(TypeSafeDataclass):
    right: HandTrackedPoints
    left: HandTrackedPoints

    @classmethod
    def create(cls,
               npy_paths: HandsNpyPaths,
               tracker_source: TrackerSourceType):
        return cls(right=HandTrackedPoints.create(data=np.load(npy_paths.right),
                                                  tracker_source=tracker_source,
                                                  component_type=ComponentType.RIGHT_HAND),
                   left=HandTrackedPoints.create(data=np.load(npy_paths.left),
                                                 tracker_source=tracker_source,
                                                 component_type=ComponentType.LEFT_HAND)
                   )
