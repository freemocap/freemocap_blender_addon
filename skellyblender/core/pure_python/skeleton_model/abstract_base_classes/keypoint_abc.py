from abc import ABC
from dataclasses import dataclass

from skellyblender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass


@dataclass
class KeypointDefinition(TypeSafeDataclass, ABC):
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

    def __post_init__(self):
        print(f"Keypoint: {self.name} instantiated with definition {self.definition}")

    def __str__(self):
        return f"Keypoint: {self.name}"


