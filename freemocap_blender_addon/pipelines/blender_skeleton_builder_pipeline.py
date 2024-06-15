from dataclasses import dataclass
from pathlib import Path

from freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import \
    create_empties_from_trajectories
from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.put_rigid_body_meshes_on_empties import \
    put_rigid_body_meshes_on_empties
from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.put_sphere_meshes_on_empties import \
    put_spheres_on_parented_empties
from freemocap_blender_addon.core_functions.rig.add_rig import add_rig
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import DEFAULT_TRACKER_TYPE, TrackerSourceType
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import PipelineConfig
from freemocap_blender_addon.pipelines.pure_python_pipeline import PurePythonPipeline
from freemocap_blender_addon.utilities.create_blender_formatted_name import create_blender_formatted_name
from freemocap_blender_addon.utilities.download_test_data import get_test_data_path
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class BlenderSkeletonBuilderPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE
    pipeline_config: PipelineConfig = PipelineConfig()

    @property
    def recording_name(self) -> str:
        return Path(self.recording_path_str).stem

    def run(self, show_all: bool = True, scale=.001):
        # Pure python stuff
        print("Loading freemocap data....")
        freemocap_data = PurePythonPipeline(recording_path_str=self.recording_path_str).run()
        empties = {}
        parents = {}

        if show_all:
            stages_to_show = freemocap_data.trajectories_by_stage
        else:
            stages_to_show = freemocap_data.keypoint_trajectories

        for stage, trajectories in stages_to_show.items():
            trajectories = self.blenderize_trajectories(trajectories=trajectories, scale=scale)

            parented_empties = create_empties_from_trajectories(keypoint_trajectories=trajectories,
                                                                parent_name=stage)

            put_spheres_on_parented_empties(parented_empties=parented_empties)

            put_rigid_body_meshes_on_empties(parented_empties=parented_empties,
                                             segment_definitions=freemocap_data.segment_definitions,
                                             )

            add_rig(
                segment_definitions=freemocap_data.segment_definitions,
                rig_name=f"{self.recording_name}_rig",
                parent_object=parented_empties.parent_object,
                config=self.pipeline_config.add_rig,
            )

def blenderize_trajectories(scale: float,
                            trajectories: dict) -> KeypointTrajectories:
    return {create_blender_formatted_name(original_name=key): value.trajectory_data * scale for key, value in
            trajectories.items()}


if __name__ == "__main__":
    recording_path_str_outer = get_test_data_path()
    pipeline = BlenderSkeletonBuilderPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")
