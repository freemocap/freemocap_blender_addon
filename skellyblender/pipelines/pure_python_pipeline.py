from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from skellyblender.core.pure_python.freemocap_data.freemocap_recording_data import FreemocapRecordingData, \
    FreemocapDataStages
from skellyblender.core.pure_python.freemocap_data.put_skeleton_on_ground import put_skeleton_on_ground
from skellyblender.core.pure_python.rigid_bodies.calculate_rigid_body_trajectories import \
    calculate_rigid_body_trajectories
from skellyblender.core.pure_python.skeleton_model.skeleton_types import SkeletonTypes
from skellyblender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import TrackerSourceType, \
    DEFAULT_TRACKER_TYPE
from skellyblender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class PurePythonPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE

    @property
    def recording_name(self) -> str:
        return Path(self.recording_path_str).stem

    def run(self, scale: Optional[float] = None) -> FreemocapDataStages:
        # Pure python stuff
        print("Loading freemocap data....")
        recording_data = FreemocapRecordingData.load_from_recording_path(recording_path=self.recording_path_str,
                                                                         tracker_type=self.tracker_type,
                                                                         scale=scale)

        print("Mapping body to keypoints....")
        og_trackedpoint_trajectories = recording_data.body.as_trajectories

        print("Calculating rigid body trajectories....")
        rigidified_keypoint_trajectories, rigid_body_definitions = calculate_rigid_body_trajectories(
            keypoint_trajectories=recording_data.body.map_to_keypoints(),
            skeleton_definition=SkeletonTypes.BODY_ONLY)

        print("Putting skeleton on ground....")
        inertial_aligned_keypoint_trajectories = put_skeleton_on_ground(
            keypoint_trajectories=rigidified_keypoint_trajectories)

        print(f"{self.__class__.__name__}.run() completed successfully for recording: {self.recording_name}")
        return FreemocapDataStages(recording_data=recording_data,
                                   og_keypoint_trajectories=og_trackedpoint_trajectories,
                                   rigidified_keypoint_trajectories=rigidified_keypoint_trajectories,
                                   inertial_aligned_keypoint_trajectories=inertial_aligned_keypoint_trajectories,
                                   rigid_body_definitions=rigid_body_definitions)

        # self.fix_hand_data()
        # self.save_data_to_disk()

        # # def enforce_rigid_bones(self):
        # #     print("Enforcing rigid bones...")
        # #     try:
        # #         self.
        # #     except Exception as e:
        # #         print(f"Failed during `enforce rigid bones`, error: `{e}`")
        # #         print(e)
        # #         raise e
        # #
        # # def put_data_in_inertial_reference_frame(self):
        # #     try:
        # #         print("Putting freemocap data in inertial reference frame....")
        # #         put_skeleton_on_ground(handler=self.skeleton_data)
        # #     except Exception as e:
        # #         print(f"Failed to put freemocap data in inertial reference frame: {e}")
        # #         print(traceback.format_exc())
        # #         raise e
        # #
        # #
        # # def fix_hand_data(self):
        # #     try:
        # #         print("Fixing hand data...")
        # #         self.skeleton_data = fix_hand_data(handler=self.skeleton_data)
        # #     except Exception as e:
        # #         print(f"Failed during `fix hand data`, error: `{e}`")
        # #         print(e)
        # #         raise e
        #
        # def save_data_to_disk(self):
        #     try:
        #         print("Saving data to disk...")
        #         FreemocapDataSaver(handler=self.skeleton_data).save(recording_path=self.recording_path_str)
        #     except Exception as e:
        #         print(f"Failed to save data to disk: {e}")
        #         print(e)
        #         raise e


if __name__ == "__main__":
    from skellyblender.tests.download_test_data import get_test_data_path

    recording_path_str_outer = get_test_data_path()
    pipeline = PurePythonPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")