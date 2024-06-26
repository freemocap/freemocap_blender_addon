from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import bpy

from skelly_blender import PACKAGE_ROOT_PATH
from skelly_blender.core.needs_bpy.blender_utilities.mesh_xyz_max_min import XYZMaxMin, find_mesh_xyz_maxmin
from skelly_blender.core.pure_python.custom_types.generic_types import BlenderizedName
from skelly_blender.core.pure_python.freemocap_data.data_paths.default_path_enums import RightLeftAxial
from skelly_blender.core.pure_python.utility_classes.type_safe_dataclass import TypeSafeDataclass

SKELLY_BONE_MESHES_PATH = Path(PACKAGE_ROOT_PATH) / "assets" / "skelly_bones"


@dataclass
class SkellyBoneFileInfo(TypeSafeDataclass):
    mesh_path: str  # Path to the mesh
    armature_origin_bone: BlenderizedName  # The bone whose HEAD location will be used to position the mesh
    bone_scale_segment: Optional[
        BlenderizedName] = None  # The bone whose TAIL location will be used to scale the mesh (default, same as host bone)

    def __post_init__(self):
        self.mesh_path = str(Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path)
        if not Path(self.mesh_path).exists():
            raise FileNotFoundError(f"Mesh file {self.mesh_path} not found!")
        if not self.bone_scale_segment:
            self.bone_scale_segment = self.armature_origin_bone


    @property
    def file_name(self) -> str:
        return (Path(SKELLY_BONE_MESHES_PATH) / self.mesh_path).stem


@dataclass
class SkellyBoneMesh(TypeSafeDataclass):
    mesh: bpy.types.Object
    armature_origin_bone: BlenderizedName
    bone_scale_segment: BlenderizedName
    right_left: RightLeftAxial

    @property
    def mesh_maxmin(self) -> XYZMaxMin:
        return find_mesh_xyz_maxmin(self.mesh)

    @classmethod
    def from_bone_file_info(cls, bone_file_info: SkellyBoneFileInfo) -> 'SkellyBoneMesh':
        bpy.ops.import_scene.fbx(filepath=str(bone_file_info.mesh_path))
        mesh = bpy.context.selected_objects[0]
        if RightLeftAxial.RIGHT.blenderize() in bone_file_info.armature_origin_bone:
            right_left = RightLeftAxial.RIGHT
        if RightLeftAxial.LEFT.blenderize() in bone_file_info.armature_origin_bone:
            right_left = RightLeftAxial.LEFT
            mesh.scale[0] = -1
            mesh.name = mesh.name.replace(right_left.RIGHT.blenderize(), right_left.LEFT.blenderize())
        else:
            right_left = RightLeftAxial.AXIAL

        return cls(mesh=mesh,
                   armature_origin_bone=bone_file_info.armature_origin_bone,
                   bone_scale_segment=bone_file_info.bone_scale_segment,
                   right_left=right_left)
