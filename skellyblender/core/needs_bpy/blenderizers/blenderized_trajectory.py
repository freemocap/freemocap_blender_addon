from dataclasses import dataclass

from skellyblender.core.pure_python.custom_types.generic_types import BlenderizedName
from skellyblender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import Trajectory


@dataclass
class BlenderizedTrajectory(Trajectory):
    name: BlenderizedName

    @classmethod
    def from_trajectory(cls, trajectory: Trajectory) -> 'BlenderizedTrajectory':
        return cls(
            name=trajectory.name,
            trajectory_fr_xyz=trajectory.trajectory_fr_xyz
        )

    def __str__(self):
        super_str = super().__str__()
        return super_str.replace("Trajectory", "BlenderizedTrajectory")
