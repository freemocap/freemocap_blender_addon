from typing import List

from skelly_blender.core.pure_python.tracked_points.tracker_sources.mediapipe_tracker.mediapipe_point_names import \
    MediapipeBodyPoints, MediapipeFacePoints, MediapipeHandPoints
from skelly_blender.core.pure_python.tracked_points.data_component_types import DataComponentTypes
from skelly_blender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import TrackerSourceType


def get_tracked_point_names(component_type: DataComponentTypes,
                            tracker_source: TrackerSourceType) -> List[str]:
    if tracker_source == TrackerSourceType.MEDIAPIPE:
        if component_type == DataComponentTypes.BODY:
            return MediapipeBodyPoints.to_lowercase_list()
        elif component_type == DataComponentTypes.FACE:
            return MediapipeFacePoints.to_lowercase_list()
        elif component_type == DataComponentTypes.RIGHT_HAND:
            return [f"right_hand_{name}" for name in MediapipeHandPoints.to_lowercase_list()]
        elif component_type == DataComponentTypes.LEFT_HAND:
            return [f"left_hand_{name}" for name in MediapipeHandPoints.to_lowercase_list()]
        else:
            raise ValueError("Component type not recognized")
