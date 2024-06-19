from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

import numpy as np



from skelly_blender.core.pure_python.blender_stuff.keyframed_empties.create_keyframed_empties import \
    create_empties_from_trajectories
from skelly_blender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import DEFAULT_TRACKER_TYPE, \
    TrackerSourceType
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass
from skelly_blender.pipelines.blender_pipeline_config import PipelineConfig
from skelly_blender.pipelines.pure_python_pipeline import PurePythonPipeline


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
        freemocap_data = PurePythonPipeline(recording_path_str=self.recording_path_str, scale_data=scale).run()

        if show_stages:
            stages_to_show = freemocap_data.trajectories_by_stage
        else:
            stages_to_show = freemocap_data.keypoint_trajectories

        for stage, trajectories in stages_to_show.items():
            trajectories = blenderize_trajectories(trajectories=trajectories, scale=scale)

            parented_empties = create_empties_from_trajectories(trajectories=trajectories,
                                                                parent_name=stage)
            # put_spheres_on_parented_empties(parented_empties=parented_empties)
            # blenderized_segment_definitions = {}
            # for segment_name, segment_definition in freemocap_data.segment_definitions.items():
            #     blenderized_name = blenderize_name(segment_name)
            #     blenderized_segment = segment_definition
            #     blenderized_segment.name = blenderize_name(blenderized_segment.name)
            #     blenderized_segment.parent = blenderize_name(blenderized_segment.parent)
            #     blenderized_segment.child = blenderize_name(blenderized_segment.child)
            #     blenderized_segment_definitions[blenderized_name] = blenderized_segment

            put_rigid_body_meshes_on_empties(parented_empties=parented_empties,
                                             segment_definitions=blenderized_segment_definitions,
                                             )

            print("Generating armature from segment lengths and rest pose definitions...")
            armature_definition = ArmatureDefinition.create(
                armature_name=f"{self.recording_name}_armature",
                segment_definitions=blenderized_segment_definitions,
                pose_definition=self.pipeline_config.add_rig.rest_pose_definition,
                bone_constraints=self.pipeline_config.add_rig.bone_constraints,
            )
            armature = generate_armature(armature_definition=armature_definition)

            # attach_skelly_bone_meshes(
            #     armature=armature,
            #     armature_definition=armature_definition,
            # )

            rig = generate_rig(
                armature=armature,
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
