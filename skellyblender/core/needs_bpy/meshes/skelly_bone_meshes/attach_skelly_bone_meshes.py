from dataclasses import dataclass
from typing import Dict, Optional

import bpy
import numpy as np

from skellyblender.core.needs_bpy.armature_rig.armature.armature_definition_classes import ArmatureDefinition
from skellyblender.core.needs_bpy.blender_utilities.object_selection import deselect_all_objects, \
    set_active_object
from skellyblender.core.needs_bpy.meshes.skelly_bone_meshes.skelly_bone_mesh_classes import SkellyBoneMesh
from skellyblender.core.needs_bpy.meshes.skelly_bone_meshes.skelly_bone_mesh_file_definitions import \
    SKELLY_BONE_MESH_FILE_DEFINITIONS


@dataclass
class SkellyMeshProcessor:
    armature: bpy.types.Object
    armature_definition: ArmatureDefinition
    bone_mesh_file_definitions = SKELLY_BONE_MESH_FILE_DEFINITIONS
    skelly_meshes = {}
    joined_mesh: Optional[bpy.types.Object] = None

    def attach_skelly_bone_meshes(self) -> None:
        deselect_all_objects()

        self.skelly_meshes = self._load_skelly_fbx_meshes()

        for host_armature_bone, skelly_bone_mesh in self.skelly_meshes.items():
            self._transform_mesh(host_armature_bone, skelly_bone_mesh)

        # self.join_meshes()

        # self._create_armature_deform_constraints_by_vector_groups()

    def _load_skelly_fbx_meshes(self) -> Dict[str, bpy.types.Object]:
        mesh_by_armature_bone = {}
        for bone_file_info in self.bone_mesh_file_definitions:
            if not bone_file_info:
                continue

            skelly_bone_mesh = SkellyBoneMesh.from_bone_file_info(bone_file_info=bone_file_info)
            mesh = bpy.data.objects[skelly_bone_mesh.mesh.name]
            self._create_vertex_group(mesh, skelly_bone_mesh.mesh.name)

            print(
                f"Loaded Mesh: {mesh.name}"
                f"\tFile path: `{bone_file_info.mesh_path}`\n"
                f"\tHost Armature Bone: `{skelly_bone_mesh.armature_origin_bone}`\n"                
                f"\tMeshScale Reference: `{skelly_bone_mesh.bone_scale_segment}`\n"
                f"\tOG Dimensions: `{skelly_bone_mesh.mesh.dimensions}`\n"
                f"\tVertex Group: `{skelly_bone_mesh.mesh.name}`\n"
            )
            mesh_by_armature_bone[skelly_bone_mesh.armature_origin_bone] = skelly_bone_mesh

        return mesh_by_armature_bone

    def _create_vertex_group(self, mesh: bpy.types.Object, group_name: str):
        bpy.context.view_layer.objects.active = mesh
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        vertex_group = mesh.vertex_groups.new(name=mesh.name)
        bpy.ops.object.vertex_group_assign()
        print(f"Created vertex group {vertex_group}")
        bpy.ops.object.mode_set(mode='OBJECT')

    def _transform_mesh(self, host_armature_bone: str, skelly_bone_mesh: SkellyBoneMesh):
        set_active_object(self.armature)
        bpy.ops.object.mode_set(mode='EDIT')
        host_bone = self.armature.data.edit_bones[host_armature_bone]
        scale_reference_bone = self.armature.data.edit_bones[skelly_bone_mesh.bone_scale_segment]
        target_length = np.linalg.norm(host_bone.head - scale_reference_bone.tail)
        mesh_og_length = skelly_bone_mesh.mesh_maxmin.y.max  # use y axis max for now
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
              f"\tTarget Length (Y): {target_length:.3f}m\n"
              f"\tOG Bone Length (Y): {mesh_og_length:.3f}m\n"
              f"\tScale Ratio: {mesh_scale_ratio:.3f}\n"
              f"\tOutput Dimensions: {skelly_bone_mesh.mesh.dimensions}m\n"
              )

    def _join_meshes(self):
        skelly_mesh_list = [bone_mesh.mesh for bone_mesh in self.skelly_meshes.values()]
        for skelly_mesh in skelly_mesh_list:
            skelly_mesh.select_set(True)

        set_active_object(skelly_mesh_list[0])
        bpy.ops.object.join()
        self.joined_mesh = bpy.context.view_layer.objects.active

    def _create_armature_deform_constraints_by_vector_groups(self):
        # Create an armature modifier
        self.armature = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE'][0]
        mod = self.joined_mesh.modifiers.new(name='Armature', type='ARMATURE')
        mod.object = self.armature

        # Assign each vertex group to its relevant armature bone
        for bone in self.armature.data.bones:
            if bone.name in self.joined_mesh.vertex_groups:
                self.joined_mesh.vertex_groups[bone.name].name = bone.name


def attach_skelly_bone_meshes(armature: bpy.types.Object, armature_definition: ArmatureDefinition) -> None:
    processor = SkellyMeshProcessor(armature=armature,
                                    armature_definition=armature_definition)
    processor.attach_skelly_bone_meshes()
