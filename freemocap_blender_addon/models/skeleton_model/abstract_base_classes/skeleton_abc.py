from abc import ABC
from dataclasses import dataclass
from typing import List

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.keypoint_abc import KeypointDefinition
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.segments_abc import SegmentABC


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
    def root(self) -> KeypointDefinition:
        # Skeleton -> Chain -> Linkage -> Segment -> Keypoint
        return self.parent.root

    def get_segments(self) -> List[SegmentABC]:

        segments = []
        for chain in self.children:
            segments.extend(chain.get_segments())
        return segments

