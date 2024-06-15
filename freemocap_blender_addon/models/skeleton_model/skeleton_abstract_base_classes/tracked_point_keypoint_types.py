from typing import List, Dict, Union

from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.keypoint_abc import KeypointTrajectory
from freemocap_blender_addon.utilities.sample_statistics import DescriptiveStatistics

TrackedPointName = str
TrackedPointList = List[TrackedPointName]
WeightedTrackedPoints = Dict[TrackedPointName, float]
KeypointMappingType = Union[TrackedPointName, TrackedPointList, WeightedTrackedPoints]  # , OffsetKeypoint]
# OffsetKeypoint = Dict[Keypoint, Tuple[float, float, float]] # TODO - implement this

KeypointTrajectories = Dict[TrackedPointName, KeypointTrajectory]
SegmentStats = Dict[str, DescriptiveStatistics]
