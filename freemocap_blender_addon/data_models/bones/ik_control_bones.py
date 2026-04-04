from dataclasses import dataclass
from typing import Tuple


@dataclass
class IKControlBoneInfo:
    controlled_bone: str
    tail_relative_position: Tuple[float, float, float]


ik_control_bones = {
    "hand.IK.R": IKControlBoneInfo(
        controlled_bone="hand.R",
        tail_relative_position=(-0.1, 0, 0),
    ),
    "hand.IK.L": IKControlBoneInfo(
        controlled_bone="hand.L",
        tail_relative_position=(0.1, 0, 0),
    ),
    "foot.IK.R": IKControlBoneInfo(
        controlled_bone="foot.R",
        tail_relative_position=(-0.1, 0, 0),
    ),
    "foot.IK.L": IKControlBoneInfo(
        controlled_bone="foot.L",
        tail_relative_position=(0.1, 0, 0),
    ),
}
