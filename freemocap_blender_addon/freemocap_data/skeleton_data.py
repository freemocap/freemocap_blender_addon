from dataclasses import dataclass

import numpy as np

from freemocap_blender_addon.core_functions.setup_scene.get_path_to_test_data import get_path_to_test_data
from freemocap_blender_addon.freemocap_data.freemocap_data_component import FreemocapDataComponent, ComponentType
from freemocap_blender_addon.freemocap_data.freemocap_data_paths import FreemocapDataPaths, DEFAULT_TRACKER_TYPE, \
    HandsNpyPaths, TrackerSourceType


@dataclass
class HandsComponentData:
    right: FreemocapDataComponent
    left: FreemocapDataComponent

    @classmethod
    def from_npy_paths(cls,
                       npy_paths: HandsNpyPaths,
                       data_source: TrackerSourceType):
        return cls(right=FreemocapDataComponent.create(data=np.load(npy_paths.right),
                                                       component_type=ComponentType.RIGHT_HAND,
                                                       data_source=data_source),
                   left=FreemocapDataComponent.create(data=np.load(npy_paths.left),
                                                      component_type=ComponentType.LEFT_HAND,
                                                      data_source=data_source)
                   )


@dataclass
class SkeletonData:
    body: FreemocapDataComponent
    hands: HandsComponentData
    face: FreemocapDataComponent

    @classmethod
    def from_recording_path(cls,
                            recording_path: str,
                            data_source: TrackerSourceType) -> 'SkeletonData':
        data_paths = FreemocapDataPaths.from_recording_path(path=recording_path,
                                                            tracker_type=data_source)

        body = FreemocapDataComponent.create(data=np.load(data_paths.skeleton.body),
                                             component_type=ComponentType.BODY,
                                             data_source=data_source)

        face = FreemocapDataComponent.create(data=np.load(data_paths.skeleton.face),
                                             data_source=data_source,
                                             component_type=ComponentType.FACE)
        hands = HandsComponentData.from_npy_paths(npy_paths=data_paths.skeleton.hands,
                                                  data_source=data_source)
        return cls(body=body, hands=hands, face=face)


if __name__ == "__main__":
    recording_path_in = get_path_to_test_data()
    skeleton_data = SkeletonData.from_recording_path(recording_path=recording_path_in,
                                                     data_source=DEFAULT_TRACKER_TYPE)
    print(str(skeleton_data))
