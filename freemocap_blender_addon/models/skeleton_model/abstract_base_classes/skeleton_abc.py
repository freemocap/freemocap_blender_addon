from abc import ABC
from dataclasses import dataclass
from typing import List, Dict

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.keypoint_abc import Keypoint, \
    KeypointTrajectory
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories


@dataclass
class SkeletonABC(ABC):
    """
    A Skeleton is composed of chains with connecting KeyPoints.
    """
    parent: ChainABC
    children: List[ChainABC]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> Keypoint:
        # Skeleton -> Chain -> Linkage -> Segment -> Keypoint
        return self.parent.root

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: KeypointTrajectories):
        """
        Create a SkeletonABC instance from trajectory data.

        Parameters
        ----------
        keypoint_trajectories : Dict[str, np.ndarray]
            A dictionary of KeypointTrajectories.

        Returns
        -------
        SkeletonABC
            An instance of SkeletonABC hydrated with KeypointTrajectories.
        """

        parent = cls.parent.from_keypoint_trajectories(keypoint_trajectories)
        children = [child.from_keypoint_trajectories(keypoint_trajectories) for child in cls.children]

        return cls(parent=parent, children=children)
