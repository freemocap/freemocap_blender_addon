from dataclasses import dataclass, field
from typing import List, Optional, Dict

import numpy as np

from skelly_blender.core.pure_python.custom_types.derived_types import Trajectories, KeypointTrajectories
from skelly_blender.core.pure_python.custom_types.generic_types import TrackedPointName, DimensionNames
from skelly_blender.core.pure_python.freemocap_data.data_paths.default_path_enums import RightLeftAxial
from skelly_blender.core.pure_python.freemocap_data.data_paths.numpy_paths import HandsNpyPaths
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory
from skelly_blender.core.pure_python.tracked_points.data_component_types import DataComponentTypes
from skelly_blender.core.pure_python.tracked_points.getters.get_keypoints_by_component_and_tracker_type import \
    get_tracked_point_names
from skelly_blender.core.pure_python.tracked_points.getters.get_mapping_by_component_and_tracker_type import \
    get_tracker_keypoint_mapping
from skelly_blender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import TrackerSourceType
from skelly_blender.core.pure_python.math_stuff.sample_statistics import DescriptiveStatistics
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass

FRAME_TRAJECTORY_XYZ = ["frame_number", "trajectory_index", "xyz"]


@dataclass
class GenericTrackedPoints(TypeSafeDataclass):
    trajectory_fr_name_xyz: np.ndarray
    trajectory_names: List[TrackedPointName]
    dimension_names: DimensionNames
    tracker_source: TrackerSourceType
    component_type: DataComponentTypes = field(default=DataComponentTypes.BODY)

    @property
    def number_of_frames(self):
        return self.trajectory_fr_name_xyz.shape[0]

    @property
    def number_of_trajectories(self):
        return self.trajectory_fr_name_xyz.shape[1]

    @property
    def as_trajectories(self) -> Trajectories:
        return {name: Trajectory(name=name, trajectory_fr_xyz=self.trajectory_fr_name_xyz[:, i, :]) for i, name in
                enumerate(self.trajectory_names)}

    def __post_init__(self):
        if not len(self.trajectory_fr_name_xyz.shape) == 3:
            raise ValueError("Data shape should be (frame, trajectory, xyz)")
        if not self.trajectory_fr_name_xyz.shape[2] == 3:
            raise ValueError("Trajectory data should be 3D (xyz)")
        if not self.number_of_trajectories == len(self.trajectory_names):
            raise ValueError(
                f"Data frame shape {self.trajectory_fr_name_xyz.shape} does not match trajectory names length {len(self.trajectory_names)}")

    def map_to_keypoints(self) -> KeypointTrajectories:
        print("Mapping TrackedPoints to KeypointsTrajectories....")
        mapping = get_tracker_keypoint_mapping(component_type=self.component_type,
                                               tracker_source=self.tracker_source)
        keypoint_trajectories = {
            keypoint_name.lower(): Trajectory(name=keypoint_name.lower(),
                                              trajectory_fr_xyz=mapping.value.calculate_trajectory(
                                                  data_fr_name_xyz=self.trajectory_fr_name_xyz,
                                                  names=self.trajectory_names))
            for keypoint_name, mapping in mapping.__members__.items()}
        return keypoint_trajectories
    def __str__(self):
        stats = DescriptiveStatistics.from_samples(samples=self.right.trajectory_fr_name_xyz).__str__()

        return (f"{self.__class__.__name__}:\n\t "
                f"Number of frames: {self.number_of_frames}\n\t "
                f"Number of trajectories: {self.number_of_trajectories}\n\t "
                f"Trajectory names: {self.trajectory_names}\n\t "
                f"Stats: {stats}")

@dataclass
class BodyTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               trajectory_data: np.ndarray,
               tracker_source: TrackerSourceType,
               ):
        return cls(trajectory_fr_name_xyz=trajectory_data,
                   trajectory_names=get_tracked_point_names(component_type=DataComponentTypes.BODY,
                                                            tracker_source=tracker_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ,
                   tracker_source=tracker_source
                   )


@dataclass
class FaceTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               data: np.ndarray,
               tracker_source: TrackerSourceType):
        return cls(trajectory_fr_name_xyz=data,
                   trajectory_names=get_tracked_point_names(component_type=DataComponentTypes.FACE,
                                                            tracker_source=tracker_source),
                   dimension_names=FRAME_TRAJECTORY_XYZ,
                   tracker_source=tracker_source
                   )


@dataclass
class HandTrackedPoints(GenericTrackedPoints):
    @classmethod
    def create(cls,
               data: np.ndarray,
               tracker_source: TrackerSourceType,
               component_type: DataComponentTypes):
        return cls(trajectory_fr_name_xyz=data,
                   trajectory_names=get_tracked_point_names(component_type=component_type,
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
               tracker_source: TrackerSourceType,
               scale: Optional[float] = None):
        if scale is None:
            scale = 1.0
        return cls(right=HandTrackedPoints.create(data=np.load(npy_paths.right) * scale,
                                                  tracker_source=tracker_source,
                                                  component_type=DataComponentTypes.RIGHT_HAND),
                   left=HandTrackedPoints.create(data=np.load(npy_paths.left) * scale,
                                                 tracker_source=tracker_source,
                                                 component_type=DataComponentTypes.LEFT_HAND)
                   )

    @property
    def as_trajectories(self) -> Dict[RightLeftAxial, Trajectories]:
        return {RightLeftAxial.RIGHT.value: self.right.as_trajectories,
                RightLeftAxial.LEFT.value:self.left.as_trajectories}

    def map_to_keypoints(self) -> Dict[RightLeftAxial, KeypointTrajectories]:
        return {RightLeftAxial.RIGHT.value: self.right.map_to_keypoints(),
                RightLeftAxial.LEFT.value: self.left.map_to_keypoints()}

