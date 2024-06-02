from abc import ABC
from dataclasses import dataclass
from typing import List

from freemocap_blender_addon.models.skeleton.keypoints.abc_keypoints import KeypointABC
from freemocap_blender_addon.models.skeleton.rigid_bodies.abc_rigid_body import RigidBodyABC, SimpleRigidBody, \
    CompositeRigidBody


@dataclass
class LinkageABC(ABC):
    """
    A linkage comprises two or more RigidBodies that share a common Keypoint.

    The distance from the linked keypoint is fixed relateive to the keypoints in the same rigid body,
     but the distances between the unlinked keypoints may change.

     #TODO- for now these are all 'universal' (ball) joints. Later we can add different constraints
    """

    bodies: List[RigidBodyABC]
    linked_keypoint: KeypointABC

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __post_init__(self):
        for body in self.bodies:
            if isinstance(body, SimpleRigidBody):
                if body.parent != self.linked_keypoint and body.child != self.linked_keypoint:
                    raise ValueError(f"Common keypoint {self.linked_keypoint.name} not found in body {body.name}")
            elif isinstance(body, CompositeRigidBody):
                if body.parent != self.linked_keypoint and body.children != self.linked_keypoint:
                    raise ValueError(f"Common keypoint {self.linked_keypoint.name} not found in body {body.name}")
            else:
                raise ValueError(f"Body {body.name} is not a valid rigid body type")

    def __str__(self) -> str:
        out_str = self.name + "\n"
        out_str += f"\tCommon Keypoint: {self.linked_keypoint}"
        bodies_str = "\n\t\t".join([f"\t{body}" for body in self.bodies])
        out_str += f"\tBodies: {bodies_str}"
        return out_str
