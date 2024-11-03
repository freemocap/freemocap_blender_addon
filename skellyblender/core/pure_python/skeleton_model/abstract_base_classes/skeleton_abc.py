from abc import ABC
from dataclasses import dataclass
from typing import List, Set

from skellyblender.core.pure_python.custom_types.base_enums import ChainEnum, SegmentEnum
from skellyblender.core.pure_python.skeleton_model.abstract_base_classes.keypoint_abc import KeypointDefinition
from skellyblender.core.pure_python.skeleton_model.abstract_base_classes.linkage_abc import LinkageABC


@dataclass
class SkeletonABC(ABC):
    """
    A Skeleton is composed of chains with connecting KeyPoints.
    """
    parent: ChainEnum
    children: List[ChainEnum]

    def get_name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> KeypointDefinition:
        # Skeleton -> Chain -> Linkage -> Segment -> Keypoint
        return self.parent.value.root

    @classmethod
    def get_linkages(cls) -> List[LinkageABC]:
        linkages = []
        linkages.extend(cls.parent.value.get_linkages())
        for chain in cls.children:
            linkages.extend(chain.value.get_linkages())
        return list(set(linkages))

    @classmethod
    def get_segments(cls) -> List[SegmentEnum]:

        segments = []
        segments.extend(cls.parent.value.get_segments())
        for chain in cls.children:
            segments.extend(chain.value.get_segments())
        return list(set(segments))

    @classmethod
    def get_keypoints(cls) -> List[KeypointDefinition]:
        keypoints = []
        for chain in cls.children:
            keypoints.extend(chain.value.get_keypoints())
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
                                    segments: List[SegmentEnum],
                                    found_keypoint_children: Set[KeypointDefinition]) -> None:
            for segment in segments:
                if segment.value.origin.lower() == name:
                    children = segment.value.get_children()
                    for child in children:
                        if child not in found_keypoint_children:  # Avoid infinite recursion
                            found_keypoint_children.add(child)
                            recursive_find_children(name=child.lower(),
                                                    segments=segments,
                                                    found_keypoint_children=found_keypoint_children)

        found_keypoint_children = set()
        recursive_find_children(name=keypoint_name,
                                segments=cls.get_segments(),
                                found_keypoint_children=found_keypoint_children)
        return list(found_keypoint_children)
