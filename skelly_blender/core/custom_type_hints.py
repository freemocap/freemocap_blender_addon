from typing import List, Dict, Union, Literal

from skelly_blender.core.rigid_bodies.rigid_segment_definition import \
    RigidSegmentDefinition
from skelly_blender.core.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory
from skelly_blender.core.utility_classes.sample_statistics import DescriptiveStatistics

TrackedPointName = str
TrackedPointList = List[TrackedPointName]
WeightedTrackedPoints = Dict[TrackedPointName, float]
KeypointMappingType = Union[TrackedPointName, TrackedPointList, WeightedTrackedPoints]  # , OffsetKeypoint]
# OffsetKeypoint = Dict[Keypoint, Tuple[float, float, float]] # TODO - implement this

KeypointTrajectories = Dict[TrackedPointName, Trajectory]
SegmentStats = Dict[str, DescriptiveStatistics]
RigidSegmentDefinitions = Dict[str, RigidSegmentDefinition]

BlenderizedName = str

DimensionNames = List[str]
