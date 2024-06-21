from dataclasses import dataclass, field
from pathlib import Path

from old.freemocap_blender_addon.core_functions.rig.add_rig import apply_bone_constraints
from skelly_blender.core.blender_stuff.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skelly_blender.core.blender_stuff.armature_rig.armature.generate_armature import generate_armature
from skelly_blender.core.blender_stuff.blenderizers.blenderized_skeleton_data import BlenderizedSkeletonData
from skelly_blender.core.blender_stuff.keyframed_empties.create_keyframed_empties import create_keyframed_empties
from skelly_blender.core.blender_stuff.rigid_body_meshes.put_rigid_body_meshes_on_empties import \
    put_rigid_body_meshes_on_empties
from skelly_blender.core.tracked_points.tracker_sources.tracker_source_types import DEFAULT_TRACKER_TYPE, \
    TrackerSourceType
from skelly_blender.core.utility_classes import TypeSafeDataclass
from skelly_blender.pipelines.blender_pipeline_config import PipelineConfig
from skelly_blender.pipelines.pure_python_pipeline import PurePythonPipeline
from skelly_blender.tests.download_test_data import get_test_data_path


@dataclass
class BlenderSkeletonBuilderPipeline(TypeSafeDataclass):
    recording_path_str: str
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE
    pipeline_config: PipelineConfig = field(default_factory=PipelineConfig)

    @property
    def recording_name(self) -> str:
        return Path(self.recording_path_str).stem

    def run(self, show_stages: bool = False, scale=.001):
        print("Loading freemocap data....")
        freemocap_skeleton_data = PurePythonPipeline(recording_path_str=self.recording_path_str).run(scale=scale)
        blenderized_data = BlenderizedSkeletonData.from_freemocap_skeleton_data(
            freemocap_skeleton_data=freemocap_skeleton_data)

        parented_empties = create_keyframed_empties(trajectories=blenderized_data.trajectories,
                                                    parent_name=self.recording_name, )

        put_rigid_body_meshes_on_empties(parented_empties=parented_empties,
                                         segment_definitions=blenderized_data.segment_definitions,
                                         )

        print("Generating armature from segment lengths and rest pose definitions...")

        armature_definition = ArmatureDefinition.create(
            armature_name=f"{self.recording_name}_armature",
            segment_definitions=blenderized_data.segment_definitions,
            pose_definition=self.pipeline_config.add_rig.rest_pose_definition,
            bone_constraints=self.pipeline_config.add_rig.bone_constraints,
        )
        armature = generate_armature(armature_definition=armature_definition)

        # attach_skelly_bone_meshes(
        #     armature=armature,
        #     armature_definition=armature_definition,
        # )

        rig = apply_bone_constraints(
            armature=armature,
            config=self.pipeline_config.add_rig,
        )

        print(f"Finished building blender skeleton for recording: {self.recording_name}")


if __name__ == "__main__":
    recording_path_str_outer = get_test_data_path()
    pipeline = BlenderSkeletonBuilderPipeline(recording_path_str=recording_path_str_outer)
    pipeline.run()
    print("All done!")
