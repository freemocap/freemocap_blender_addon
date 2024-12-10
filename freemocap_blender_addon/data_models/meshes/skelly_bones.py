from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple, Union
from mathutils import Vector


@dataclass
class SkellyBoneMeshInfo:
    bones: List[str]  # Bones of the mesh
    bones_origin: Vector  # Origin of the bones
    bones_end: Vector  # End of the bones
    bones_length: float  # Total length of the bones
    mesh_length: float  # Length of the mesh
    position_offset: Tuple[float, float, float]  # Position offset of the mesh
    adjust_rotation: bool  # Adjust rotation of mesh after offset

def get_skelly_bones() -> dict[str, SkellyBoneMeshInfo]:
    return deepcopy(_SKELLY_BONES)

def skelly_bone_names() -> list[str]:
    return list(_SKELLY_BONES.keys())


_SKELLY_BONES = {
    "head": SkellyBoneMeshInfo(
        bones=["face"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.244915,
        position_offset=(0, 0, 0.03),
        adjust_rotation=False,
    ),
    "spine": SkellyBoneMeshInfo(
        bones=["spine", "spine.001", "neck"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.70856,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "upper_arm.R": SkellyBoneMeshInfo(
        bones=["upper_arm.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.325418,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "upper_arm.L": SkellyBoneMeshInfo(
        bones=["upper_arm.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.325418,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "forearm.R": SkellyBoneMeshInfo(
        bones=["forearm.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.255504,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "forearm.L": SkellyBoneMeshInfo(
        bones=["forearm.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.255504,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "hand.R": SkellyBoneMeshInfo(
        bones=["hand.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.0845,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "hand.L": SkellyBoneMeshInfo(
        bones=["hand.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.0845,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thumb.01.R": SkellyBoneMeshInfo(
        bones=["thumb.01.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.03675,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thumb.01.L": SkellyBoneMeshInfo(
        bones=["thumb.01.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.03675,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thumb.02.R": SkellyBoneMeshInfo(
        bones=["thumb.02.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.032224,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thumb.02.L": SkellyBoneMeshInfo(
        bones=["thumb.02.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.032224,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thumb.03.R": SkellyBoneMeshInfo(
        bones=["thumb.03.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.023374,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thumb.03.L": SkellyBoneMeshInfo(
        bones=["thumb.03.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.023374,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "palm.01.R": SkellyBoneMeshInfo(
        bones=["palm.01.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.085891,
        position_offset=(0, -0.025, 0.02),
        adjust_rotation=True,
    ),
    "palm.01.L": SkellyBoneMeshInfo(
        bones=["palm.01.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.085891,
        position_offset=(0, -0.025, 0.02),
        adjust_rotation=True,
    ),
    "palm.02.R": SkellyBoneMeshInfo(
        bones=["palm.02.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.085828,
        position_offset=(0, -0.005, 0.02),
        adjust_rotation=True,
    ),
    "palm.02.L": SkellyBoneMeshInfo(
        bones=["palm.02.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.085828,
        position_offset=(0, -0.005, 0.02),
        adjust_rotation=True,
    ),
    "palm.03.R": SkellyBoneMeshInfo(
        bones=["palm.03.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.082869,
        position_offset=(0, 0.01, 0.02),
        adjust_rotation=True,
    ),
    "palm.03.L": SkellyBoneMeshInfo(
        bones=["palm.03.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.082869,
        position_offset=(0, 0.01, 0.02),
        adjust_rotation=True,
    ),
    "palm.04.R": SkellyBoneMeshInfo(
        bones=["palm.04.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.070385,
        position_offset=(0, 0.025, 0.02),
        adjust_rotation=True,
    ),
    "palm.04.L": SkellyBoneMeshInfo(
        bones=["palm.04.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.070385,
        position_offset=(0, 0.025, 0.02),
        adjust_rotation=True,
    ),
    "f_index.01.R": SkellyBoneMeshInfo(
        bones=["f_index.01.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.053961,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_index.01.L": SkellyBoneMeshInfo(
        bones=["f_index.01.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.053961,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_index.02.R": SkellyBoneMeshInfo(
        bones=["f_index.02.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.033378,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_index.02.L": SkellyBoneMeshInfo(
        bones=["f_index.02.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.033378,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_index.03.R": SkellyBoneMeshInfo(
        bones=["f_index.03.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.024385,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_index.03.L": SkellyBoneMeshInfo(
        bones=["f_index.03.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.024385,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_middle.01.R": SkellyBoneMeshInfo(
        bones=["f_middle.01.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.053792,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_middle.01.L": SkellyBoneMeshInfo(
        bones=["f_middle.01.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.053792,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_middle.02.R": SkellyBoneMeshInfo(
        bones=["f_middle.02.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.03347,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_middle.02.L": SkellyBoneMeshInfo(
        bones=["f_middle.02.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.03347,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_middle.03.R": SkellyBoneMeshInfo(
        bones=["f_middle.03.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.028028,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_middle.03.L": SkellyBoneMeshInfo(
        bones=["f_middle.03.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.028028,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_ring.01.R": SkellyBoneMeshInfo(
        bones=["f_ring.01.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.046598,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_ring.01.L": SkellyBoneMeshInfo(
        bones=["f_ring.01.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.046598,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_ring.02.R": SkellyBoneMeshInfo(
        bones=["f_ring.02.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.036003,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_ring.02.L": SkellyBoneMeshInfo(
        bones=["f_ring.02.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.036003,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_ring.03.R": SkellyBoneMeshInfo(
        bones=["f_ring.03.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.024413,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_ring.03.L": SkellyBoneMeshInfo(
        bones=["f_ring.03.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.024413,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_pinky.01.R": SkellyBoneMeshInfo(
        bones=["f_pinky.01.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.039485,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_pinky.01.L": SkellyBoneMeshInfo(
        bones=["f_pinky.01.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.039485,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_pinky.02.R": SkellyBoneMeshInfo(
        bones=["f_pinky.02.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.027034,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_pinky.02.L": SkellyBoneMeshInfo(
        bones=["f_pinky.02.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.027034,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_pinky.03.R": SkellyBoneMeshInfo(
        bones=["f_pinky.03.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.020288,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "f_pinky.03.L": SkellyBoneMeshInfo(
        bones=["f_pinky.03.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.020288,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thigh.R": SkellyBoneMeshInfo(
        bones=["thigh.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.42875,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "thigh.L": SkellyBoneMeshInfo(
        bones=["thigh.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.42875,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "shin.R": SkellyBoneMeshInfo(
        bones=["shin.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.412281,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "shin.L": SkellyBoneMeshInfo(
        bones=["shin.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.412281,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "foot.R": SkellyBoneMeshInfo(
        bones=["foot.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.226,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "foot.L": SkellyBoneMeshInfo(
        bones=["foot.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.226,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "heel.02.R": SkellyBoneMeshInfo(
        bones=["heel.02.R"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.150255,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
    "heel.02.L": SkellyBoneMeshInfo(
        bones=["heel.02.L"],
        bones_origin=Vector(0, 0, 0),
        bones_end=Vector(0, 0, 0),
        bones_length=0,
        mesh_length=0.150255,
        position_offset=(0, 0, 0),
        adjust_rotation=False,
    ),
}
