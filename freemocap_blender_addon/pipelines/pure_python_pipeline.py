from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from freemocap_blender_addon.freemocap_data.freemocap_recording_data import FreemocapRecordingData
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import DEFAULT_TRACKER_TYPE, TrackerSourceType
from freemocap_blender_addon.freemocap_data_handler.operations.put_skeleton_on_ground import put_skeleton_on_ground
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    calculate_rigid_body_trajectories, RigidSegmentDefinitions
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories
from freemocap_blender_addon.utilities.download_test_data import get_test_data_path
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class DataStages(TypeSafeDataclass):
    raw_from_disk: KeypointTrajectories
    rigidified: KeypointTrajectories
    inertial_aligned: KeypointTrajectories
    segment_definitions: RigidSegmentDefinitions

    @property
    def trajectories_by_stage(self) -> Dict[str, KeypointTrajectories]:
        return {"raw_from_disk": self.raw_from_disk,
                "rigidified": self.rigidified,
                "inertial_aligned": self.inertial_aligned}

    @property
    def keypoint_trajectories(self) -> Dict[str, KeypointTrajectories]:
        """
        Returns the keypoint trajectories at the most processed stage
        """
        return {"inertial_aligned": self.inertial_aligned}


@dataclass
class PurePythonPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE

    @property
    def recording_name(self) -> str:
        return Path(self.recording_path_str).stem

    def run(self):
        # Pure python stuff
        print("Loading freemocap data....")
        recording_data = FreemocapRecordingData.load_from_recording_path(recording_path=self.recording_path_str,
                                                                         tracker_type=self.tracker_type)

        print("Mapping body to keypoints....")
        og_keypoint_trajectories = recording_data.body.map_to_keypoints()

        print("Calculating rigid body trajectories....")
        rigidified_keypoint_trajectories, rigid_body_definitions = calculate_rigid_body_trajectories(
            keypoint_trajectories=og_keypoint_trajectories,
            skeleton_definition=SkeletonTypes.BODY_ONLY)

        print("Putting skeleton on ground....")
        inertial_aligned_keypoint_trajectories = put_skeleton_on_ground(
            keypoint_trajectories=rigidified_keypoint_trajectories)

        print(f"{self.__class__.__name__}.run() completed successfully for recording: {self.recording_name}")
        return DataStages(raw_from_disk=og_keypoint_trajectories,
                          rigidified=rigidified_keypoint_trajectories,
                          inertial_aligned=inertial_aligned_keypoint_trajectories,
                          segment_definitions=rigid_body_definitions)

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
    recording_path_str_outer = get_test_data_path()
    pipeline = PurePythonPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")
