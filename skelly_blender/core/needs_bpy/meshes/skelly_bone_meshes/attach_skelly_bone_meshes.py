from typing import Dict, Optional

import bpy

from skelly_blender.core.needs_bpy.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skelly_blender.core.needs_bpy.meshes.skelly_bone_meshes.skelly_bones_mesh_info import SKELLY_BONE_MESHES, \
    SkellyBoneMesh


def deselect_all_objects():
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.data.objects:
        obj.select_set(False)


def set_active_object(bpy_object: bpy.types.Object):
    bpy_object.select_set(True)
    bpy.context.view_layer.objects.active = bpy_object


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
        for bone_mesh_segment_host, bone_mesh_info in SKELLY_BONE_MESHES.items():
            if not bone_mesh_info:
                continue

            bpy.ops.import_scene.fbx(filepath=str(bone_mesh_info.mesh_path))
            mesh = bpy.data.objects[bone_mesh_info.mesh_name]
            mesh_scale_reference = bpy.data.objects[bone_mesh_info.scale_reference_keypoint.blenderize().upper()]
            mesh_scale = mesh_scale_reference.location.length

            meshes[bone_mesh_segment_host] = SkellyBoneMesh(name=bone_mesh_info.mesh_name,
                                                            mesh=mesh,
                                                            mesh_length=mesh_scale)

            self._create_vertex_group(mesh, bone_mesh_info.mesh_name)

            print(
                f"Loaded Mesh: '{bone_mesh_info.mesh_name}'\n"
                f"  Bone: '{bone_mesh_segment_host}'\n"
                f"  Path: '{bone_mesh_info.mesh_path}'\n"
                f"  Scale: {mesh_scale:.3f}\n"
                f"  Scale Reference: '{bone_mesh_info.scale_reference_keypoint}'\n"
                f"  Mesh Length: {mesh_scale:.3f}\n"
                f"  Vertex Group: '{bone_mesh_info.mesh_name}'\n"
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
        host_bone_length = host_bone.length
        mesh_scale_ratio = skelly_bone_mesh.mesh_length / host_bone_length
        host_bone_matrix = host_bone.matrix

        bpy.ops.object.mode_set(mode='OBJECT')
        skelly_bone_mesh.scale = (mesh_scale_ratio, mesh_scale_ratio, mesh_scale_ratio)
        skelly_bone_mesh.mesh.matrix_world = host_bone_matrix

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

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
