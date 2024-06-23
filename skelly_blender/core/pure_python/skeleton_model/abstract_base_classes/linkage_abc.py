from abc import ABC
from dataclasses import dataclass
from typing import List

from skelly_blender.core.pure_python.custom_types.base_enums import SegmentEnum, LinkageEnum
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.keypoint_abc import KeypointDefinition
from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.segments_abc import SimpleSegmentABC, \
    CompoundSegmentABC


@dataclass
class LinkageABC(ABC):
    """
    A simple linkage comprises two Segments that share a common Keypoint.

    The distance from the linked keypoint is fixed relative to the keypoints in the same rigid body,
     but the distances between the unlinked keypoints may change.

     #for now these are all 'universal' (ball) joints. Later we can add different constraints
    """
    parent: LinkageEnum
    children: List[LinkageEnum]
    # TODO - calculate the linked_point on instantiation rather than defining it manually
    linked_keypoint: [KeypointDefinition]

    def get_name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> KeypointDefinition:
        return self.parent.value.root

    def __post_init__(self):
        for body in [self.parent] + self.children:
            if isinstance(body.value, SimpleSegmentABC):
                if self.linked_keypoint.name not in [body.value.origin.name, body.value.z_axis_reference.name]:
                    raise ValueError(
                        f"Error instantiation Linkage: {self.get_name()} - Common keypoint {self.linked_keypoint.name} not found in body {body}")
            elif isinstance(body.value, CompoundSegmentABC):
                if self.linked_keypoint.name not in [body.value.parent.name] + [child.name for child in body.value.children]:
                    raise ValueError(
                        f"Error instantiation Linkage: {self.get_name()} - Common keypoint {self.linked_keypoint.name} not found in body {body}")
            else:
                raise ValueError(f"Body {body} is not a valid rigid body type")
        print(f"Linkage: {self.get_name()} instantiated with parent {self.parent} and children {self.children}")

    @classmethod
    def get_segments(cls) -> List[SegmentEnum]:
        segments = [cls.parent] + cls.children
        return segments

    @classmethod
    def get_keypoints(cls) -> [KeypointDefinition]:
        keypoints = cls.parent.value.get_keypoints()
        for linkage in cls.children:
            keypoints.extend(linkage.value.get_keypoints())
        return keypoints

    def __str__(self) -> str:
        out_str = super().__str__()
        out_str += "\n\t".join(f"Common Keypoints: {self.linked_keypoint}\n")
        return out_str
