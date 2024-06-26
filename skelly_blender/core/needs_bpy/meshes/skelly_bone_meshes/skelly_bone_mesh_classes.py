from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import bpy

from skelly_blender import PACKAGE_ROOT_PATH
from skelly_blender.core.pure_python.custom_types.generic_types import BlenderizedName
from skelly_blender.core.pure_python.freemocap_data.data_paths.default_path_enums import RightLeftAxial

SKELLY_BONE_MESHES_PATH = Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones"


@dataclass
class SkellyBoneMeshInfo:
    mesh_path: str  # Path to the mesh
    armature_origin_bone: BlenderizedName  # The bone whose HEAD location will be used to position the mesh
    bone_scale_segment: Optional[BlenderizedName] =None # The bone whose TAIL location will be used to scale the mesh(default, same as host bone)
    right_left: RightLeftAxial = RightLeftAxial.AXIAL
    def __post_init__(self):
        self.mesh_path = str(Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path)
        if not Path(self.mesh_path).exists():
            raise FileNotFoundError(f"Mesh file {self.mesh_path} not found!")
        if not self.bone_scale_segment:
            self.bone_scale_segment = self.armature_origin_bone

        if RightLeftAxial.RIGHT.blenderize() in self.armature_origin_bone:
            self.right_left = RightLeftAxial.RIGHT
        if RightLeftAxial.LEFT.blenderize() in self.armature_origin_bone:
            self.right_left = RightLeftAxial.LEFT

    @property
    def mesh_name(self) -> str:
        return (Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path).stem


@dataclass
class SkellyBoneMesh:
    mesh: bpy.types.Object
    bone_scale_segment: BlenderizedName
    right_left: RightLeftAxial

    @property
    def name(self) -> str:
        return self.mesh.name

    def __post_init__(self):
        if self.right_left == RightLeftAxial.LEFT:
            self._transform_right_mesh_to_left()

    def _transform_right_mesh_to_left(self):
        self.mesh.scale[0] = -1  # mirror the mesh on the x-axis
        self.mesh.name = self.mesh.name.replace(self.right_left.RIGHT.blenderize(), self.right_left.LEFT.blenderize())
