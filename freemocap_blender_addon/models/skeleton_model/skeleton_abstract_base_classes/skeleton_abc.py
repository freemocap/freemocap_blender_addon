from abc import ABC
from dataclasses import dataclass
from typing import List, Set

from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.keypoint_abc import KeypointDefinition
from freemocap_blender_addon.models.skeleton_model.skeleton_abstract_base_classes.segments_abc import SimpleSegmentABC


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

    @classmethod
    def get_segments(cls) -> List[SimpleSegmentABC]:

        segments = []
        segments.extend(cls.parent.get_segments())
        for chain in cls.children:
            segments.extend(chain.get_segments())
        return list(set(segments))

    @classmethod
    def get_keypoints(cls) -> List[KeypointDefinition]:
        keypoints = []
        for chain in cls.children:
            keypoints.extend(chain.get_keypoints())
        return keypoints

    @classmethod
    def get_keypoint_children(cls, keypoint_name: str) -> List[KeypointDefinition]:
        """
        Recursively get all children keypoints for a given keypoint name.

        Parameters
        ----------
        keypoint_name : str
            The name of the keypoint to find children for.

        Returns
        -------
        Set[KeypointDefinition]
            A set of all children keypoints.
        """
        def recursive_find_children(name: str,
                                    segments: List[SimpleSegmentABC],
                                    found_children: Set[KeypointDefinition]) -> None:
            for segment in segments:
                if segment.value.parent.name.lower() == name:
                    children = segment.value.get_children()
                    for child in children:
                        if child not in found_children:  # Avoid infinite recursion
                            found_children.add(child)
                            recursive_find_children(name=child.name.lower(),
                                                    segments=segments,
                                                    found_children=found_children)

        found_children = set()
        recursive_find_children(keypoint_name,
                                cls.get_segments(),
                                found_children)
        return list(found_children)
