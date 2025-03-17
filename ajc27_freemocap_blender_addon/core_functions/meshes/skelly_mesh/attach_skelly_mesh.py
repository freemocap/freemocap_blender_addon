from enum import Enum
import traceback
from pathlib import Path
from typing import Dict

from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.skelly_mesh_paths import SKELLY_FULL_MESH_PATH
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_bone_mesh import \
    attach_skelly_by_bone_mesh
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_full_mesh import \
    attach_skelly_complete_mesh
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.strategies.attach_skelly_by_vertex_groups import \
    attach_skelly_by_vertex_group
from ajc27_freemocap_blender_addon.data_models.armatures.armature_bone_info import ArmatureBoneInfo
from ajc27_freemocap_blender_addon.data_models.poses.pose_element import PoseElement
import bpy
from mathutils import Vector, Matrix, Euler
from copy import deepcopy

from ajc27_freemocap_blender_addon import PACKAGE_ROOT_PATH
from ajc27_freemocap_blender_addon.system.constants import (
    FREEMOCAP_ARMATURE,
    UE_METAHUMAN_SIMPLE_ARMATURE,
)
from ajc27_freemocap_blender_addon.data_models.data_references import ArmatureType, PoseType
from ajc27_freemocap_blender_addon.data_models.armatures.bone_name_map import (
    bone_name_map,
)
from ajc27_freemocap_blender_addon.data_models.meshes.skelly_bones import (
    get_skelly_bones,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.mesh_utilities import (
    get_bone_info,
    align_markers_to_armature,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.translate_vertex_groups import (
    translate_vertex_groups,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.scale_vertex_groups import (
    scale_vertex_groups,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.rotate_vertex_groups import (
    rotate_vertex_groups,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.parent_vertex_groups_to_armature import (
    parent_vertex_groups_to_armature,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.empty_markers_for_rest_pose import (
    _EMPTY_MARKERS,
)
from ajc27_freemocap_blender_addon.core_functions.meshes.skelly_mesh.helpers.skelly_vertex_groups import (
    _SKELLY_VERTEX_GROUPS,
)


class AddSkellyMeshStrategies(Enum):
    BY_BONE_MESH = "by_bone_mesh"
    COMPLETE_MESH = "complete_mesh"
    BY_VERTEX_GROUP = "by_vertex_group"

def attach_skelly_mesh_to_rig(
    data_parent_empty_name: str,
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
            data_parent_empty_name=data_parent_empty_name,
            skelly_mesh_path=SKELLY_FULL_MESH_PATH,
            rig=rig,
            vertex_groups=deepcopy(_SKELLY_VERTEX_GROUPS),
            empty_markers_reference=deepcopy(_EMPTY_MARKERS),
        )
    else:
        raise ValueError("Invalid add_mesh_method")


