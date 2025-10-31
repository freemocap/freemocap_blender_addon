from enum import Enum
from typing import Dict

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.skelly_mesh_paths import SKELLY_FULL_MESH_PATH
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_bone_mesh import \
    attach_skelly_by_bone_mesh
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_full_mesh import \
    attach_skelly_complete_mesh
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_vertex_groups import \
    attach_skelly_by_vertex_group

import bpy
from copy import deepcopy

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.skelly_vertex_groups import (
    _SKELLY_VERTEX_GROUPS,
)


class AddSkellyMeshStrategies(Enum):
    BY_BONE_MESH = "by_bone_mesh"
    COMPLETE_MESH = "complete_mesh"
    BY_VERTEX_GROUP = "by_vertex_group"

def attach_skelly_mesh_to_rig(
    rig: bpy.types.Object,
    body_dimensions: Dict[str, float],
    add_mesh_strategy: AddSkellyMeshStrategies = AddSkellyMeshStrategies.BY_VERTEX_GROUP,
) -> None:
    # Change to object mode
    if bpy.context.selected_objects != []:
        bpy.ops.object.mode_set(mode='OBJECT')

    if add_mesh_strategy == AddSkellyMeshStrategies.BY_BONE_MESH:
        attach_skelly_by_bone_mesh(
            rig=rig,
        )
    elif add_mesh_strategy == AddSkellyMeshStrategies.COMPLETE_MESH:
        attach_skelly_complete_mesh(
            rig=rig,
            body_dimensions=body_dimensions,
        )
    elif add_mesh_strategy == AddSkellyMeshStrategies.BY_VERTEX_GROUP:
        attach_skelly_by_vertex_group(
            skelly_mesh_path=SKELLY_FULL_MESH_PATH,
            rig=rig,
            vertex_groups=deepcopy(_SKELLY_VERTEX_GROUPS),
        )
    else:
        raise ValueError("Invalid add_mesh_method")


