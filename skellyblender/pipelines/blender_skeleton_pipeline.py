from dataclasses import dataclass, field
from pathlib import Path

from skellyblender.core.needs_bpy.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skellyblender.core.needs_bpy.armature_rig.armature.generate_armature import generate_armature
from skellyblender.core.needs_bpy.armature_rig.bone_constraints.apply_bone_constraints import apply_bone_constraints
from skellyblender.core.needs_bpy.blender_type_hints import ParentEmpty
from skellyblender.core.needs_bpy.blenderizers.blenderized_skeleton_data import BlenderizedSkeletonData
from skellyblender.core.needs_bpy.empties.create_keyframed_empties import create_keyframed_empties
from skellyblender.core.needs_bpy.empties.create_parent_empty import create_parent_empty
from skellyblender.core.needs_bpy.meshes.rigid_body_meshes.put_rigid_body_meshes_on_empties import \
    put_rigid_body_meshes_on_empties
from skellyblender.core.needs_bpy.meshes.skelly_bone_meshes.attach_skelly_bone_meshes import attach_skelly_bone_meshes
from skellyblender.core.pure_python.freemocap_data.freemocap_recording_data import FreemocapDataStages
from skellyblender.core.pure_python.tracked_points.tracker_sources.tracker_source_types import DEFAULT_TRACKER_TYPE, \
    TrackerSourceType
from skellyblender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass
from skellyblender.pipelines.blender_pipeline_config import PipelineConfig
from skellyblender.pipelines.pure_python_pipeline import PurePythonPipeline
from skellyblender.tests.download_test_data import get_test_data_path

FREEMOCAP_TO_METERS_SCALE_FACTOR = .001


@dataclass
class BlenderSkeletonBuilderPipeline(TypeSafeDataclass):
    recording_path_str: str
    parent_empty: ParentEmpty
    tracker_type: TrackerSourceType = DEFAULT_TRACKER_TYPE
    pipeline_config: PipelineConfig = field(default_factory=PipelineConfig)

    @property
    def recording_name(self) -> str:
        return Path(self.recording_path_str).stem

    def run(self, show_stages: bool = False, scale=FREEMOCAP_TO_METERS_SCALE_FACTOR):
        self._print_start_message()

        freemocap_data_stages: FreemocapDataStages = PurePythonPipeline(recording_path_str=self.recording_path_str).run(
            scale=scale)
        stages_to_show = {"only": freemocap_data_stages.most_processed_trajectories}
        if show_stages:
            stages_to_show = freemocap_data_stages.get_all_processing_stages()

        for stage_name, trajectories in stages_to_show.items():
            if show_stages:
                print(f"\n--------------------------------------------\n"
                      f"CREATING BLENDER SKELETON BASED ON PROCESSING STAGE: {stage_name}\n")
                stage_data_name = f"{stage_name}"
            else:
                stage_data_name = self.recording_name

            if "og" in stage_name:
                create_keyframed_empties(trajectories=trajectories,
                                         empty_type="PLAIN_AXES",
                                         parent_empty=self.parent_empty)
                continue

            print("\n--------------------------------------------\n"
                  "Blenderizing data....\n")
            blenderized_data = BlenderizedSkeletonData.create(
                trajectories=trajectories,
                rigid_body_definitions=freemocap_data_stages.rigid_body_definitions,
                parent_name=self.parent_empty.name,
            )

            print("\n--------------------------------------------\n"
                  "Creating keyframed empties....\n")

            parented_empties = create_keyframed_empties(trajectories=blenderized_data.trajectories,
                                                        parent_empty=self.parent_empty)

            print("\n--------------------------------------------\n"
                  "Creating rigid body meshes....\n")
            put_rigid_body_meshes_on_empties(parented_empties=parented_empties,
                                             segment_definitions=blenderized_data.segment_definitions,
                                             )

            print("Generating armature from segment lengths and rest pose definitions...")

            armature_definition = ArmatureDefinition.create(
                armature_name=f"{self.parent_empty.name}_armature",
                segment_definitions=blenderized_data.segment_definitions,
                pose_definition=self.pipeline_config.add_rig.rest_pose_definition,
                bone_constraints=self.pipeline_config.add_rig.bone_constraints,
            )

            print("\n--------------------------------------------\n"
                  f"Generating armature...\n")
            armature = generate_armature(armature_definition=armature_definition)

            print("\n--------------------------------------------\n"
                  f"Attaching skelly bone meshes to armature...\n")
            attach_skelly_bone_meshes(
                armature=armature,
                armature_definition=armature_definition,
            )
            return
            print("\n--------------------------------------------\n"
                  f"Applying bone constraints to armature...\n")
            rig = apply_bone_constraints(
                armature=armature,
                config=self.pipeline_config.add_rig,
                parent_name=self.parent_empty.name,
            )

        print(f"Finished building blender skeleton for recording:\n\t {self.recording_name}")

    def _print_start_message(self):
        print(f"\nRUNNING `{self.__class__.__name__}`: {self}...\n")

    def __str__(self):
        return f"{self.__class__.__name__}:\n\tRecording Path: {self.recording_path_str}\n\tTracker Type: {self.tracker_type}"


if __name__ == "__main__":
    recording_path_str_outer = get_test_data_path()

    pipeline = BlenderSkeletonBuilderPipeline(recording_path_str=recording_path_str_outer,
                                              parent_empty=create_parent_empty(
                                                  name=Path(recording_path_str_outer).stem))
    pipeline.run()
    print("All done!")

