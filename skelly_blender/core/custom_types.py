from typing import List, Dict, Union

from skelly_blender.core.rigid_bodies.rigid_segment import RigidSegmentDefinition
from skelly_blender.core.skeleton_model.abstract_base_classes import Trajectory
from skelly_blender.core.utility_classes import DescriptiveStatistics

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
BlenderizedName = str
