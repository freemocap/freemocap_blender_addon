from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, List


@dataclass
class KeypointABC(ABC):
    name: str

    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __str__(self):
        return self.name


class Keypoints(Enum):
    """An enumeration of Keypoint instances, ensuring each member is a Keypoint.

    Methods
    -------
    __new__(cls, *args, **kwargs):
        Creates a new Keypoint instance with the enum member name as the Keypoint name.
    _generate_next_value_(name, start, count, last_values):
        Generates the next value for the auto-assigned enum members.
    """

    @property
    def name(self):
        return self.__class__.__name__

    def __new__(cls, *args: Any, **kwargs: Any) -> 'Keypoints':
        obj = object.__new__(cls)
        if not args:
            name = cls._name_.lower()
        else:
            name = args[0].lower()
        obj._value_ = KeypointABC(name)
        return obj

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def to_list(cls, exclude: List[KeypointABC] = None) -> List[KeypointABC]:

        if exclude is None:
            exclude = []
        return [keypoint.value for keypoint in cls.__members__.values() if keypoint.value not in exclude]

    def __str__(self):
        out_str = f"{self.name}: \n {self.value}"
        return out_str




@dataclass
class WeightedSumDefinition(ABC):
    parent_keypoints: List[KeypointABC]
    weights: List[float]

    def __post_init__(self):
        if len(self.parent_keypoints) != len(self.weights):
            raise ValueError("The number of parent keypoints must match the number of weights")
