from dataclasses import dataclass

from skellyblender.core.needs_bpy.blender_type_hints import BlenderizedTrajectories, BlenderizedSegmentDefinitions
from skellyblender.core.needs_bpy.blenderizers.blenderize_name import blenderize_name
from skellyblender.core.needs_bpy.blenderizers.blenderized_segment import BlenderizedSegmentDefinition
from skellyblender.core.needs_bpy.blenderizers.blenderized_trajectory import BlenderizedTrajectory
from skellyblender.core.pure_python.custom_types.derived_types import Trajectories, RigidBodyDefinitions
from skellyblender.core.pure_python.freemocap_data.freemocap_skeleton_data import FreemocapSkeletonData


@dataclass
class BlenderizedSkeletonData(FreemocapSkeletonData):
    trajectories: BlenderizedTrajectories
    segment_definitions: BlenderizedSegmentDefinitions
    parent_name: str

    @classmethod
    def create(cls,
               trajectories: Trajectories,
               rigid_body_definitions: RigidBodyDefinitions,
               parent_name: str) -> 'BlenderizedSkeletonData':
        blenderized_trajectories = {
            parentify_name(blenderize_name(name), parent_name=parent_name): BlenderizedTrajectory.from_trajectory(
                trajectory) for
            name, trajectory in trajectories.items()}

        blenderized_segments = {
            parentify_name(blenderize_name(name),
                           parent_name=parent_name): BlenderizedSegmentDefinition.from_segment(segment) for
            name, segment in rigid_body_definitions.items()}
        return cls(
            trajectories=blenderized_trajectories,
            segment_definitions=blenderized_segments,
            parent_name=parent_name
        )

    def __str__(self):
        trajectory_str = "\n\t\t".join([f"{name}: {trajectory}" for name, trajectory in self.trajectories.items()])
        segment_str = "\n\t\t".join([f"{name}: {segment}" for name, segment in self.segment_definitions.items()])
        return f"BlenderizedSkeletonData:\n\tTrajectories:{trajectory_str}\n\tSegments:{segment_str}"


def parentify_name(name: str, parent_name: str) -> str:
    return f"[{parent_name}]{name}"


def deparentify_name(name: str) -> str:
    return name.split("]")[1]
