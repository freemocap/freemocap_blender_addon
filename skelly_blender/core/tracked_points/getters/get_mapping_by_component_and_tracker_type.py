from skelly_blender.core.tracked_points.data_component_types import DataComponentTypes
from skelly_blender.core.tracked_points.tracker_sources.mediapipe_tracker.mediapipe_mapping import \
    MediapipeBodyMapping
from skelly_blender.core.tracked_points.tracker_sources.tracker_source_types import TrackerSourceType


def get_tracker_keypoint_mapping(component_type: DataComponentTypes,
                                 tracker_source: TrackerSourceType):  # TODO- figure out how to give this a generic `mapping` return type hint
    if tracker_source == TrackerSourceType.MEDIAPIPE:
        if component_type == DataComponentTypes.BODY:
            return MediapipeBodyMapping

        else:
            raise ValueError("Component type not recognized")
    else:
        raise ValueError("Data source not recognized")
