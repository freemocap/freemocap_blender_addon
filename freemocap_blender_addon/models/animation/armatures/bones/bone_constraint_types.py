from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ConstraintType(Enum):
    COPY_LOCATION = "COPY_LOCATION"
    LOCKED_TRACK = "LOCKED_TRACK"
    DAMPED_TRACK = "DAMPED_TRACK"
    LIMIT_ROTATION = "LIMIT_ROTATION"
    IK = "IK"


class TrackAxis(Enum):
    TRACK_X = "TRACK_X"
    TRACK_NEGATIVE_X = "TRACK_NEGATIVE_X"
    TRACK_Y = "TRACK_Y"
    TRACK_NEGATIVE_Y = "TRACK_NEGATIVE_Y"
    TRACK_Z = "TRACK_Z"
    TRACK_NEGATIVE_Z = "TRACK_NEGATIVE_Z"


class LockAxis(Enum):
    LOCK_X = "LOCK_X"
    LOCK_Y = "LOCK_Y"
    LOCK_Z = "LOCK_Z"


class OwnerSpace(Enum):
    LOCAL = "LOCAL"
    WORLD = "WORLD"


@dataclass
class Constraint:
    type: ConstraintType = field(init=False)


@dataclass
class CopyLocationConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.COPY_LOCATION.value, init=False)
    target: str


@dataclass
class LockedTrackConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.LOCKED_TRACK.value, init=False)
    target: str
    track_axis: TrackAxis
    lock_axis: LockAxis
    influence: Optional[float] = 1.0


@dataclass
class DampedTrackConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.DAMPED_TRACK.value, init=False)
    target: str
    track_axis: TrackAxis


@dataclass
class LimitRotationConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.LIMIT_ROTATION.value, init=False)
    use_limit_x: bool
    min_x: float
    max_x: float
    use_limit_y: bool
    min_y: float
    max_y: float
    use_limit_z: bool
    min_z: float
    max_z: float
    owner_space: OwnerSpace


@dataclass
class IKConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.IK.value, init=False)
    target: str
    pole_target: str
    chain_count: int
    pole_angle: float
