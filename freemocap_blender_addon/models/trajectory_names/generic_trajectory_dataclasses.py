from dataclasses import dataclass
from typing import Optional, List


@dataclass
class HandsTrajectoryNames:
    right: Optional[List[str]]
    left: Optional[List[str]]


@dataclass
class TetrapodTrajectoryNames:
    body: Optional[List[str]]
    face: Optional[List[str]]
    hands: Optional[HandsTrajectoryNames]
    tail: Optional[List[str]]

@dataclass
class HumanTrajectoryNames(TetrapodTrajectoryNames):
    pass
