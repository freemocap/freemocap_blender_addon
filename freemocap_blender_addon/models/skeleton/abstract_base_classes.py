import collections
from abc import ABC
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NamedDataclassABC(ABC):
    name: str

    def __init__(self, name: Optional[str] = None):
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.name


@dataclass
class SimpleDataclassABC(NamedDataclassABC):
    parent: NamedDataclassABC
    child: NamedDataclassABC

    def __init__(self, parent: NamedDataclassABC, child: NamedDataclassABC, name: Optional[str] = None):
        super().__init__(name)
        self.parent = parent
        self.child = child

        if self.parent == self.child:
            raise ValueError("Parent keypoint cannot be the same as the child keypoint")

    def __str__(self) -> str:
        out_str = self.name + "\n"
        out_str += f"\tParent: {self.parent}\n"
        out_str += f"\tChild: {self.child}"
        return out_str


@dataclass
class CompoundDataclassABC(NamedDataclassABC):
    parent: NamedDataclassABC
    children: List[NamedDataclassABC]

    @property
    def positive_x(self) -> str:
        raise NotImplementedError("Primary axis must be defined in the subclass")

    @property
    def approximate_positive_y(self) -> str:
        raise NotImplementedError("Secondary axis must be defined in the subclass")

    def get_child(self, child: NamedDataclassABC) -> NamedDataclassABC:
        if child not in self.children:
            raise ValueError(f"Keypoint {child.name} is not a child of {self.parent.name}")
        return child

    def __init__(self, parent: NamedDataclassABC, children: List[NamedDataclassABC], name: Optional[str] = None):
        super().__init__(name)
        self.parent = parent
        self.children = children

        if self.parent in self.children:
            raise ValueError("Parent keypoint cannot be a child keypoint")
        if len(self.children) < 2:
            raise ValueError(
                "A CompoundDataclassABC must have at least 2 children - use SimpleDataclassABC instead")

        # check for duplicate children
        if len(set(self.children)) < len(self.children):
            duplicates = [item for item, count in collections.Counter(self.children).items() if count > 1]
            raise ValueError(f"Duplicate children found: {duplicates}")

    def __str__(self) -> str:
        out_str = self.name + "\n"
        out_str += f"\tParent: {self.parent}\n"
        children_str = "\n\t\t".join([f"{child}" for child in self.children])
        out_str += f"\tChildren: {children_str}"
        return out_str


@dataclass
class KeypointABC(NamedDataclassABC):
    """
    A Keypoint is a named "key" location on a skeleton, used to define the position of a rigid body or linkage.
    In marker-based motion capture, keypoints could correspond to markers placed on the body.
    In markerless motion capture, keypoints could correspond to a tracked point in the image.
    When a Keypoint is hydrated with data, it becomes a Trajectory.
    """
    pass


@dataclass
class RigidBodyABC(NamedDataclassABC):
    """
    A RigigBody is a collection of keypoints that are linked together, such that the distance between them is constant.
    """
    pass


@dataclass
class SimpleRigidBody(RigidBodyABC, SimpleDataclassABC):
    """
    A simple rigid body is a RigidBody consisting of Two and Only Two keypoints that are linked together, the distance between them is constant.
    The parent keypoint defines the origin of the rigid body, and the child keypoint is the end of the rigid body.
    The primary axis (+X) of the rigid body is the vector from the parent to the child, the secondary and tertiary axes (+Y, +Z) are undefined (i.e. we have enough information to define the pitch and yaw, but not the roll).
    """
    parent: KeypointABC
    child: KeypointABC


@dataclass
class CompositeRigidBody(RigidBodyABC, CompoundDataclassABC):
    """
    A composite rigid body is a collection of keypoints that are linked together, such that the distance between all keypoints is constant.
    The parent keypoint is the origin of the rigid body
    The primary and secondary axes must be defined when in the instantiated class.
    """
    parent: KeypointABC
    children: List[KeypointABC]
    shared_keypoint: KeypointABC

    def __init__(self,
                 parent: KeypointABC,
                 children: List[KeypointABC],
                 shared_keypoint: KeypointABC,
                 name: Optional[str] = None):
        super().__init__(parent, children, name)
        self.shared_keypoint = shared_keypoint
        self.parent = parent
        self.children = children

        for child in self.children:
            if child == self.shared_keypoint:
                return
        raise ValueError(f"Shared keypoint {self.shared_keypoint.name} not found in children {self.children}")


class LinkageABC(NamedDataclassABC):
    """
    An abstract base class for a linkage between two or more rigid bodies.
    """


@dataclass
class SimpleLinkageABC(LinkageABC, SimpleDataclassABC):
    """
    A simple linkage comprises two RigidBodies that share a common Keypoint.

    The distance from the linked keypoint is fixed relative to the keypoints in the same rigid body,
     but the distances between the unlinked keypoints may change.

     #for now these are all 'universal' (ball) joints. Later we can add different constraints
    """
    parent: RigidBodyABC
    child: RigidBodyABC
    # TODO - calculate the common keypoint from the bodies and raise an error if it doesn't exist or if there are more than one
    linked_keypoint: KeypointABC

    def __init__(self, parent: RigidBodyABC, child: RigidBodyABC, linked_keypoint: KeypointABC, name: Optional[str] = None):
        super().__init__(parent, child, name)
        self.parent = parent
        self.child = child
        self.linked_keypoint = linked_keypoint

        for body in [self.parent, self.child]:
            if isinstance(body, SimpleRigidBody):
                if body.parent != self.linked_keypoint and body.child != self.linked_keypoint:
                    raise ValueError(f"Common keypoint {self.linked_keypoint.name} not found in body {body.name}")
            elif isinstance(body, CompositeRigidBody):
                if body.parent != self.linked_keypoint and body.children != self.linked_keypoint:
                    raise ValueError(f"Common keypoint {self.linked_keypoint.name} not found in body {body.name}")
            else:
                raise ValueError(f"Body {body.name} is not a valid rigid body type")

    def __str__(self) -> str:
        out_str = super().__str__()
        out_str += f"\n\tCommon Keypoint: {self.linked_keypoint}\n"
        return out_str


class CompoundLinkageABC(LinkageABC, CompoundDataclassABC):
    """
    A Compound Linkage is a collection of linkages that are connected via at least two separate keypoints.
    """
    linkages: List[SimpleLinkageABC]
    root_keypoint: KeypointABC

    # TODO - calculate the common keypoints from the bodies and raise an error if they don't exist or if there are more than one
    common_keypoints: List[KeypointABC]

    def __init__(self,
                 linkages: List[SimpleLinkageABC],
                 root_keypoint: KeypointABC,
                 shared_keypoints: List[KeypointABC],
                 name: Optional[str] = None):
        super().__init__(name)
        self.linkages = linkages
        self.root_keypoint = root_keypoint
        self.shared_keypoints = shared_keypoints


        for linkage in self.linkages:
            if not isinstance(linkage, LinkageABC):
                raise ValueError(f"Linkage {linkage.name} is not a valid linkage type")



    def __str__(self) -> str:
        out_str = self.name + "\n"
        linkages_str = "\n\t".join([f"{linkage}" for linkage in self.linkages])
        out_str += f"\tLinkages: {linkages_str}"
        return out_str


class SkeletonABC(CompoundLinkageABC):
    """
    A special case of a CompoundLinkage that represents a full skeleton (human or otherwise)
    """
    pass


### Abstract Enum Classes & Auxilliary Classes ###

@dataclass
class WeightedSumDefinition(ABC):
    parent_keypoints: List[KeypointABC]
    weights: List[float]

    def __post_init__(self):
        if len(self.parent_keypoints) != len(self.weights):
            raise ValueError("The number of parent keypoints must match the number of weights")

# # TODO - Create an Abstract enum that can be used as a base enum for Keypoints, RigidBodies, Linkages, or Skeletons, implementing similar type stuff that this one does for Keypoints (but for the appropriate type)
# class Keypoints(Enum):
#     """An enumeration of Keypoint instances, ensuring each member is a Keypoint.
#
#     Methods
#     -------
#     __new__(cls, *args, **kwargs):
#         Creates a new Keypoint instance with the enum member name as the Keypoint name.
#     _generate_next_value_(name, start, count, last_values):
#         Generates the next value for the auto-assigned enum members.
#     """
#
#     @property
#     def name(self):
#         return self.__class__.__name__
#
#     def __new__(cls, *args: Any, **kwargs: Any) -> 'Keypoints':
#         obj = object.__new__(cls)
#         if not args:
#             name = cls._name_.lower()
#         else:
#             name = args[0].lower()
#         obj._value_ = KeypointABC(name)
#         return obj
#
#     @staticmethod
#     def _generate_next_value_(name, start, count, last_values):
#         return name
#
#     @classmethod
#     def to_list(cls, exclude: List[KeypointABC] = None) -> List[KeypointABC]:
#
#         if exclude is None:
#             exclude = []
#         return [keypoint.value for keypoint in cls.__members__.values() if keypoint.value not in exclude]
#
#     def __str__(self):
#         out_str = f"{self.name}: \n {self.value}"
#         return out_str
#
#
