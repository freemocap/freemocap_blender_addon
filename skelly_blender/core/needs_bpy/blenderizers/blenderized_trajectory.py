from dataclasses import dataclass

from skelly_blender.core.pure_python.custom_types.generic_types import BlenderizedName
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import TrajectoryABC


@dataclass
class BlenderizedTrajectory(TrajectoryABC):
    name: BlenderizedName

    @classmethod
    def from_trajectory(cls, trajectory: TrajectoryABC) -> 'BlenderizedTrajectory':
        return cls(
            name=trajectory.name,
            trajectory_data=trajectory.trajectory_data
        )

    def __str__(self):
        super_str = super().__str__()
        return super_str.replace("Trajectory", "BlenderizedTrajectory")
