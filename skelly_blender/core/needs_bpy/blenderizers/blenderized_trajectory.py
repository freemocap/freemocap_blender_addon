from dataclasses import dataclass

from skelly_blender.core.pure_python.custom_types import BlenderizedName
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.trajectory_abc import TrajectoryABC


@dataclass
class BlenderizedTrajectoryABC(TrajectoryABC):
    name: BlenderizedName

    @classmethod
    def from_trajectory(cls, trajectory: TrajectoryABC) -> 'BlenderizedTrajectoryABC':
        return cls(
            name=trajectory.name,
            trajectory_data=trajectory.trajectory_data
        )

