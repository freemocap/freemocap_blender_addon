import bpy
from pathlib import Path  

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import \
    get_bone_info
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.rotate_vertex_groups import \
    rotate_vertex_groups
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.scale_vertex_groups import \
    scale_vertex_groups
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.translate_vertex_groups import \
    translate_vertex_groups

def attach_skelly_by_vertex_group(
    skelly_mesh_path: Path,
    rig: bpy.types.Object,
    vertex_groups: dict,
) -> None:
    
    object_name = 'skelly_mesh'

    # Append the skelly mesh as blend file because the exports (fbx, obj)
    # don't save all the vertex groups
    with bpy.data.libraries.load(skelly_mesh_path, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)

    # Link the appended object to the current scene
    for obj in bpy.data.objects:
        if object_name in obj.name and obj.parent is None:
            bpy.context.collection.objects.link(obj)
            skelly_mesh = obj
            break

    align_and_parent_vertex_groups_to_armature(
        armature=rig,
        mesh_object=skelly_mesh,
        vertex_groups=vertex_groups,
    )


# This function aligns and parents the skelly mesh to the armature
# It is defined separately because it is also called in export 3d model
def align_and_parent_vertex_groups_to_armature(
    armature: bpy.types.Object,
    mesh_object: bpy.types.Object,
    vertex_groups: dict,
):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    # Get the bone info (postions and lengths)
    bone_info = get_bone_info(armature)
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    # Remove the modifiers from the mesh
    mesh_object.modifiers.clear()
    # Select and activate the mesh object
    mesh_object.select_set(True)
    bpy.context.view_layer.objects.active = mesh_object
    # Change to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Transform the vertex groups to match the new pose
    translate_vertex_groups(mesh_object, vertex_groups, bone_info)
    scale_vertex_groups(mesh_object, vertex_groups, bone_info)
    rotate_vertex_groups(mesh_object, vertex_groups, bone_info)
    # Change to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    # Parent the mesh to the armature
    bpy.ops.object.select_all(action='DESELECT')
    mesh_object.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='ARMATURE_NAME')
