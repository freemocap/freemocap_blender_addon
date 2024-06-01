from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List


@dataclass
class Keypoint:
    name: str


class Keypoints(Enum):
    """An enumeration of Keypoint instances, ensuring each member is a Keypoint.

    Methods
    -------
    __new__(cls, *args, **kwargs):
        Creates a new Keypoint instance with the enum member name as the Keypoint name.
    _generate_next_value_(name, start, count, last_values):
        Generates the next value for the auto-assigned enum members.
    """

    def __new__(cls, *args: Any, **kwargs: Any) -> 'Keypoints':
        obj = object.__new__(cls)
        if not args:
            name = cls._name_.lower()
        else:
            name = args[0].lower()
        obj._value_ = Keypoint(name)
        return obj

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def to_list(cls, exclude: List[Keypoint] = None) -> List[str]:

        if exclude is None:
            exclude = []
        return [name for name, _ in cls.__members__.items() if cls[name].value not in exclude]

