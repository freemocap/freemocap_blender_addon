from abc import ABC
from dataclasses import dataclass

from freemocap_blender_addon.models.skeleton_model.abstract_base_classes.keypoint_abc import Keypoint
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
    linked_keypoint: [Keypoint]

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def root(self) -> Keypoint:
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

    @classmethod
    def from_keypoint_trajectories(cls, keypoint_trajectories: KeypointTrajectories):
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

        return cls(parent=parent, children=children, linked_keypoint=cls.linked_keypoint)

    def __str__(self) -> str:
        out_str = super().__str__()
        out_str += "\n\t".join(f"Common Keypoints: {self.linked_keypoint}\n")
        return out_str
