from typing import Dict

import bpy

from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.put_sphere_at_location import \
    put_sphere_mesh_at_location
from freemocap_blender_addon.utilities.color_generator import ColorType, generate_color


def put_spheres_on_empties(empties: Dict[str, bpy.types.Object],
                           parent_empty: bpy.types.Object,
                           name_prefix: str = "",
                           color_type: ColorType = ColorType.VIVID,
                           emission_strength: float = 0.0,
                           sphere_scale: float = 0.025
                           ):
    if name_prefix:
        name_prefix += "_"

    meshes = []
    color = generate_color(color_type)
    for empty_name, empty in empties.items():
        bpy.ops.object.mode_set(mode="OBJECT")
        put_sphere_mesh_at_location(name=f"{name_prefix}{empty_name}",
                                    location=empty.location,
                                    sphere_scale=sphere_scale,
                                    color=color,
                                    emission_strength=emission_strength)

        bpy.ops.object.mode_set(mode="OBJECT")
        sphere_mesh = bpy.context.active_object
        constraint = sphere_mesh.constraints.new(type="COPY_LOCATION")
        constraint.target = empty
        sphere_mesh.parent = parent_empty

    return meshes
