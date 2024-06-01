from dataclasses import dataclass

import numpy as np

from freemocap_blender_addon.core_functions.setup_scene.get_path_to_sample_data import get_path_to_test_data
from freemocap_blender_addon.freemocap_data.freemocap_component_data import FreemocapComponentData, ComponentType
from freemocap_blender_addon.freemocap_data.freemocap_data_paths import FreemocapDataPaths, DEFAULT_TRACKER_TYPE, \
    HandsNpyPaths, TrackerType, RightLeft
from freemocap_blender_addon.freemocap_data.freemocap_data_stats import FreemocapDataStats
from freemocap_blender_addon.models.mediapipe_names.mediapipe_trajectory_names import MEDIAPIPE_HAND_NAMES


@dataclass
class CenterOfMassComponentData:
    full_body: FreemocapComponentData
    segments: FreemocapComponentData

    @classmethod
    def from_npy_paths(cls, npy_paths: FreemocapDataPaths) -> 'CenterOfMassComponentData':
        full_body = FreemocapComponentData.create(npy_paths=npy_paths.center_of_mass.total_body_center_of_mass,
                                                  component_type=ComponentType.FULL_BODY_CENTER_OF_MASS,
                                                  tracker_type=DEFAULT_TRACKER_TYPE)
        segments = FreemocapComponentData.create(npy_paths=npy_paths.center_of_mass.segment_center_of_mass,
                                                 component_type=ComponentType.SEGMENT_CENTER_OF_MASS,
                                                 tracker_type=DEFAULT_TRACKER_TYPE)
        return cls(full_body=full_body, segments=segments)


@classmethod
class HandsComponentData:
    right: FreemocapComponentData
    left: FreemocapComponentData

    @classmethod
    def from_npy_paths(cls,
                       npy_paths: HandsNpyPaths,
                       reprojection_error: np.ndarray,
                       tracker_type: str = TrackerType) -> 'HandsComponentData':
        if tracker_type == 'mediapipe':
            trajectory_names = MEDIAPIPE_HAND_NAMES
        else:
            raise NotImplementedError(f"Tracker type {tracker_type} not implemented")
        return cls(right=FreemocapComponentData(data=np.load(npy_paths.right),
                                                component_type=ComponentType.HAND_RIGHT,
                                                trajectory_names=[f"{RightLeft.RIGHT.value}_{name}" for name in
                                                                  trajectory_names],
                                                tracker_type=tracker_type,
                                                reprojection_error=reprojection_error),

                   left=FreemocapComponentData(npy_paths=npy_paths.left,
                                               component_type=ComponentType.HAND_LEFT,
                                               tracker_type=tracker_type,
                                               reprojection_error=reprojection_error))


@dataclass
class SkeletonData:
    body: FreemocapComponentData
    hands: HandsComponentData
    face: FreemocapComponentData
    center_of_mass: CenterOfMassComponentData

    @classmethod
    def from_recording_path(cls,
                            recording_path: str,
                            tracker_type: TrackerType) -> 'SkeletonData':
        data_paths = FreemocapDataPaths.from_recording_path(path=recording_path)
        reprojection_error = np.load(data_paths.skeleton.reprojection_error)

        body = FreemocapComponentData.create(npy_paths=data_paths.skeleton.body,
                                             component_type=ComponentType.BODY,
                                             tracker_type=tracker_type)

        hands = HandsComponentData.from_npy_paths(npy_paths=data_paths.skeleton.hands,
                                                  reprojection_error=reprojection_error,
                                                  tracker_type=tracker_type)
        face = FreemocapComponentData.create(npy_paths=data_paths.skeleton.face,
                                             tracker_type=tracker_type,
                                             component_type=ComponentType.FACE)
        center_of_mass = CenterOfMassComponentData.from_npy_paths(npy_paths=data_paths.center_of_mass,
                                                                  tracker_type=tracker_type)

    def __str__(self):
        return str(FreemocapDataStats.from_freemocap_data(self))


if __name__ == "__main__":
    recording_path_in = get_path_to_test_data()
    freemocap_data = SkeletonData.from_recording_path(recording_path=recording_path_in)
    print(str(freemocap_data))
