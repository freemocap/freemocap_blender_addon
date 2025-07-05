import bpy
import os
from copy import deepcopy

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import get_bone_info, \
    align_markers_to_armature

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.empty_markers_for_rest_pose import (
    _EMPTY_MARKERS,
)

def set_armature_pose_by_markers(
    data_parent_empty: bpy.types.Object,
    armature: bpy.types.Armature,
):
    # Get references to the empties_parent object
    empties_parent = [obj for obj in data_parent_empty.children if 'empties_parent' in obj.name][0]

    # Get the bone info (postions and lengths)
    bone_info = get_bone_info(armature)

    # Move the empty markers to make the rest pose in the current frame
    align_markers_to_armature(
        markers_list=empties_parent.children,
        markers_reference=deepcopy(_EMPTY_MARKERS),
        bone_info=bone_info
    )

    # Insert a keyframe in each marker position
    for marker in empties_parent.children:
        # bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        marker.keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)

    return
