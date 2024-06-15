from typing import Dict

import bpy

from freemocap_blender_addon.core_functions.empties.creation.create_empty_from_trajectory import ParentedEmpties
from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.put_sphere_at_location import \
    put_sphere_mesh_at_location
from freemocap_blender_addon.utilities.color_generator import ColorType, generate_color


def put_spheres_on_parented_empties(parented_empties: ParentedEmpties,
                                    color_type: ColorType = ColorType.VIVID,
                                    emission_strength: float = 0.0,
                                    sphere_scale: float = 0.025
                                    ):


    meshes = []
    color = generate_color(color_type)
    for empty_name, empty in parented_empties.empties.items():
        bpy.ops.object.mode_set(mode="OBJECT")
        put_sphere_mesh_at_location(name=f"{parented_empties.parent_name}_{empty_name}",
                                    location=empty.location,
                                    sphere_scale=sphere_scale,
                                    color=color,
                                    emission_strength=emission_strength)

        bpy.ops.object.mode_set(mode="OBJECT")
        sphere_mesh = bpy.context.active_object
        constraint = sphere_mesh.constraints.new(type="COPY_LOCATION")
        constraint.target = empty
        sphere_mesh.parent = parented_empties.parent_object

    return meshes
