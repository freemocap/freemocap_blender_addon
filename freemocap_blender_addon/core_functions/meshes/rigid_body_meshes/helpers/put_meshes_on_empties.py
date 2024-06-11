from typing import Dict, Tuple

import bpy
import numpy as np

from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.make_bone_mesh import make_rigid_body_mesh
from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.put_sphere_at_location import \
    put_sphere_mesh_at_location
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions


def put_rigid_body_meshes_on_empties(empties: Dict[str, bpy.types.Object],
                                     segment_definitions: RigidSegmentDefinitions,
                                     parent_empty: bpy.types.Object,
                                     name_prefix: str = ""):
    if name_prefix:
        name_prefix += "_"
    for segment_name, segment in segment_definitions.items():
        print(
            f"Creating rigid body mesh for segment: {segment_name} with parent: {segment.parent} and child: {segment.child} and length: {segment.length:.3f}m")
        color, squish_scale = get_rigid_body_mesh_color_and_squish(segment=segment_name)

        bone_mesh = make_rigid_body_mesh(name=f"{name_prefix}{segment_name}_rigid_body_mesh",
                                         length=segment.length,
                                         squish_scale=squish_scale,
                                         joint_color=color,
                                         cone_color=color,
                                         axis_visible=False
                                         )
        location_constraint = bone_mesh.constraints.new(type="COPY_LOCATION")
        location_constraint.target = empties[segment.parent]

        track_to_constraint = bone_mesh.constraints.new(type="DAMPED_TRACK")
        track_to_constraint.target = empties[segment.child]
        track_to_constraint.track_axis = "TRACK_Z"
        bone_mesh.parent = parent_empty


def put_spheres_on_empties(empties: Dict[str, bpy.types.Object],
                           parent_empty: bpy.types.Object,
                           name_prefix: str = ""):
    if name_prefix:
        name_prefix += "_"

    meshes = []
    emission_strength = 1.0
    color, emission_strength, sphere_scale = get_segment_mesh_settings(emission_strength=emission_strength)

    for empty_name, empty in empties.items():
        bpy.ops.object.mode_set(mode="OBJECT")
        put_sphere_mesh_at_location(name=f"{name_prefix}empty_name",
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


def get_rigid_body_mesh_color_and_squish(segment: str) -> Tuple[str, Tuple[float, float, float]]:
    squish_scale = (.8, 1, 1)
    if not "hand" in segment:
        if "right" in segment:
            color = "#FF0000"
        elif "left" in segment:
            color = "#0000FF"
        else:
            color = "#002500"
            squish_scale = (1.0, 1.0, 1.0)

    else:
        if "right" in segment:
            color = "#FF00FF"

        elif "left" in segment:
            color = "#00FFFF"

        else:
            raise ValueError(f"All hand bones must have 'right' or 'left' in their name, not {segment}")
    return color, squish_scale


def generate_random_hex_color() -> str:
    """
    Generate a random hex color code.

    Returns
    -------
    str
        A string representing a random hex color code in the format '#RRGGBB'.

    Examples
    --------
    >>> generate_random_hex_color()
    '#1A2B3C'
    """
    return f'#{np.random.randint(0, 0xFFFFFF):06X}'


def get_segment_mesh_settings(component_name: str = None,
                              emission_strength: float = None) -> Tuple[str, float, float]:
    color = generate_random_hex_color()
    sphere_scale = .025

    if component_name == "body":
        if "right" in component_name:
            color = "#FF0000"
        elif "left" in component_name:
            color = "#0000FF"
        else:
            color = "#610088"
        sphere_scale = .025
    elif component_name == "left_hand":
        color = "#00FFFF"
        sphere_scale = .025
    elif component_name == "right_hand":
        color = "#FF00FF"
        sphere_scale = .025
    elif component_name == "other":
        color = "#00FF77"
        sphere_scale = .04
        emission_strength = 100
    return color, emission_strength, sphere_scale
