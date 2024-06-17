import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import bpy


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
class ConstraintABC(ABC):
    type: ConstraintType = field(init=False)

    def validate_target(self, target: str) -> None:
        if target not in bpy.data.objects:
            raise ValueError(f"Target {target} not found in bpy.data.objects")

    @abstractmethod
    def apply_constraint(self, bone: bpy.types.PoseBone) -> None:
        pass


@dataclass
class CopyLocationConstraint(ConstraintABC):
    type: ConstraintType = field(default=ConstraintType.COPY_LOCATION.value, init=False)
    target: str

    def apply_constraint(self, bone: bpy.types.PoseBone) -> bpy.types.Constraint:
        self.validate_target(self.target)
        constraint = bone.constraints.new(self.type)
        constraint.target = bpy.data.objects[self.target]


@dataclass
class LockedTrackConstraint(ConstraintABC):
    type: ConstraintType = field(default=ConstraintType.LOCKED_TRACK.value, init=False)
    target: str
    track_axis: TrackAxis
    lock_axis: LockAxis
    influence: Optional[float] = 1.0

    def apply_constraint(self, bone: bpy.types.PoseBone) -> None:
        self.validate_target(self.target)
        constraint = bone.constraints.new(self.type)
        constraint.target = bpy.data.objects[self.target]
        constraint.track_axis = self.track_axis
        constraint.lock_axis = self.lock_axis
        constraint.influence = self.influence


@dataclass
class DampedTrackConstraint(ConstraintABC):
    type: ConstraintType = field(default=ConstraintType.DAMPED_TRACK.value, init=False)
    target: str
    track_axis: TrackAxis

    def apply_constraint(self, bone: bpy.types.PoseBone) -> None:
        self.validate_target(self.target)
        constraint = bone.constraints.new(self.type)
        constraint.target = bpy.data.objects[self.target]
        constraint.track_axis = self.track_axis


@dataclass
class LimitRotationConstraint(ConstraintABC):
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

    def apply_constraint(self, bone: bpy.types.PoseBone) -> None:
        constraint = bone.constraints.new(self.type)
        constraint.use_limit_x = self.use_limit_x
        constraint.min_x = math.radians(self.min_x)
        constraint.max_x = math.radians(self.max_x)
        constraint.use_limit_y = self.use_limit_y
        constraint.min_y = math.radians(self.min_y)
        constraint.max_y = math.radians(self.max_y)
        constraint.use_limit_z = self.use_limit_z
        constraint.min_z = math.radians(self.min_z)
        constraint.max_z = math.radians(self.max_z)
        constraint.owner_space = self.owner_space


@dataclass
class IKConstraint(ConstraintABC):
    type: ConstraintType = field(default=ConstraintType.IK.value, init=False)
    target: str
    pole_target: str
    chain_count: int
    pole_angle: float

    def apply_constraint(self, bone: bpy.types.PoseBone) -> None:
        self.validate_target(self.target)
        self.validate_target(self.pole_target)
        constraint = bone.constraints.new(self.type)
        constraint.target = bpy.data.objects[self.target]
        constraint.pole_target = bpy.data.objects[self.pole_target]
        constraint.chain_count = self.chain_count
        constraint.pole_angle = self.pole_angle


class BoneConstraintTypes(Enum):
    COPY_LOCATION: ConstraintABC = CopyLocationConstraint
    LOCKED_TRACK: ConstraintABC = LockedTrackConstraint
    DAMPED_TRACK: ConstraintABC = DampedTrackConstraint
    LIMIT_ROTATION: ConstraintABC = LimitRotationConstraint
    IK: ConstraintABC = IKConstraint
