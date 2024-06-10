from typing import List, Dict, Union

import numpy as np

TrackedPointName = str
TrackedPointList = List[TrackedPointName]
WeightedTrackedPoints = Dict[TrackedPointName, float]
KeypointMappingType = Union[TrackedPointName, TrackedPointList, WeightedTrackedPoints]  # , OffsetKeypoint]
# OffsetKeypoint = Dict[Keypoint, Tuple[float, float, float]] # TODO - implement this

KeypointTrajectories = Dict[TrackedPointName, np.ndarray]