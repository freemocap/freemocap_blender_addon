from typing import List, Dict, Union

from skelly_blender.core.pure_python.rigid_bodies.rigid_segment_definition import RigidSegmentDefinition
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory
from skelly_blender.core.pure_python.utility_classes.sample_statistics import DescriptiveStatistics

TrackedPointName = str
SegmentName = str
DimensionName = str

TrackedPointList = List[TrackedPointName]
WeightedTrackedPoints = Dict[TrackedPointName, float]
KeypointMappingType = Union[TrackedPointName, TrackedPointList, WeightedTrackedPoints]  # , OffsetKeypoint]
# OffsetKeypoint = Dict[Keypoint, Tuple[float, float, float]] # TODO - implement this

Trajectories = Dict[TrackedPointName, Trajectory]
SegmentStats = Dict[SegmentName, DescriptiveStatistics]
RigidSegmentDefinitions = Dict[SegmentName, RigidSegmentDefinition]



DimensionNames = List[DimensionName]
