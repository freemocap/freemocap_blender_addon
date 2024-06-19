from typing import List


def get_keypoint_names(component_type: ComponentType,
                       tracker_source: TrackerSourceType) -> List[str]:
    if tracker_source == TrackerSourceType.MEDIAPIPE:
        if component_type == ComponentType.BODY:
            return MEDIAPIPE_BODY_NAMES
        elif component_type == ComponentType.FACE:
            return MEDIAPIPE_FACE_NAMES
        elif component_type == ComponentType.RIGHT_HAND:
            return [f"right_hand_{name}" for name in MEDIAPIPE_HAND_NAMES]
        elif component_type == ComponentType.LEFT_HAND:
            return [f"left_hand_{name}" for name in MEDIAPIPE_HAND_NAMES]
        else:
            raise ValueError("Component type not recognized")
