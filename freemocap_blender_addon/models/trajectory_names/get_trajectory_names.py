from typing import List

from freemocap_blender_addon.freemocap_data.freemocap_data_component import ComponentType
from freemocap_blender_addon.freemocap_data.freemocap_data_paths import TrackerSourceType


def get_trajectory_names(component_type: ComponentType,
                         data_source: TrackerSourceType) -> List[str]:
    if data_source == 'mediapipe':
        if component_type == ComponentType.BODY:
            return MEDIAPIPE_TRAJECTORY_NAMES.body
        elif component_type == ComponentType.FACE:
            return MEDIAPIPE_TRAJECTORY_NAMES.face
        elif component_type == ComponentType.RIGHT_HAND:
            return MEDIAPIPE_TRAJECTORY_NAMES.hands.right
        elif component_type == ComponentType.LEFT_HAND:
            return MEDIAPIPE_TRAJECTORY_NAMES.hands.left
        else:
            raise ValueError("Component type not recognized")

    if data_source == 'center_of_mass':
        if component_type == ComponentType.FULL_BODY_CENTER_OF_MASS:
            return ['total_body_center_of_mass']
        elif component_type == ComponentType.SEGMENT_CENTER_OF_MASS:
            return WINTER_95_SEGMENT_NAMES
        else:
            raise ValueError("Component type not recognized")
