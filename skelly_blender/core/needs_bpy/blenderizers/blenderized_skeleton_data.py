from dataclasses import dataclass

from skelly_blender.core.needs_bpy.blender_type_hints import BlenderizedTrajectories, BlenderizedSegmentDefinitions
from skelly_blender.core.needs_bpy.blenderizers.blenderize_name import blenderize_name
from skelly_blender.core.needs_bpy.blenderizers.blenderized_segment import BlenderizedSegmentDefinition
from skelly_blender.core.needs_bpy.blenderizers.blenderized_trajectory import BlenderizedTrajectory
from skelly_blender.core.pure_python.custom_types.derived_types import Trajectories, RigidBodyDefinitions
from skelly_blender.core.pure_python.freemocap_data.freemocap_skeleton_data import FreemocapSkeletonData


@dataclass
class BlenderizedSkeletonData(FreemocapSkeletonData):
    trajectories: BlenderizedTrajectories
    segment_definitions: BlenderizedSegmentDefinitions

    @classmethod
    def create(cls, trajectories: Trajectories,
               rigid_body_definitions: RigidBodyDefinitions) -> 'BlenderizedSkeletonData':
        blenderized_trajectories = {blenderize_name(name): BlenderizedTrajectory.from_trajectory(trajectory) for
                                    name, trajectory in trajectories.items()}
        blenderized_segments = {blenderize_name(name): BlenderizedSegmentDefinition.from_segment(segment) for
                                name, segment in rigid_body_definitions.items()}
        return cls(
            trajectories=blenderized_trajectories,
            segment_definitions=blenderized_segments
        )

    def __str__(self):
        trajectory_str = "\n\t\t".join([f"{name}: {trajectory}" for name, trajectory in self.trajectories.items()])
        segment_str = "\n\t\t".join([f"{name}: {segment}" for name, segment in self.segment_definitions.items()])
        return f"BlenderizedSkeletonData:\n\tTrajectories:{trajectory_str}\n\tSegments:{segment_str}"