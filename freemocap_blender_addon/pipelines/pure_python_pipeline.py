from dataclasses import dataclass

from freemocap_blender_addon.freemocap_data.freemocap_recording_data import FreemocapRecordingData
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import DEFAULT_TRACKER_TYPE, TrackerSourceType
from freemocap_blender_addon.freemocap_data_handler.operations.put_skeleton_on_ground import put_skeleton_on_ground
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    calculate_rigid_body_trajectories
from freemocap_blender_addon.models.skeleton_model import SkeletonTypes
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import PipelineConfig
from freemocap_blender_addon.utilities.download_test_data import get_test_data_path
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class PurePythonPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE
    print("Running all stages...")

    def run(self):
        # Pure python stuff
        print("Loading freemocap data....")
        recording_data = FreemocapRecordingData.load_from_recording_path(recording_path=self.recording_path_str,
                                                                         tracker_type=self.tracker_type)

        og_keypoint_trajectories = recording_data.body.map_to_keypoints()

        rigidified_keypoint_trajectories, segment_length_statistics = calculate_rigid_body_trajectories(
            keypoint_trajectories=og_keypoint_trajectories,
            skeleton_definition=SkeletonTypes.BODY_ONLY)

        inertial_aligned_keypoints = put_skeleton_on_ground(keypoint_trajectories=rigidified_keypoint_trajectories)
        f=9
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
    pipeline_config_outer = PipelineConfig()
    recording_path_str_outer = get_test_data_path()
    pipeline = PurePythonPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")
