from abc import ABC
from dataclasses import dataclass
from typing import List, Optional

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.keypoint_abc import Keypoint, \
    KeypointTrajectory
from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.tracked_point_keypoint_types import KeypointTrajectories


@dataclass
class SegmentABC(ABC):
    """
    A RigigBody is a collection of keypoints that are linked together, such that the distance between them is constant.
    """
    parent: Keypoint

    def __post_init__(self):
        if not isinstance(self.parent, Keypoint):
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
    parent: Keypoint
    child: Keypoint

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> Keypoint:
        return self.parent

    def __post_init__(self):
        if not all(isinstance(keypoint, Keypoint) for keypoint in [self.parent, self.child]):
            raise ValueError("Parent and child keypoints must be instances of Keypoint")
        if self.parent == self.child:
            raise ValueError("Parent and child keypoints must be different")
        print(f"SimpleSegment: {self.name} instantiated with parent {self.parent} and child {self.child}")

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: KeypointTrajectories):
        """
        Create a SimpleSegmentABC instance from trajectory data.

        Parameters
        ----------
        keypoint_trajectories : Dict[str, np.ndarray]
            A dictionary of KeypointTrajectories.

        Returns
        -------
        SimpleSegmentABC
            An instance of SimpleSegmentABC hydrated with KeypointTrajectories.
        """

        parent = KeypointTrajectory(name=cls.parent.name, definition=cls.parent.value,
                                    data=keypoint_trajectories[cls.parent.name.lower()])
        child = KeypointTrajectory(name=cls.child.name, definition=cls.child.value,
                                   data=keypoint_trajectories[cls.child.name.lower()])

        return cls(parent=parent, child=child)

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
    parent: Keypoint
    children: List[Keypoint]
    shared_keypoint: Keypoint
    positive_x_direction: Keypoint
    approximate_positive_y_direction: Optional[Keypoint]
    approximate_negative_y_direction: Optional[Keypoint]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> Keypoint:
        return self.parent

    def __post_init__(self):
        if not any(child == self.shared_keypoint for child in self.children):
            raise ValueError(f"Shared keypoint {self.shared_keypoint.name} not found in children {self.children}")
        if not any(child == self.positive_x_direction for child in self.children):
            raise ValueError(
                f"Positive X direction {self.positive_x_direction.name} not found in children {self.children}")
        if self.approximate_positive_y_direction and not any(
                child == self.approximate_positive_y_direction for child in self.children):
            raise ValueError(
                f"Approximate Positive Y direction {self.approximate_positive_y_direction.name} not found in children {self.children}")
        if self.approximate_negative_y_direction and not any(
                child == self.approximate_negative_y_direction for child in self.children):
            raise ValueError(
                f"Approximate Negative Y direction {self.approximate_negative_y_direction.name} not found in children {self.children}")

        if not self.approximate_positive_y_direction and not self.approximate_negative_y_direction:
            raise ValueError(
                "At least one of approximate_positive_y_direction or approximate_negative_y_direction must be defined")

        print(f"CompoundSegment: {self.name} instantiated with parent {self.parent} and children {self.children}")

    @property
    def orthonormal_basis(self):
        raise NotImplementedError("TODO - this lol")

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: KeypointTrajectories):
        """
        Create a CompoundSegmentABC instance from trajectory data.

        Parameters
        ----------
        keypoint_trajectories : Dict[str, np.ndarray]
            A dictionary of KeypointTrajectories.

        Returns
        -------
        CompoundSegmentABC
            An instance of CompoundSegmentABC hydrated with KeypointTrajectories.
        """

        parent = KeypointTrajectory(name=cls.parent.name, definition=cls.parent.value,
                                    data=keypoint_trajectories[cls.parent.name.lower()])
        children = [
            KeypointTrajectory(name=child.name, definition=child.definition, data=keypoint_trajectories[child.name.lower()]) for
            child in cls.children]

        return cls(parent=parent, children=children)
