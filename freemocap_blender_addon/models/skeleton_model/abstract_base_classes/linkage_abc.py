from abc import ABC
from dataclasses import dataclass

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.keypoint_abc import KeypointDefinition
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.segments_abc import SegmentABC, \
    SimpleSegmentABC, CompoundSegmentABC
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.tracked_point_keypoint_types import \
    KeypointTrajectories


@dataclass
class LinkageABC(ABC):
    """
    A simple linkage comprises two Segments that share a common Keypoint.

    The distance from the linked keypoint is fixed relative to the keypoints in the same rigid body,
     but the distances between the unlinked keypoints may change.

     #for now these are all 'universal' (ball) joints. Later we can add different constraints
    """
    parent: SegmentABC
    children: [SegmentABC]
    # TODO - calculate the linked_point on instantiation rather than defining it manually
    linked_keypoint: [KeypointDefinition]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> KeypointDefinition:
        return self.parent.root

    def __post_init__(self):
        for body in [self.parent] + self.children:
            if isinstance(body, SimpleSegmentABC):
                if self.linked_keypoint.name not in [body.parent.name, body.child.name]:
                    raise ValueError(
                        f"Error instantiation Linkage: {self.name} - Common keypoint {self.linked_keypoint.name} not found in body {body}")
            elif isinstance(body, CompoundSegmentABC):
                if self.linked_keypoint.name not in [body.parent.name] + [child.name for child in body.children]:
                    raise ValueError(
                        f"Error instantiation Linkage: {self.name} - Common keypoint {self.linked_keypoint.name} not found in body {body}")
            else:
                raise ValueError(f"Body {body} is not a valid rigid body type")
        print(f"Linkage: {self.name} instantiated with parent {self.parent} and children {self.children}")

    def get_segments(self) -> [SegmentABC]:
        segments = [self.parent] + self.children
        return segments

    def __str__(self) -> str:
        out_str = super().__str__()
        out_str += "\n\t".join(f"Common Keypoints: {self.linked_keypoint}\n")
        return out_str
