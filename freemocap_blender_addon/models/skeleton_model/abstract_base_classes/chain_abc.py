from abc import ABC
from typing import List, Dict

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.keypoint_abc import Keypoint
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.linkage_abc import LinkageABC
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.segments_abc import SegmentABC
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories


class ChainABC(ABC):
    """
    A Chain is a set of linkages that are connected via shared Segments.
    """
    parent: LinkageABC
    children: List[LinkageABC]
    # TODO - calculate the linked_point on instanciation rather than defining it manually
    shared_segments: List[SegmentABC]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> Keypoint:
        # Chain -> Linkage -> Segment -> Keypoint
        return self.parent.root

    def __post_init__(self):
        for body in self.shared_segments:
            if not any(body == linkage.parent for linkage in self.children):
                raise ValueError(f"Shared segment {body.name} not found in children {self.children}")
        print(
            f"Chain: {self.name} instantiated with parent {self.parent} and children {[child.name for child in self.children]}")

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: KeypointTrajectories):
        """
        Create a ChainABC instance from trajectory data.

        Parameters
        ----------
        keypoint_trajectories : Dict[str, np.ndarray]
            A dictionary of KeypointTrajectories.

        Returns
        -------
        ChainABC
            An instance of ChainABC hydrated with KeypointTrajectories.
        """

        cls.parent = cls.parent.from_keypoint_trajectories(keypoint_trajectories)
        cls.children = [child.from_keypoint_trajectories(keypoint_trajectories) for child in cls.children]

        return cls
