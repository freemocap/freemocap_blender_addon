from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Union

import numpy as np

from freemocap_blender_addon.utilities.type_safe_dataclass import TypeSafeDataclass


@dataclass
class Keypoint(TypeSafeDataclass, ABC):
    """
    A Keypoint is a named "key" location on a skeleton, used to define the position of a rigid body or linkage.
    In marker-based motion capture, keypoints could correspond to markers placed on the body.
    In markerless motion capture, keypoints could correspond to a tracked point in the image.
    When a Keypoint is hydrated with data, it becomes a Trajectory.

    `definition` is a human-oriented description of the keypoint's location (e.g. an anatomical
    description of a landmark on a bone).
    """
    name: str
    definition: str


@dataclass
class KeypointTrajectory(Keypoint):
    """
    A KeypointTrajectory is a Keypoint that has been hydrated with data.
    """
    data: np.ndarray

    def __post_init__(self):
        if not len(self.data.shape) == 3:
            raise ValueError("Data shape should be (frame, trajectory, xyz)")
        if not self.data.shape[2] == 3:
            raise ValueError("Trajectory data should be 3D (xyz)")


@dataclass
class SegmentABC(ABC):
    """
    A RigigBody is a collection of keypoints that are linked together, such that the distance between them is constant.
    """
    parent: Keypoint

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

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: Dict[str, KeypointTrajectory]):
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

        parent = KeypointTrajectory(name=cls.parent.name, definition=cls.parent.definition,
                                    data=keypoint_trajectories[cls.parent.name])
        child = KeypointTrajectory(name=cls.child.name, definition=cls.child.definition,
                                   data=keypoint_trajectories[cls.child.name])

        return cls(parent=parent, child=child)


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

    @property
    def orthonormal_basis(self):
        raise NotImplementedError("TODO - this lol")

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: Dict[str, KeypointTrajectory]):
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

        parent = KeypointTrajectory(name=cls.parent.name, definition=cls.parent.definition,
                                    data=keypoint_trajectories[cls.parent.name])
        children = [
            KeypointTrajectory(name=child.name, definition=child.definition, data=keypoint_trajectories[child.name]) for
            child in cls.children]

        return cls(parent=parent, children=children)


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
    linked_keypoints: [Keypoint]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> Keypoint:
        return self.parent.root

    def __post_init__(self):
        for body in [self.parent, self.children]:
            for keypoint in self.linked_keypoints:
                if isinstance(body, SimpleSegmentABC):
                    if keypoint not in [body.parent, body.child]:
                        raise ValueError(f"Common keypoint {keypoint.name} not found in body {body}")
                elif isinstance(body, CompoundSegmentABC):
                    if keypoint not in [body.parent] + body.children:
                        raise ValueError(f"Common keypoint {keypoint.name} not found in body {body}")
                else:
                    raise ValueError(f"Body {body} is not a valid rigid body type")

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: Dict[str, KeypointTrajectory]):
        """
        Create a LinkageABC instance from trajectory data.

        Parameters
        ----------
        keypoint_trajectories : Dict[str, np.ndarray]
            A dictionary of KeypointTrajectories.

        Returns
        -------
        LinkageABC
            An instance of LinkageABC hydrated with KeypointTrajectories.
        """

        parent = cls.parent.from_keypoint_trajectories(keypoint_trajectories)
        children = [child.from_keypoint_trajectories(keypoint_trajectories) for child in cls.children]

        return cls(parent=parent, children=children)

    def __str__(self) -> str:
        out_str = super().__str__()
        out_str += "\n\t".join(f"Common Keypoints: {self.linked_keypoints}\n")
        return out_str


class ChainABC(ABC):
    """
    A Chain is a set of linkages that are connected via shared Segments.
    """
    parent: LinkageABC
    children: List[LinkageABC]
    # TODO - calculate the linked_point on instanciation rather than defining it manually
    shared_segments: List[SegmentABC]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> Keypoint:
        # Chain -> Linkage -> Segment -> Keypoint
        return self.parent.root

    def __post_init__(self):
        for body in self.shared_segments:
            if not any(body == linkage.parent for linkage in self.children):
                raise ValueError(f"Shared segment {body.name} not found in children {self.children}")

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: Dict[str, KeypointTrajectory]):
        """
        Create a ChainABC instance from trajectory data.

        Parameters
        ----------
        keypoint_trajectories : Dict[str, np.ndarray]
            A dictionary of KeypointTrajectories.

        Returns
        -------
        ChainABC
            An instance of ChainABC hydrated with KeypointTrajectories.
        """

        parent = cls.parent.from_keypoint_trajectories(keypoint_trajectories)
        children = [child.from_keypoint_trajectories(keypoint_trajectories) for child in cls.children]

        return cls(parent=parent, children=children)


### Abstract Enum Classes & Auxilliary Classes ###
TrackedPointName = str
TrackedPointList = List[TrackedPointName]
WeightedTrackedPoints = Dict[TrackedPointName, float]
# OffsetKeypoint = Dict[Keypoint, Tuple[float, float, float]] # TODO - implement this

KeypointMappingType = Union[TrackedPointName, TrackedPointList, WeightedTrackedPoints]  # , OffsetKeypoint]


@dataclass
class KeypointMapping(TypeSafeDataclass):
    """
    A KeypointMapping provides information on how to map a keypoint to data from a TrackingDataSource trajectory.
    It can represent:
     a single keypoint (maps to the keypoint)
     a list of keypoints (maps to the geometric mean of the keypoints),
     a dictionary of keypoints with weights (maps to the weighted sum of the tracked points), or
     a dictionary of keypoints with offsets (maps to the tracked point with an offset defined in the local reference frame of the Segment).

    """
    mapping: KeypointMappingType
    tracked_points: Optional[List[TrackedPointName]] = None
    weights: Optional[List[float]] = None

    def __post_init__(self):
        if isinstance(self.mapping, str):
            self.tracked_points = [self.mapping]
            self.weights = [1]

        elif isinstance(self.mapping, list):  # TODO - fancy types
            self.tracked_points = self.mapping
            self.weights = [1 / len(self.mapping)] * len(self.mapping)

        elif isinstance(self.mapping, dict):
            self.tracked_points = list(self.mapping.keys())
            self.weights = list(self.mapping.values())
        else:
            raise ValueError("Mapping must be a TrackedPointName, TrackedPointList, or WeightedTrackedPoints")

        if np.sum(self.weights) != 1:
            raise ValueError("The sum of the weights must be 1")

    def calculate_trajectory(self, data: np.ndarray, names: List[TrackedPointName]) -> np.ndarray:
        """
        Calculate a trajectory from a mapping of tracked points and their weights.
        """
        if data.shape[1] != len(names):
            raise ValueError("Data shape does not match trajectory names length")
        if not all(tracked_point_name in names for tracked_point_name in self.tracked_points):
            raise ValueError("Not all tracked points in mapping found in trajectory names")

        number_of_frames = data.shape[0]
        number_of_dimensions = data.shape[2]
        trajectories_frame_xyz = np.zeros((number_of_frames, number_of_dimensions), dtype=np.float32)

        for tracked_point_name, weight in zip(self.tracked_points, self.weights):
            if tracked_point_name not in names:
                raise ValueError(f"Key {tracked_point_name} not found in trajectory names")

            keypoint_index = names.index(tracked_point_name)
            keypoint_xyz = data[:, keypoint_index, :]
            trajectories_frame_xyz += keypoint_xyz * weight

        return trajectories_frame_xyz


class KeypointMappingsEnum(Enum):
    """An Enum that can hold different types of keypoint mappings."""

    def __new__(cls, value: KeypointMappingType):
        obj = object.__new__(cls)
        obj._value_ = KeypointMapping(mapping=value)
        return obj


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
    def root(self) -> Keypoint:
        # Skeleton -> Chain -> Linkage -> Segment -> Keypoint
        return self.parent.root

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: Dict[str, KeypointTrajectory]):
        """
        Create a SkeletonABC instance from trajectory data.

        Parameters
        ----------
        keypoint_trajectories : Dict[str, np.ndarray]
            A dictionary of KeypointTrajectories.

        Returns
        -------
        SkeletonABC
            An instance of SkeletonABC hydrated with KeypointTrajectories.
        """

        parent = cls.parent.from_keypoint_trajectories(keypoint_trajectories)
        children = [child.from_keypoint_trajectories(keypoint_trajectories) for child in cls.children]

        return cls(parent=parent, children=children)

