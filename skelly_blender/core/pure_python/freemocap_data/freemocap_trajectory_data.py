from dataclasses import dataclass
from typing import Dict, Union, cast

from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedTrajectories, BlenderizedTrajectory, \
    BlenderizedSegmentDefinitions
from skelly_blender.core.blender_stuff.blenderizable_enum import blenderize_name
from skelly_blender.core.pure_python.generic_type_hints import Trajectories, RigidSegmentDefinitions
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class FreemocapTrajectoryData(TypeSafeDataclass):
    raw_from_disk: Trajectories
    rigidified: Trajectories
    inertial_aligned: Trajectories
    segment_definitions: RigidSegmentDefinitions

    def get_trajectories_by_stage(self, blenderize_names: bool) -> Dict[str, Trajectories]:
        if blenderize_names:
            return {"raw_from_disk": self._blenderize_names(self.raw_from_disk),
                    "rigidified": self._blenderize_names(self.rigidified),
                    "inertial_aligned": self._blenderize_names(self.inertial_aligned)}
        else:
            return {"raw_from_disk": self.raw_from_disk,
                    "rigidified": self.rigidified,
                    "inertial_aligned": self.inertial_aligned}

    def get_keypoint_trajectories(self, blenderize_names: bool) -> Union[Trajectories, BlenderizedTrajectories]:
        """
        Returns the keypoint trajectories at the most processed stage
        """
        if blenderize_names:
            return self._blenderize_names(self.inertial_aligned)
        else:
            return self.inertial_aligned

    def _blenderize_names(self, keypoint_trajectories: Trajectories) -> BlenderizedTrajectories:
        return {blenderize_name(key): cast(BlenderizedTrajectory, keypoint_trajectories[key]) for key in
                keypoint_trajectories.keys()}

    def get_blenderized_segment_definitions(self) -> BlenderizedSegmentDefinitions:
        blenderized_segment_definitions = {}
        for segment_name, segment_definition in self.segment_definitions.items():
            blenderized_segment_definitions[blenderize_name(segment_name)] = segment_definition.blenderize()

        return blenderized_segment_definitions
