from dataclasses import dataclass

from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedTrajectories, BlenderizedSegmentDefinitions
from skelly_blender.core.blender_stuff.blenderizers.blenderize_name import blenderize_name
from skelly_blender.core.blender_stuff.blenderizers.blenderized_segment import BlenderizedSegmentDefinition
from skelly_blender.core.blender_stuff.blenderizers.blenderized_trajectory import BlenderizedTrajectory
from skelly_blender.core.pure_python.freemocap_data.freemocap_skeleton_data import FreemocapSkeletonData


@dataclass
class BlenderizedSkeletonData(FreemocapSkeletonData):
    trajectories: BlenderizedTrajectories
    segment_definitions: BlenderizedSegmentDefinitions

    @classmethod
    def from_freemocap_skeleton_data(cls, freemocap_skeleton_data: FreemocapSkeletonData) -> 'BlenderizedSkeletonData':
        blenderized_trajectories = {blenderize_name(name): BlenderizedTrajectory.from_trajectory(trajectory) for
                                    name, trajectory in freemocap_skeleton_data.trajectories.items()}
        blenderized_segments = {blenderize_name(name): BlenderizedSegmentDefinition.from_segment(segment) for
                                 name, segment in freemocap_skeleton_data.segment_definitions.items()}
        return cls(
            trajectories=blenderized_trajectories,
            segment_definitions=blenderized_segments
        )
