from typing import List, Dict, Union

import numpy as np

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.keypoint_abc import KeypointTrajectory

TrackedPointName = str
TrackedPointList = List[TrackedPointName]
WeightedTrackedPoints = Dict[TrackedPointName, float]
KeypointMappingType = Union[TrackedPointName, TrackedPointList, WeightedTrackedPoints]  # , OffsetKeypoint]
# OffsetKeypoint = Dict[Keypoint, Tuple[float, float, float]] # TODO - implement this

KeypointTrajectories = Dict[TrackedPointName, KeypointTrajectory]