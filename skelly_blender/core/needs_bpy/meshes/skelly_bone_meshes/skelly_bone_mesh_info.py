from dataclasses import dataclass
from pathlib import Path
from typing import List

import bpy

from skelly_blender import PACKAGE_ROOT_PATH
from skelly_blender.core.pure_python.custom_types.base_enums import SegmentEnum
from skelly_blender.core.pure_python.custom_types.generic_types import BlenderizedName
from skelly_blender.core.pure_python.skeleton_model.static_definitions.body.body_keypoints import BodyKeypoints

SKELLY_BONE_MESHES_PATH = Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones"


@dataclass
class SkellyBoneMeshInfo:
    mesh_path: str  # Path to the mesh
    bone_scale_segment: BlenderizedName # The bone whose TAIL location will be used to scale the mesh

    def __post_init__(self):
        self.mesh_path = str(Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path)

    @property
    def mesh_name(self) -> str:
        return (Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path).stem


@dataclass
class SkellyBoneMesh:
    name: str
    mesh: bpy.types.Object
    bone_scale_segment: BlenderizedName
