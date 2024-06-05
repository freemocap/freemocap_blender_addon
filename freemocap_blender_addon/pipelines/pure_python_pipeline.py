import traceback
from pathlib import Path
from typing import Optional

from freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler
from freemocap_blender_addon.freemocap_data_handler.helpers.saver import FreemocapDataSaver
from freemocap_blender_addon.freemocap_data_handler.operations.enforce_rigid_bodies.enforce_rigid_bodies import \
    enforce_rigid_bodies
from freemocap_blender_addon.freemocap_data_handler.operations.fix_hand_data import fix_hand_data
from freemocap_blender_addon.freemocap_data_handler.operations.put_skeleton_on_ground import put_skeleton_on_ground
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import PipelineConfig
from freemocap_blender_addon.utilities.singleton_metaclass import SingletonMetaClass


class PurePythonController(metaclass=SingletonMetaClass):
    def __init__(self, recording_path: str, blend_file_path_str: str, pipeline_config: PipelineConfig):
        self.pipeline_config: PipelineConfig = pipeline_config
        self.recording_path_str: str = recording_path
        self.recording_name = Path(self.recording_path_str).stem
        self._output_video_path = str(Path(self.blend_file_path_str).parent / f"{self.recording_name}_video_output.mp4")
        self.freemocap_data_handler: Optional[FreemocapDataHandler] = None

    def load_freemocap_data(self):
        try:
            print("Loading freemocap data....")
            self.freemocap_data_handler = load_freemocap_data(recording_path=self.recording_path_str)
        except Exception as e:
            print(f"Failed to load freemocap data: {e}")
            raise e

    def calculate_virtual_trajectories(self):
        try:
            print("Calculating virtual trajectories....")
            self.freemocap_data_handler.calculate_virtual_trajectories()
            self.freemocap_data_handler.mark_processing_stage("add_virtual_trajectories")
        except Exception as e:
            print(f"Failed to calculate virtual trajectories: {e}")
            print(e)
            raise e

    def put_data_in_inertial_reference_frame(self):
        try:
            print("Putting freemocap data in inertial reference frame....")
            put_skeleton_on_ground(handler=self.freemocap_data_handler)
        except Exception as e:
            print(f"Failed to put freemocap data in inertial reference frame: {e}")
            print(traceback.format_exc())
            raise e

    def enforce_rigid_bones(self):
        print("Enforcing rigid bones...")
        try:
            self.freemocap_data_handler = enforce_rigid_bodies(handler=self.freemocap_data_handler)
        except Exception as e:
            print(f"Failed during `enforce rigid bones`, error: `{e}`")
            print(e)
            raise e

    def fix_hand_data(self):
        try:
            print("Fixing hand data...")
            self.freemocap_data_handler = fix_hand_data(handler=self.freemocap_data_handler)
        except Exception as e:
            print(f"Failed during `fix hand data`, error: `{e}`")
            print(e)
            raise e

    def save_data_to_disk(self):
        try:
            print("Saving data to disk...")
            FreemocapDataSaver(handler=self.freemocap_data_handler).save(recording_path=self.recording_path_str)
        except Exception as e:
            print(f"Failed to save data to disk: {e}")
            print(e)
            raise e

    def run_all(self):
        print("Running all stages...")

        # Pure python stuff
        self.load_freemocap_data()
        self.calculate_virtual_trajectories()
        self.put_data_in_inertial_reference_frame()
        self.enforce_rigid_bones()
        self.fix_hand_data()
        self.save_data_to_disk()
