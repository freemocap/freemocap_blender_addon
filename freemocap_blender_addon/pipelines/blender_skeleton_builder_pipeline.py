from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

import numpy as np

from freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import \
    create_empties_from_trajectories
from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.put_rigid_body_meshes_on_empties import \
    put_rigid_body_meshes_on_empties
from freemocap_blender_addon.core_functions.rig.add_rig import generate_rig
from freemocap_blender_addon.freemocap_data.tracker_and_data_types import DEFAULT_TRACKER_TYPE, TrackerSourceType
from freemocap_blender_addon.pipelines.pipeline_parameters.pipeline_parameters import PipelineConfig
from freemocap_blender_addon.pipelines.pure_python_pipeline import PurePythonPipeline
from freemocap_blender_addon.utilities.blenderize_name import blenderize_name
from freemocap_blender_addon.utilities.download_test_data import get_test_data_path
from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class BlenderSkeletonBuilderPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE
    pipeline_config: PipelineConfig = field(default_factory=PipelineConfig)

    @property
    def recording_name(self) -> str:
        return Path(self.recording_path_str).stem

    def run(self, show_stages: bool = True, scale=.001):
        # Pure python stuff
        print("Loading freemocap data....")
        freemocap_data = PurePythonPipeline(recording_path_str=self.recording_path_str).run()

        if show_stages:
            stages_to_show = freemocap_data.trajectories_by_stage
        else:
            stages_to_show = freemocap_data.keypoint_trajectories

        for stage, trajectories in stages_to_show.items():
            trajectories = blenderize_trajectories(trajectories=trajectories, scale=scale)

            parented_empties = create_empties_from_trajectories(trajectories=trajectories,
                                                                parent_name=stage)
            # put_spheres_on_parented_empties(parented_empties=parented_empties)
            blenderized_segment_definitions = {}
            for segment_name, segment_definition in freemocap_data.segment_definitions.items():
                blenderized_name = blenderize_name(segment_name)
                blenderized_segment = segment_definition
                blenderized_segment.name = blenderize_name(blenderized_segment.name)
                blenderized_segment.parent = blenderize_name(blenderized_segment.parent)
                blenderized_segment.child = blenderize_name(blenderized_segment.child)
                blenderized_segment_definitions[blenderized_name] = blenderized_segment

            put_rigid_body_meshes_on_empties(parented_empties=parented_empties,
                                             segment_definitions=blenderized_segment_definitions,
                                             )

            generate_rig(
                rig_name=f"{self.recording_name}_rig",
                segment_definitions=blenderized_segment_definitions,
                parent_object=parented_empties.parent_object,
                config=self.pipeline_config.add_rig,
            )
        print(f"Finished building blender skeleton for recording: {self.recording_name}")


def blenderize_trajectories(scale: float,
                            trajectories: dict) -> Dict[str, np.ndarray]:
    return {blenderize_name(original_name=key): value.trajectory_data * scale for key, value in
            trajectories.items()}


if __name__ == "__main__":
    recording_path_str_outer = get_test_data_path()
    pipeline = BlenderSkeletonBuilderPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")
