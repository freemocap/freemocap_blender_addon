from abc import ABC
from dataclasses import dataclass
from typing import List

from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import KeypointABC, Keypoints


@dataclass
class RigidBodyABC(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__


@dataclass
class SimpleRigidBody(RigidBodyABC):
    """
    A simple rigid body is a pair of keypoints that are linked together, the distance between them is constant.
    The parent keypoint is the origin of the rigid body, and the child keypoint is the end of the rigid body.
    The primary axis (+X) of the rigid body is the vector from the parent to the child, the secondary axis (+Y) is undefined.
    """
    parent: Keypoints
    child: Keypoints

    def __str__(self) -> str:
        out_str = self.name + "\n"
        out_str += f"\tParent: {self.parent}"
        out_str += f"\tChild: {self.child}"
        return out_str


@dataclass
class CompositeRigidBody(RigidBodyABC):
    """
    A composite rigid body is a collection of keypoints that are linked together, such that the distance between all keypoints is constant.
    The parent keypoint is the origin of the rigid body
    The primary and secondary axes must be defined when in the instantiated class.
    """
    parent: KeypointABC
    children: List[KeypointABC]

    @property
    def positive_x(self) -> str:
        raise NotImplementedError("Primary axis must be defined in the subclass")

    @property
    def approximate_positive_y(self) -> str:
        raise NotImplementedError("Secondary axis must be defined in the subclass")

    def get_child(self, keypoint: KeypointABC) -> KeypointABC:
        if keypoint not in self.children:
            raise ValueError(f"Keypoint {keypoint.name} is not a child of {self.parent.name}")
        return keypoint

    def __post_init__(self):
        if self.parent in self.children:
            raise ValueError("Parent keypoint cannot be a child keypoint")
        if len(self.children) < 2:
            raise ValueError(
                "Composite rigid body must have at least 2 child keypoints - use SimpleRigidBodyABC instead")


