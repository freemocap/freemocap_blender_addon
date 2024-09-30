from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Union, Dict, Optional
from enum import Enum


# Enums for specific keys to avoid spelling issues
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
    type: ConstraintType = field(default=ConstraintType.COPY_LOCATION, init=False)
    target: str


@dataclass
class LockedTrackConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.LOCKED_TRACK, init=False)
    target: str
    track_axis: Dict[str, TrackAxis]
    lock_axis: Dict[str, LockAxis]
    influence: Optional[float] = 1.0


@dataclass
class DampedTrackConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.DAMPED_TRACK, init=False)
    target: str
    track_axis: TrackAxis


@dataclass
class LimitRotationConstraint(Constraint):
    type: ConstraintType = field(default=ConstraintType.LIMIT_ROTATION, init=False)
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
    type: ConstraintType = field(default=ConstraintType.IK, init=False)
    target: str
    pole_target: str
    chain_count: int
    pole_angle: float


_BONE_CONSTRAINT_DEFINITIONS: Dict[
    str,
    List[
        Union[
            CopyLocationConstraint,
            LockedTrackConstraint,
            DampedTrackConstraint,
            LimitRotationConstraint,
            IKConstraint,
        ]
    ],
] = {
    "pelvis": [
        CopyLocationConstraint(target="hips_center"),
        LockedTrackConstraint(
            target="right_hip",
            track_axis={
                "freemocap_apose": TrackAxis.TRACK_NEGATIVE_X,
                "freemocap_tpose": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_default": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_tpose": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_realtime": TrackAxis.TRACK_Z,
            },
            lock_axis={
                "freemocap_apose": LockAxis.LOCK_Z,
                "freemocap_tpose": LockAxis.LOCK_Z,
                "ue_metahuman_default": LockAxis.LOCK_Z,
                "ue_metahuman_tpose": LockAxis.LOCK_Z,
                "ue_metahuman_realtime": LockAxis.LOCK_Y,
            },
            influence=1.0,
        ),
        LockedTrackConstraint(
            target="right_hip",
            track_axis={
                "freemocap_apose": TrackAxis.TRACK_NEGATIVE_X,
                "freemocap_tpose": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_default": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_tpose": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_realtime": TrackAxis.TRACK_Z,
            },
            lock_axis={
                "freemocap_apose": LockAxis.LOCK_Y,
                "freemocap_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_default": LockAxis.LOCK_Y,
                "ue_metahuman_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_realtime": LockAxis.LOCK_X,
            },
            influence=1.0,
        ),
    ],
    "pelvis.R": [
        DampedTrackConstraint(target="right_hip", track_axis=TrackAxis.TRACK_Y)
    ],
    "pelvis.L": [
        DampedTrackConstraint(target="left_hip", track_axis=TrackAxis.TRACK_Y)
    ],
    "spine": [
        CopyLocationConstraint(target="hips_center"),
        DampedTrackConstraint(target="trunk_center", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-45,
            max_x=68,
            use_limit_y=True,
            min_y=-45,
            max_y=45,
            use_limit_z=True,
            min_z=-30,
            max_z=30,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "spine.001": [
        DampedTrackConstraint(target="neck_center", track_axis=TrackAxis.TRACK_Y),
        LockedTrackConstraint(
            target="right_shoulder",
            track_axis={
                "freemocap_apose": TrackAxis.TRACK_NEGATIVE_X,
                "freemocap_tpose": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_default": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_tpose": TrackAxis.TRACK_NEGATIVE_X,
                "ue_metahuman_realtime": TrackAxis.TRACK_Z,
            },
            lock_axis={
                "freemocap_apose": LockAxis.LOCK_Y,
                "freemocap_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_default": LockAxis.LOCK_Y,
                "ue_metahuman_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_realtime": LockAxis.LOCK_Y,
            },
            influence=1.0,
        ),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-45,
            max_x=22,
            use_limit_y=True,
            min_y=-45,
            max_y=45,
            use_limit_z=True,
            min_z=-30,
            max_z=30,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "neck": [
        DampedTrackConstraint(target="head_center", track_axis=TrackAxis.TRACK_Y),
        LockedTrackConstraint(
            target="nose",
            track_axis={
                "freemocap_apose": TrackAxis.TRACK_Z,
                "freemocap_tpose": TrackAxis.TRACK_Z,
                "ue_metahuman_default": TrackAxis.TRACK_Z,
                "ue_metahuman_tpose": TrackAxis.TRACK_Z,
                "ue_metahuman_realtime": TrackAxis.TRACK_X,
            },
            lock_axis={
                "freemocap_apose": LockAxis.LOCK_Y,
                "freemocap_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_default": LockAxis.LOCK_Y,
                "ue_metahuman_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_realtime": LockAxis.LOCK_Y,
            },
            influence=1.0,
        ),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-37,
            max_x=22,
            use_limit_y=True,
            min_y=-45,
            max_y=45,
            use_limit_z=True,
            min_z=-30,
            max_z=30,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "face": [DampedTrackConstraint(target="nose", track_axis=TrackAxis.TRACK_Y)],
    "shoulder.R": [
        CopyLocationConstraint(target="neck_center"),
        DampedTrackConstraint(target="right_shoulder", track_axis=TrackAxis.TRACK_Y),
    ],
    "shoulder.L": [
        CopyLocationConstraint(target="neck_center"),
        DampedTrackConstraint(target="left_shoulder", track_axis=TrackAxis.TRACK_Y),
    ],
    "upper_arm.R": [
        DampedTrackConstraint(target="right_elbow", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-135,
            max_x=90,
            use_limit_y=True,
            min_y=-98,
            max_y=180,
            use_limit_z=True,
            min_z=-97,
            max_z=91,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "upper_arm.L": [
        DampedTrackConstraint(target="left_elbow", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-135,
            max_x=90,
            use_limit_y=True,
            min_y=-180,
            max_y=98,
            use_limit_z=True,
            min_z=-91,
            max_z=97,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "forearm.R": [
        DampedTrackConstraint(target="right_wrist", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-90,
            max_x=79,
            use_limit_y=True,
            min_y=0,
            max_y=146,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "forearm.L": [
        DampedTrackConstraint(target="left_wrist", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-90,
            max_x=79,
            use_limit_y=True,
            min_y=-146,
            max_y=0,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "hand.R": [
        DampedTrackConstraint(target="right_index", track_axis=TrackAxis.TRACK_Y),
        LockedTrackConstraint(
            target="right_hand_thumb_cmc",
            track_axis={
                "freemocap_apose": TrackAxis.TRACK_Z,
                "freemocap_tpose": TrackAxis.TRACK_Z,
                "ue_metahuman_default": TrackAxis.TRACK_Z,
                "ue_metahuman_tpose": TrackAxis.TRACK_Z,
                "ue_metahuman_realtime": TrackAxis.TRACK_Z,
            },
            lock_axis={
                "freemocap_apose": LockAxis.LOCK_Y,
                "freemocap_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_default": LockAxis.LOCK_Y,
                "ue_metahuman_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_realtime": LockAxis.LOCK_Y,
            },
            influence=1.0,
        ),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-36,
            max_y=25,
            use_limit_z=True,
            min_z=-86,
            max_z=90,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "hand.L": [
        DampedTrackConstraint(target="left_index", track_axis=TrackAxis.TRACK_Y),
        LockedTrackConstraint(
            target="left_hand_thumb_cmc",
            track_axis={
                "freemocap_apose": TrackAxis.TRACK_Z,
                "freemocap_tpose": TrackAxis.TRACK_Z,
                "ue_metahuman_default": TrackAxis.TRACK_Z,
                "ue_metahuman_tpose": TrackAxis.TRACK_Z,
                "ue_metahuman_realtime": TrackAxis.TRACK_NEGATIVE_Z,
            },
            lock_axis={
                "freemocap_apose": LockAxis.LOCK_Y,
                "freemocap_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_default": LockAxis.LOCK_Y,
                "ue_metahuman_tpose": LockAxis.LOCK_Y,
                "ue_metahuman_realtime": LockAxis.LOCK_Y,
            },
            influence=1.0,
        ),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-45,
            max_x=45,
            use_limit_y=True,
            min_y=-25,
            max_y=36,
            use_limit_z=True,
            min_z=-90,
            max_z=86,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "thigh.R": [
        CopyLocationConstraint(target="right_hip"),
        DampedTrackConstraint(target="right_knee", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-155,
            max_x=45,
            use_limit_y=True,
            min_y=-105,
            max_y=85,
            use_limit_z=True,
            min_z=-88,
            max_z=17,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "thigh.L": [
        CopyLocationConstraint(target="left_hip"),
        DampedTrackConstraint(target="left_knee", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-155,
            max_x=45,
            use_limit_y=True,
            min_y=-85,
            max_y=105,
            use_limit_z=True,
            min_z=-17,
            max_z=88,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "shin.R": [
        DampedTrackConstraint(target="right_ankle", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=0,
            max_x=150,
            use_limit_y=True,
            min_y=0,
            max_y=0,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "shin.L": [
        DampedTrackConstraint(target="left_ankle", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=0,
            max_x=150,
            use_limit_y=True,
            min_y=0,
            max_y=0,
            use_limit_z=True,
            min_z=0,
            max_z=0,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "foot.R": [
        DampedTrackConstraint(target="right_foot_index", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-31,
            max_x=63,
            use_limit_y=True,
            min_y=-26,
            max_y=26,
            use_limit_z=True,
            min_z=-15,
            max_z=74,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "foot.L": [
        DampedTrackConstraint(target="left_foot_index", track_axis=TrackAxis.TRACK_Y),
        LimitRotationConstraint(
            use_limit_x=True,
            min_x=-31,
            max_x=63,
            use_limit_y=True,
            min_y=-26,
            max_y=26,
            use_limit_z=True,
            min_z=-74,
            max_z=15,
            owner_space=OwnerSpace.LOCAL,
        ),
    ],
    "heel.02.R": [
        DampedTrackConstraint(target="right_heel", track_axis=TrackAxis.TRACK_Y)
    ],
    "heel.02.L": [
        DampedTrackConstraint(target="left_heel", track_axis=TrackAxis.TRACK_Y)
    ],
    "thumb.carpal.R": [
        DampedTrackConstraint(
            target="right_hand_thumb_cmc", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "thumb.01.R": [
        DampedTrackConstraint(
            target="right_hand_thumb_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "thumb.02.R": [
        DampedTrackConstraint(
            target="right_hand_thumb_ip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "thumb.03.R": [
        DampedTrackConstraint(
            target="right_hand_thumb_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.01.R": [
        DampedTrackConstraint(
            target="right_hand_index_finger_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_index.01.R": [
        DampedTrackConstraint(
            target="right_hand_index_finger_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_index.02.R": [
        DampedTrackConstraint(
            target="right_hand_index_finger_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_index.03.R": [
        DampedTrackConstraint(
            target="right_hand_index_finger_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.02.R": [
        DampedTrackConstraint(
            target="right_hand_middle_finger_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_middle.01.R": [
        DampedTrackConstraint(
            target="right_hand_middle_finger_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_middle.02.R": [
        DampedTrackConstraint(
            target="right_hand_middle_finger_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_middle.03.R": [
        DampedTrackConstraint(
            target="right_hand_middle_finger_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.03.R": [
        DampedTrackConstraint(
            target="right_hand_ring_finger_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_ring.01.R": [
        DampedTrackConstraint(
            target="right_hand_ring_finger_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_ring.02.R": [
        DampedTrackConstraint(
            target="right_hand_ring_finger_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_ring.03.R": [
        DampedTrackConstraint(
            target="right_hand_ring_finger_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.04.R": [
        DampedTrackConstraint(
            target="right_hand_pinky_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_pinky.01.R": [
        DampedTrackConstraint(
            target="right_hand_pinky_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_pinky.02.R": [
        DampedTrackConstraint(
            target="right_hand_pinky_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_pinky.03.R": [
        DampedTrackConstraint(
            target="right_hand_pinky_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "thumb.carpal.L": [
        DampedTrackConstraint(
            target="left_hand_thumb_cmc", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "thumb.01.L": [
        DampedTrackConstraint(
            target="left_hand_thumb_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "thumb.02.L": [
        DampedTrackConstraint(target="left_hand_thumb_ip", track_axis=TrackAxis.TRACK_Y)
    ],
    "thumb.03.L": [
        DampedTrackConstraint(
            target="left_hand_thumb_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.01.L": [
        DampedTrackConstraint(
            target="left_hand_index_finger_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_index.01.L": [
        DampedTrackConstraint(
            target="left_hand_index_finger_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_index.02.L": [
        DampedTrackConstraint(
            target="left_hand_index_finger_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_index.03.L": [
        DampedTrackConstraint(
            target="left_hand_index_finger_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.02.L": [
        DampedTrackConstraint(
            target="left_hand_middle_finger_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_middle.01.L": [
        DampedTrackConstraint(
            target="left_hand_middle_finger_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_middle.02.L": [
        DampedTrackConstraint(
            target="left_hand_middle_finger_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_middle.03.L": [
        DampedTrackConstraint(
            target="left_hand_middle_finger_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.03.L": [
        DampedTrackConstraint(
            target="left_hand_ring_finger_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_ring.01.L": [
        DampedTrackConstraint(
            target="left_hand_ring_finger_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_ring.02.L": [
        DampedTrackConstraint(
            target="left_hand_ring_finger_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_ring.03.L": [
        DampedTrackConstraint(
            target="left_hand_ring_finger_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "palm.04.L": [
        DampedTrackConstraint(
            target="left_hand_pinky_mcp", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_pinky.01.L": [
        DampedTrackConstraint(
            target="left_hand_pinky_pip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_pinky.02.L": [
        DampedTrackConstraint(
            target="left_hand_pinky_dip", track_axis=TrackAxis.TRACK_Y
        )
    ],
    "f_pinky.03.L": [
        DampedTrackConstraint(
            target="left_hand_pinky_tip", track_axis=TrackAxis.TRACK_Y
        )
    ],
}

def get_bone_constraint_definitions():
    return deepcopy(_BONE_CONSTRAINT_DEFINITIONS)