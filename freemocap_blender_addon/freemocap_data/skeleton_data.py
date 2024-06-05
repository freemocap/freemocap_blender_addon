from dataclasses import dataclass

import numpy as np

from freemocap_blender_addon.freemocap_data.data_paths.freemocap_data_paths import FreemocapDataPaths
from freemocap_blender_addon.freemocap_data.freemocap_data_component import BodyDataComponent
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import TrackerSourceType, DEFAULT_TRACKER_TYPE
from freemocap_blender_addon.utilities.get_path_to_test_data import get_path_to_test_data


# @dataclass
# class HandsComponentData:
#     right: SkeletonDataComponent
#     left: SkeletonDataComponent
#
#     @classmethod
#     def from_npy_paths(cls,
#                        npy_paths: HandsNpyPaths,
#                        data_source: TrackerSourceType):
#         return cls(right=SkeletonDataComponent.create(data=np.load(npy_paths.right),
#                                                       component_type=ComponentType.RIGHT_HAND,
#                                                       data_source=data_source),
#                    left=SkeletonDataComponent.create(data=np.load(npy_paths.left),
#                                                      component_type=ComponentType.LEFT_HAND,
#                                                      data_source=data_source)
#                    )


@dataclass
class SkeletonData:
    body: BodyDataComponent

    # hands: HandsComponentData
    # face: SkeletonDataComponent

    @classmethod
    def load_from_recording_path(cls,
                                 recording_path: str,
                                 tracker_type: TrackerSourceType) -> 'SkeletonData':
        data_paths = FreemocapDataPaths.from_recording_path(path=recording_path,
                                                            tracker_type=tracker_type)


        body = BodyDataComponent.create(data=np.load(data_paths.skeleton.body),
                                        data_source=tracker_type)

        # face = FaceDataComponent.create(data=np.load(data_paths.skeleton.face),
        #                                     data_source=tracker_type,
        #                                     component_type=ComponentType.FACE)
        # hands = HandsComponentData.from_npy_paths(npy_paths=data_paths.skeleton.hands,
        #                                           data_source=tracker_type)
        #
        #
        return cls(body=body)  # , hands=hands, face=face)


if __name__ == "__main__":
    recording_path_in = get_path_to_test_data()
    skeleton_data = SkeletonData.load_from_recording_path(recording_path=recording_path_in,
                                                          tracker_type=DEFAULT_TRACKER_TYPE)
    print(str(skeleton_data))
