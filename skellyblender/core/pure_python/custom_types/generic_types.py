from typing import List, Dict, Union

TrackedPointName = str
KeypointName = str
SegmentName = str
DimensionName = str

TrackedPointList = List[TrackedPointName]
WeightedTrackedPoints = Dict[TrackedPointName, float]
KeypointMappingType = Union[TrackedPointName, TrackedPointList, WeightedTrackedPoints]  # , OffsetKeypoint]
# OffsetKeypoint = Dict[Keypoint, Tuple[float, float, float]] # TODO - implement this

DimensionNames = List[DimensionName]
BlenderizedName = str
