from typing import List

from freemocap_blender_addon.freemocap_data.freemocap_data_component import ComponentType
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType
from freemocap_blender_addon.models.mediapipe_stuff.mediapipe_trajectory_names import MEDIAPIPE_BODY_NAMES, \
    MEDIAPIPE_FACE_NAMES, MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS


def get_keypoint_names(component_type: ComponentType,
                       data_source: TrackerSourceType) -> List[str]:

    if data_source == 'mediapipe':
        if component_type == ComponentType.BODY:
            return MEDIAPIPE_BODY_NAMES
        elif component_type == ComponentType.FACE:
            return MEDIAPIPE_FACE_NAMES
        elif component_type == ComponentType.RIGHT_HAND:
            return [f"right_hand_{name}" for name in MEDIAPIPE_BODY_NAMES]
        elif component_type == ComponentType.LEFT_HAND:
            return [f"left_hand_{name}" for name in MEDIAPIPE_BODY_NAMES]
        else:
            raise ValueError("Component type not recognized")


def get_virtual_trajectory_definitions(data_source: TrackerSourceType):
    if data_source == 'mediapipe':
        return MEDIAPIPE_VIRTUAL_TRAJECTORY_DEFINITIONS
    else:
        raise ValueError("Data source not recognized")