from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import get_bone_info, \
    align_markers_to_armature
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.parent_vertex_groups_to_armature import \
    parent_vertex_groups_to_armature
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.rotate_vertex_groups import \
    rotate_vertex_groups
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.scale_vertex_groups import \
    scale_vertex_groups
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.translate_vertex_groups import \
    translate_vertex_groups

from pathlib import Path  
import bpy 

def attach_skelly_by_vertex_group(
    data_parent_empty_name: str,
    skelly_mesh_path: Path,
    rig: bpy.types.Object,
    vertex_groups: dict,
    empty_markers_reference: dict,
) -> None:
    
    # Get references to the data parent empty and the empties_parent
    data_parent_empty = bpy.data.objects[data_parent_empty_name]
    empties_parent = [obj for obj in data_parent_empty.children if 'empties_parent' in obj.name][0]

    # Get the bone info (postions and lengths)
    bone_info = get_bone_info(rig)

    # Move the empty markers to make the T-Pose in the current frame
    align_markers_to_armature(
        markers_list=empties_parent.children,
        markers_reference=empty_markers_reference,
        bone_info=bone_info
    )

    object_name = 'skelly_mesh'

    # bpy.ops.object.select_all(action='DESELECT')

    # Append the skelly mesh as blend file because the exports (fbx, obj)
    # don't save all the vertex groups
    with bpy.data.libraries.load(skelly_mesh_path, link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects.append(object_name)
            
    # skelly_mesh = bpy.context.selected_objects[0]

    # Link the appended object to the current scene
    for obj in bpy.data.objects:
        if object_name in obj.name and obj.parent is None:
            bpy.context.collection.objects.link(obj)
            skelly_mesh = obj
            break
    # if object_name in bpy.data.objects:
    #     obj = bpy.data.objects[object_name]
    #     bpy.context.collection.objects.link(obj)
    # bpy.context.collection.objects.link(skelly_mesh)

    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    # skelly_mesh = bpy.data.objects['skelly_mesh']
    skelly_mesh.select_set(True)
    bpy.context.view_layer.objects.active = skelly_mesh

    # Change to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    transform_vertex_groups(bone_info, skelly_mesh, vertex_groups)

    # Change to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    parent_vertex_groups_to_armature(skelly_mesh, vertex_groups, rig)

    # Parent the skelly mesh to the rig
    bpy.ops.object.select_all(action='DESELECT')
    skelly_mesh.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type='OBJECT')


def transform_vertex_groups(bone_info,
                            skelly_mesh,
                            vertex_groups):
    translate_vertex_groups(skelly_mesh, vertex_groups, bone_info)
    scale_vertex_groups(skelly_mesh, vertex_groups, bone_info)
    rotate_vertex_groups(skelly_mesh, vertex_groups, bone_info)
