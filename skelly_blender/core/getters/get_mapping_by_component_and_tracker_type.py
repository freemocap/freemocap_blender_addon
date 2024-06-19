def get_mapping(component_type: ComponentType,
                tracker_source: TrackerSourceType):  # TODO- figure out how to give this a generic `mapping` return type hint
    if tracker_source == TrackerSourceType.MEDIAPIPE:
        if component_type == ComponentType.BODY:
            return MediapipeBodyMapping

        else:
            raise ValueError("Component type not recognized")
    else:
        raise ValueError("Data source not recognized")
