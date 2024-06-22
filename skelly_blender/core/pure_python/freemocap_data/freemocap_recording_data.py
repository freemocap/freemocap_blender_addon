from dataclasses import dataclass
from typing import Optional, Dict

import numpy as np

from skelly_blender.core.pure_python.custom_types.derived_types import RigidBodyDefinitions, Trajectories
from skelly_blender.core.pure_python.custom_types.generic_types import TrackedPointName
from skelly_blender.core.pure_python.freemocap_data.data_paths.freemocap_data_paths import FreemocapDataPaths
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory
from skelly_blender.core.pure_python.tracked_points.data_component_types import DataComponentTypes
from skelly_blender.core.pure_python.tracked_points.tracked_points_classes import BodyTrackedPoints, FaceTrackedPoints, \
    HandsData
from skelly_blender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import DEFAULT_TRACKER_TYPE, \
    TrackerSourceType
from skelly_blender.core.pure_python.math_stuff.sample_statistics import DescriptiveStatistics
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass
from skelly_blender.system.get_path_to_test_data import get_path_to_test_data


@dataclass
class FreemocapRecordingData(TypeSafeDataclass):
    body: BodyTrackedPoints
    hands: HandsData
    face: FaceTrackedPoints

    @classmethod
    def load_from_recording_path(cls,
                                 recording_path: str,
                                 tracker_type: TrackerSourceType,
                                 scale: Optional[float] = None) -> 'FreemocapRecordingData':
        if scale is None:
            scale = 1.0  # default units are in millimeters

        data_paths = FreemocapDataPaths.from_recording_path(path=recording_path,
                                                            tracker_type=tracker_type)

        body = BodyTrackedPoints.create(trajectory_data=np.load(data_paths.skeleton.body) * scale,
                                        tracker_source=tracker_type)

        face = FaceTrackedPoints.create(data=np.load(data_paths.skeleton.face) * scale,
                                        tracker_source=tracker_type)

        hands = HandsData.create(npy_paths=data_paths.skeleton.hands,
                                 tracker_source=tracker_type,
                                 scale=scale
                                 )

        return cls(body=body, hands=hands, face=face)

    def get_trajectories(self, component_type:DataComponentTypes= DataComponentTypes.BODY) -> Dict[TrackedPointName, Trajectory]:
        if component_type == DataComponentTypes.BODY:
            return self.body.as_trajectories
        elif component_type == DataComponentTypes.FACE:
            return self.face.as_trajectories
        elif component_type == DataComponentTypes.HANDS:
            return self.hands.as_trajectories

    def __str__(self):
        body_stats = DescriptiveStatistics.from_samples(samples=self.body.trajectory_fr_name_xyz).__str__()
        right_hand_stats = DescriptiveStatistics.from_samples(samples=self.hands.right.trajectory_fr_name_xyz).__str__()
        left_hand_stats = DescriptiveStatistics.from_samples(samples=self.hands.left.trajectory_fr_name_xyz).__str__()
        face_stats = DescriptiveStatistics.from_samples(samples=self.face.trajectory_fr_name_xyz).__str__()
        return (f"SkeletonData:\n\t "
                f"BODY:\n{body_stats}, \n"
                f"RIGHT_HAND:\n{right_hand_stats}, \n"
                f"LEFT_HAND:\n{left_hand_stats}, \n"
                f"FACE:\n{face_stats}")


def load_freemocap_test_recording():
    recording_path_in = get_path_to_test_data()
    return FreemocapRecordingData.load_from_recording_path(recording_path=recording_path_in,
                                                           tracker_type=DEFAULT_TRACKER_TYPE)


@dataclass
class FreemocapDataStages(TypeSafeDataclass):
    recording_data: FreemocapRecordingData
    og_keypoint_trajectories: Trajectories
    rigidified_keypoint_trajectories: Trajectories
    inertial_aligned_keypoint_trajectories: Trajectories
    rigid_body_definitions: RigidBodyDefinitions

    @property
    def most_processed_trajectories(self) -> Trajectories:
        return self.inertial_aligned_keypoint_trajectories

    def get_all_processing_stages(self) -> Dict[str, Trajectories]:
        return {"og_from_disk": self.og_keypoint_trajectories,
                "rigidified": self.rigidified_keypoint_trajectories,
                "inertial_aligned": self.inertial_aligned_keypoint_trajectories}


if __name__ == "__main__":
    print(str(load_freemocap_test_recording()))
