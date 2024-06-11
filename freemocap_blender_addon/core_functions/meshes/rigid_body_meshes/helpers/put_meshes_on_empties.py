from typing import Dict, Tuple

import bpy

from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.put_sphere_at_location import \
    put_sphere_mesh_at_location


def put_rigid_body_meshes_on_empties(empties: Dict[str, bpy.types.Object],
                                     segment_lengths: Dict[str, float],
                                     parent_empty: bpy.types.Object):

    for parent_empty_name in empties.keys():
        print(f"Creating bone mesh for {parent_empty_name}...")
        color, squish_scale = get_rigid_body_mesh_color_and_squish(parent_empty_name)

        for child_name in MEDIAPIPE_HIERARCHY[parent_empty_name]["children"]:
            # segment length is the distance between the parent and child empty
            def find_bone(parent_name: str, child_name: str):
                for bone_name, bone in bone_data.items():
                    if bone.head == parent_name and bone.tail == child_name:
                        return bone
                return None
            bone = find_bone(parent_name=parent_empty_name, child_name=child_name)
            # print(f"Segment length for {parent_empty_name} to {child_name} is {bone_data[parent_empty_name].median:.3f}m")
            print(f"Segment length for {parent_empty_name} to {child_name} is {bone.median:.3f}m")
            bone_mesh = make_bone_mesh(name=f"{parent_empty_name}_bone_mesh",
                                       length=bone.median,
                                       squish_scale=squish_scale,
                                       joint_color=color,
                                       cone_color=color,
                                       axis_visible=False
                                       )
            location_constraint = bone_mesh.constraints.new(type="COPY_LOCATION")
            location_constraint.target = all_empties[parent_empty_name]

            track_to_constraint = bone_mesh.constraints.new(type="DAMPED_TRACK")
            track_to_constraint.target = all_empties[child_name]
            track_to_constraint.track_axis = "TRACK_Z"
            bone_mesh.parent = parent_empty


def put_spheres_on_empties(empties: Dict[str, bpy.types.Object],
                           parent_empty: bpy.types.Object):
    meshes = []
    emission_strength = 1.0
    color, emission_strength, sphere_scale = get_segment_mesh_settings(emission_strength=emission_strength)

    for empty_name, empty in empties.items():

        bpy.ops.object.mode_set(mode="OBJECT")
        sphere_mesh = put_sphere_mesh_at_location(name=empty_name,
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


def get_rigid_body_mesh_color_and_squish(parent_empty_name: str) -> Tuple[str, Tuple[float, float, float]]:
    squish_scale = (.8, 1, 1)
    if not "hand" in parent_empty_name:

        if "right" in parent_empty_name:
            color = "#FF0000"
        elif "left" in parent_empty_name:
            color = "#0000FF"
        else:
            color = "#002500"
            squish_scale = (1.0, 1.0, 1.0)

    else:
        if "right" in parent_empty_name:
            color = "#FF00FF"

        elif "left" in parent_empty_name:
            color = "#00FFFF"

        else:
            raise ValueError(f"All hand bones must have 'right' or 'left' in their name, not {parent_empty_name}")
    return color, squish_scale

import random

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
    return f'#{random.randint(0, 0xFFFFFF):06X}'

def get_segment_mesh_settings(component_name: str=None,
                              emission_strength: float=None) -> Tuple[str, float, float]:
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