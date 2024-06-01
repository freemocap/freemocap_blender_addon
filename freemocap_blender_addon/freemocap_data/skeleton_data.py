from dataclasses import dataclass

import numpy as np

from freemocap_blender_addon.core_functions.setup_scene.get_path_to_test_data import get_path_to_test_data
from freemocap_blender_addon.freemocap_data.freemocap_component_data import FreemocapComponentData, ComponentType
from freemocap_blender_addon.freemocap_data.freemocap_data_paths import FreemocapDataPaths, DEFAULT_DATA_SOURCE, \
    HandsNpyPaths, DataSourceType
from freemocap_blender_addon.freemocap_data.freemocap_data_stats import FreemocapDataStats


# @dataclass
# class CenterOfMassComponentData:
#     full_body: FreemocapComponentData
#     segments: FreemocapComponentData
#
#     @classmethod
#     def from_npy_paths(cls, npy_paths: FreemocapDataPaths) -> 'CenterOfMassComponentData':
#         full_body = FreemocapComponentData.create(data=np.load(npy_paths.center_of_mass.total_body_center_of_mass),
#                                                   component_type=ComponentType.FULL_BODY_CENTER_OF_MASS,
#                                                   data_source=DataSourceType.FULL_BODY_CENTER_OF_MASS)
#         segments = FreemocapComponentData.create(data=np.load(npy_paths.center_of_mass.segment_center_of_mass),
#                                                  component_type=ComponentType.SEGMENT_CENTER_OF_MASS,
#                                                  data_source=DataSourceType.WINTER_ANTHROPOMETRY)
#         return cls(full_body=full_body, segments=segments)


@dataclass
class HandsComponentData:
    right: FreemocapComponentData
    left: FreemocapComponentData

    @classmethod
    def from_npy_paths(cls,
                       npy_paths: HandsNpyPaths,
                       data_source: DataSourceType):
        return cls(right=FreemocapComponentData.create(data=np.load(npy_paths.right),
                                                       component_type=ComponentType.RIGHT_HAND,
                                                       data_source=data_source),
                   left=FreemocapComponentData.create(data=np.load(npy_paths.left),
                                                      component_type=ComponentType.LEFT_HAND,
                                                      data_source=data_source)
                   )


@dataclass
class SkeletonData:
    body: FreemocapComponentData
    hands: HandsComponentData
    face: FreemocapComponentData

    @classmethod
    def from_recording_path(cls,
                            recording_path: str,
                            data_source: DataSourceType) -> 'SkeletonData':
        data_paths = FreemocapDataPaths.from_recording_path(path=recording_path,
                                                            data_source=data_source)

        body = FreemocapComponentData.create(data=np.load(data_paths.skeleton.body),
                                             component_type=ComponentType.BODY,
                                             data_source=data_source)

        face = FreemocapComponentData.create(data=np.load(data_paths.skeleton.face),
                                             data_source=data_source,
                                             component_type=ComponentType.FACE)
        hands = HandsComponentData.from_npy_paths(npy_paths=data_paths.skeleton.hands,
                                                  data_source=data_source)
        return cls(body=body, hands=hands, face=face)

    def __str__(self):
        return str(FreemocapDataStats.from_freemocap_data(self))


if __name__ == "__main__":
    recording_path_in = get_path_to_test_data()
    freemocap_data = SkeletonData.from_recording_path(recording_path=recording_path_in,
                                                      data_source=DEFAULT_DATA_SOURCE)
    print(str(freemocap_data))
