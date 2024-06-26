from dataclasses import dataclass
from typing import Dict, Optional

import bpy
import numpy as np

from skelly_blender.core.needs_bpy.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skelly_blender.core.needs_bpy.meshes.skelly_bone_meshes.body_segment_bone_mesh_mapping import \
    BODY_SEGMENT_BONE_MESH_MAPPING
from skelly_blender.core.needs_bpy.meshes.skelly_bone_meshes.skelly_bone_mesh_info import SkellyBoneMesh


def deselect_all_objects():
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.data.objects:
        obj.select_set(False)


def set_active_object(bpy_object: bpy.types.Object):
    bpy_object.select_set(True)
    bpy.context.view_layer.objects.active = bpy_object


@dataclass
class MaxMin:
    min: float
    max: float

@dataclass
class XYZMaxMin:
    x: MaxMin
    y: MaxMin
    z: MaxMin

def find_mesh_xyz_maxmin(mesh: bpy.types.Object) -> XYZMaxMin:
    if mesh and mesh.type == 'MESH':
        vertices = np.array([v.co.to_tuple() for v in mesh.data.vertices])
        min_x, max_x = vertices[:, 0].min(), vertices[:, 0].max()
        min_y, max_y = vertices[:, 1].min(), vertices[:, 1].max()
        min_z, max_z = vertices[:, 2].min(), vertices[:, 2].max()
        
        return XYZMaxMin(
            x=MaxMin(min=min_x, max=max_x),
            y=MaxMin(min=min_y, max=max_y),
            z=MaxMin(min=min_z, max=max_z)
        )
    else:
        raise ValueError(f"Object {mesh} is not a mesh object!")
    

class SkellyMeshProcessor:
    def __init__(self, armature: bpy.types.Object, armature_definition: ArmatureDefinition):
        self._armature = armature
        self._armature_definition = armature_definition
        self._skelly_meshes = {}
        self._joined_mesh: Optional[bpy.types.Object] = None

    def attach_skelly_bone_meshes(self) -> None:
        deselect_all_objects()

        self._skelly_meshes = self._load_skelly_fbx_meshes()

        for host_armature_bone, skelly_bone_mesh in self._skelly_meshes.items():
            self._transform_mesh(host_armature_bone, skelly_bone_mesh)

        # self._join_meshes()

        self._create_armature_deform_constraints_by_vector_groups()

    def _load_skelly_fbx_meshes(self) -> Dict[str, bpy.types.Object]:
        meshes = {}
        for bone_mesh_segment_host, bone_mesh_info in BODY_SEGMENT_BONE_MESH_MAPPING.items():
            if not bone_mesh_info:
                continue

            bpy.ops.import_scene.fbx(filepath=str(bone_mesh_info.mesh_path))
            mesh = bpy.data.objects[bone_mesh_info.mesh_name]

            meshes[bone_mesh_segment_host] = SkellyBoneMesh(name=mesh.name,
                                                            mesh=mesh,
                                                            bone_scale_segment=bone_mesh_info.bone_scale_segment)
            self._create_vertex_group(mesh, bone_mesh_info.mesh_name)

            print(
                f"Loaded Mesh: '{bone_mesh_info.mesh_name}'\n"
                f"\tHost Armature Bone: '{bone_mesh_segment_host}'\n"
                f"\tPath: '{bone_mesh_info.mesh_path}'\n"
                f"\tMeshScale Reference: '{bone_mesh_info.bone_scale_segment}'\n"
                f"\tVertex Group: '{bone_mesh_info.mesh_name}'\n"
            )

        return meshes

    def _create_vertex_group(self, mesh: bpy.types.Object, group_name: str):
        bpy.context.view_layer.objects.active = mesh
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        vertex_group = mesh.vertex_groups.new(name=mesh.name)
        bpy.ops.object.vertex_group_assign()
        print(f"Created vertex group {vertex_group}")
        bpy.ops.object.mode_set(mode='OBJECT')

    def _transform_mesh(self, host_armature_bone: str, skelly_bone_mesh: SkellyBoneMesh):
        set_active_object(self._armature)
        bpy.ops.object.mode_set(mode='EDIT')
        host_bone = self._armature.data.edit_bones[host_armature_bone]
        scale_reference_bone = self._armature.data.edit_bones[skelly_bone_mesh.bone_scale_segment]
        target_length = np.linalg.norm(host_bone.head - scale_reference_bone.tail)
        mesh_og_length = find_mesh_xyz_maxmin(skelly_bone_mesh.mesh).y.max # use y axis max for now
        mesh_scale_ratio = target_length / mesh_og_length
        host_bone_head_location = host_bone.head
        host_bone_rotation_matrix = host_bone.matrix.to_3x3()

        bpy.ops.object.mode_set(mode='OBJECT')
        set_active_object(skelly_bone_mesh.mesh)
        skelly_bone_mesh.mesh.scale = (mesh_scale_ratio, mesh_scale_ratio, mesh_scale_ratio)
        skelly_bone_mesh.mesh.location = host_bone_head_location
        skelly_bone_mesh.mesh.rotation_euler = host_bone_rotation_matrix.to_euler()

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        print(f"Transformed mesh: {skelly_bone_mesh.mesh.name} to bone: {host_armature_bone}\n"
              f"\tScale Ratio: {mesh_scale_ratio}\n"
              f"\tBone Dimensions: {skelly_bone_mesh.mesh.dimensions}\n"
              )

    def _join_meshes(self):
        skelly_mesh_list = [bone_mesh.mesh for bone_mesh in self._skelly_meshes.values()]
        for skelly_mesh in skelly_mesh_list:
            skelly_mesh.select_set(True)

        set_active_object(skelly_mesh_list[0])
        bpy.ops.object.join()
        self._joined_mesh = bpy.context.view_layer.objects.active

    def _create_armature_deform_constraints_by_vector_groups(self):
        # Create an armature modifier
        self._armature = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE'][0]
        mod = self._joined_mesh.modifiers.new(name='Armature', type='ARMATURE')
        mod.object = self._armature

        # Assign each vertex group to its relevant armature bone
        for bone in self._armature.data.bones:
            if bone.name in self._joined_mesh.vertex_groups:
                self._joined_mesh.vertex_groups[bone.name].name = bone.name


def attach_skelly_bone_meshes(armature: bpy.types.Object, armature_definition: ArmatureDefinition) -> None:
    processor = SkellyMeshProcessor(armature, armature_definition)
    processor.attach_skelly_bone_meshes()
