from abc import ABC
from dataclasses import dataclass
from typing import List, Optional

from skelly_blender.core.pure_python.skeleton_model.abstract_base_classes.keypoint_abc import KeypointDefinition


@dataclass
class SegmentABC(ABC):
    """
    A RigigBody is a collection of keypoints that are linked together, such that the distance between them is constant.
    """
    parent: KeypointDefinition

    def __post_init__(self):
        if not isinstance(self.parent, KeypointDefinition):
            raise ValueError("Parent must be an instance of Keypoint")

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self):
        return self.parent


@dataclass
class SimpleSegmentABC(SegmentABC):
    """
    A simple rigid body is a Segment consisting of Two and Only Two keypoints that are linked together, the distance between them is constant.
    The parent keypoint defines the origin of the rigid body, and the child keypoint is the end of the rigid body.
    The primary axis (+X) of the rigid body is the vector from the parent to the child, the secondary and tertiary axes (+Y, +Z) are undefined (i.e. we have enough information to define the pitch and yaw, but not the roll).
    """
    parent: KeypointDefinition
    child: KeypointDefinition

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> KeypointDefinition:
        return self.parent

    def __post_init__(self):
        if not all(isinstance(keypoint, KeypointDefinition) for keypoint in [self.parent, self.child]):
            raise ValueError("Parent and child keypoints must be instances of Keypoint")
        if self.parent == self.child:
            raise ValueError("Parent and child keypoints must be different")
        print(f"SimpleSegment: {self.name} instantiated with parent {self.parent} and child {self.child}")

    @classmethod
    def get_children(cls) -> List[KeypointDefinition]:
        return [cls.child]

    def __str__(self):
        out_str = f"Segment: {self.name}"
        out_str += f"\n\tParent: {self.parent}"
        return out_str


@dataclass
class CompoundSegmentABC(SegmentABC):
    """
    A composite rigid body is a collection of keypoints that are linked together, such that the distance between all keypoints is constant.
    The parent keypoint is the origin of the rigid body
    The primary and secondary axes must be defined in the class, and will be used to calculate the orthonormal basis of the rigid body
    """
    segments = List[SimpleSegmentABC]
    origin: KeypointDefinition
    primary_axis_upwards_z: KeypointDefinition  # defining primary axis as upwards Z
    approximate_forwards_x: Optional[KeypointDefinition]
    approximate_leftward_y: Optional[KeypointDefinition]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> KeypointDefinition:
        return self.parent

    def __post_init__(self):

        if not self.approximate_forwards_x and not self.approximate_forwards_x:
            raise ValueError(
                "At least one of approximate_positive_y_direction or approximate_negative_y_direction must be defined")

        print(f"CompoundSegment: {self.name} instantiated with parent {self.parent} and children {self.children}")

    @property
    def orthonormal_basis(self):
        raise NotImplementedError("TODO - this lol")

    @classmethod
    def get_children(cls) -> List[KeypointDefinition]:
        children = []
        for segment in cls.segments:
            children.extend(segment.get_children())
        return children
