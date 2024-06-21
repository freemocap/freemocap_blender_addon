from dataclasses import dataclass

from skelly_blender.core.custom_types import BlenderizedName
from skelly_blender.core.skeleton_model.abstract_base_classes import Trajectory


@dataclass
class BlenderizedTrajectory(Trajectory):
    name: BlenderizedName

    @classmethod
    def from_trajectory(cls, trajectory: Trajectory) -> 'BlenderizedTrajectory':
        return cls(
            name=trajectory.name,
            trajectory_data=trajectory.trajectory_data
        )

