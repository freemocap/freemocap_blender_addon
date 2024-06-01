from abc import ABC
from dataclasses import dataclass
from typing import List

from freemocap_blender_addon.models.skeleton.keypoints_enum import Keypoint, Keypoints


@dataclass
class WeightedSumDefinition(ABC):
    parent_keypoints: List[Keypoint]
    weights: List[float]

    def __post_init__(self):
        if len(self.parent_keypoints) != len(self.weights):
            raise ValueError("The number of parent keypoints must match the number of weights")


@dataclass
class SimpleRigidBodyABC(ABC):
    """
    A simple rigid body is a pair of keypoints that are linked together, the distance between them is constant.
    The parent keypoint is the origin of the rigid body, and the child keypoint is the end of the rigid body.
    The primary axis (+X) of the rigid body is the vector from the parent to the child, the secondary axis (+Y) is undefined.
    """
    parent: Keypoints
    child: Keypoints

    @property
    def linkage(self) -> str:
        return f"{self.parent.name}_{self.child.name}"

    @property
    def name(self) -> str:
        return self.__class__.__name__


@dataclass
class CompositeRigidBodyABC(ABC):
    """
    A composite rigid body is a collection of keypoints that are linked together, such that the distance between all keypoints is constant.
    The parent keypoint is the origin of the rigid body
    The primary and secondary axes must be defined when in the instantiated class.
    """
    parent: Keypoint
    children: List[Keypoint]

    @property
    def primary_axis(self) -> str:
        raise NotImplementedError("Primary axis must be defined in the subclass")

    @property
    def secondary_axis(self) -> str:
        raise NotImplementedError("Secondary axis must be defined in the subclass")

    def get_child(self, keypoint: Keypoint) -> Keypoint:
        if keypoint not in self.children:
            raise ValueError(f"Keypoint {keypoint.name} is not a child of {self.parent.name}")
        return keypoint

    def __post_init__(self):
        if self.parent in self.children:
            raise ValueError("Parent keypoint cannot be a child keypoint")
        if len(self.children) < 2:
            raise ValueError(
                "Composite rigid body must have at least 2 child keypoints - use SimpleRigidBodyABC instead")
