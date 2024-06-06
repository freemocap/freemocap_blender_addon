from dataclasses import dataclass
from typing import List

import numpy as np

from freemocap_blender_addon.freemocap_data.data_paths.numpy_paths import HandsNpyPaths
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, ComponentType, \
    FRAME_TRAJECTORY_XYZ
from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import TrackedPointName
from freemocap_blender_addon.utilities.get_keypoint_names import get_keypoint_names
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class GenericTrackedPoints(TypeSafeDataclass):
    trajectory_data: np.ndarray
    trajectory_names: List[TrackedPointName]
    dimension_names: List[str]

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



class BodyTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               trajectory_data: np.ndarray,
               data_source: TrackerSourceType,
               ):
        return cls(trajectory_data=trajectory_data,
                   trajectory_names=get_keypoint_names(component_type=ComponentType.BODY,
                                                       data_source=data_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ,

                   )


class FaceTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               data: np.ndarray,
               data_source: TrackerSourceType):

        return cls(trajectory_data=data,
                   trajectory_names=get_keypoint_names(component_type=ComponentType.FACE,
                                                       data_source=data_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ
                   )


class HandTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               data: np.ndarray,
               data_source: TrackerSourceType,
               component_type: ComponentType):

        return cls(data=data,
                   trajectory_names=get_keypoint_names(component_type=component_type,
                                                       data_source=data_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ
                   )


@dataclass
class HandsData(TypeSafeDataclass):
    right: HandTrackedPoints
    left: HandTrackedPoints

    @classmethod
    def create(cls,
               npy_paths: HandsNpyPaths,
               data_source: TrackerSourceType):
        return cls(right=HandTrackedPoints.create(data=np.load(npy_paths.right),
                                                  data_source=data_source,
                                                  component_type=ComponentType.RIGHT_HAND),
                   left=HandTrackedPoints.create(data=np.load(npy_paths.left),
                                                 data_source=data_source,
                                                 component_type=ComponentType.LEFT_HAND)
                   )
