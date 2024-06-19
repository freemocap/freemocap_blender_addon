from dataclasses import dataclass

import numpy as np

from skelly_blender.core.load_data.data_paths.freemocap_data_paths import FreemocapDataPaths
from skelly_blender.core.tracked_points.tracked_points_classes import BodyTrackedPoints, FaceTrackedPoints, HandsData
from skelly_blender.core.tracked_points.tracker_sources.tracker_source_types import DEFAULT_TRACKER_TYPE, TrackerSourceType
from skelly_blender.core.utility_classes.sample_statistics import DescriptiveStatistics
from skelly_blender.core.utility_classes.type_safe_dataclass import TypeSafeDataclass
from skelly_blender.system.get_path_to_test_data import get_path_to_test_data


@dataclass
class FreemocapRecordingData(TypeSafeDataclass):
    body: BodyTrackedPoints
    hands: HandsData
    face: FaceTrackedPoints

    @classmethod
    def load_from_recording_path(cls,
                                 recording_path: str,
                                 tracker_type: TrackerSourceType) -> 'FreemocapRecordingData':
        data_paths = FreemocapDataPaths.from_recording_path(path=recording_path,
                                                            tracker_type=tracker_type)

        body = BodyTrackedPoints.create(trajectory_data=np.load(data_paths.skeleton.body),
                                        tracker_source=tracker_type)

        face = FaceTrackedPoints.create(data=np.load(data_paths.skeleton.face),
                                        tracker_source=tracker_type)

        hands = HandsData.create(npy_paths=data_paths.skeleton.hands,
                                 tracker_source=tracker_type)

        return cls(body=body, hands=hands, face=face)

    def __str__(self):
        body_stats = DescriptiveStatistics.from_samples(samples=self.body.trajectory_data).__str__()
        right_hand_stats = DescriptiveStatistics.from_samples(samples=self.hands.right.trajectory_data).__str__()
        left_hand_stats = DescriptiveStatistics.from_samples(samples=self.hands.left.trajectory_data).__str__()
        face_stats = DescriptiveStatistics.from_samples(samples=self.face.trajectory_data).__str__()
        return (f"SkeletonData:\n\t "
                f"BODY:\n{body_stats}, \n"
                f"RIGHT_HAND:\n{right_hand_stats}, \n"
                f"LEFT_HAND:\n{left_hand_stats}, \n"
                f"FACE:\n{face_stats}")


def load_freemocap_test_recording():
    recording_path_in = get_path_to_test_data()
    return FreemocapRecordingData.load_from_recording_path(recording_path=recording_path_in,
                                                           tracker_type=DEFAULT_TRACKER_TYPE)


if __name__ == "__main__":
    print(str(load_freemocap_test_recording()))
