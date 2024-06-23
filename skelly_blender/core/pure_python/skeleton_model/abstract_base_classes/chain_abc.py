from abc import ABC
from typing import List

from skelly_blender.core.pure_python.custom_types.base_enums import LinkageEnum, KeypointEnum, SegmentEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SegmentABC


class ChainABC(ABC):
    """
    A Chain is a set of linkages that are connected via shared Segments.
    """
    parent: LinkageEnum
    children: List[LinkageEnum]
    # TODO - calculate the linked_point on instancing rather than defining it manually
    shared_segments: List[SegmentABC]

    @property
    def root(self) -> KeypointEnum:
        # Chain -> Linkage -> Segment -> Keypoint
        return self.parent.value.root

    def get_name(self):
        return self.__class__.__name__

    def __post_init__(self):
        for body in self.shared_segments:
            if not any(body == linkage.value.origin for linkage in self.children):
                raise ValueError(f"Shared segment {body.name} not found in children {self.children}")
        print(
            f"Chain: {self.get_name()} instantiated with parent {self.parent} and children {[child.name for child in self.children]}")

    @classmethod
    def get_keypoints(cls) -> List[KeypointEnum]:
        keypoints = cls.parent.value.get_keypoints()
        for linkage in cls.children:
            keypoints.extend(linkage.value.get_keypoints())
        return keypoints

    @classmethod
    def get_segments(cls) -> List[SegmentEnum]:
        segments = cls.parent.value.get_segments()
        for linkage in cls.children:
            segments.extend(linkage.value.get_segments())
        return segments

    def get_linkages(self) -> List[LinkageEnum]:
        linkages = [self.parent]
        linkages.extend(self.children)
        return linkages
