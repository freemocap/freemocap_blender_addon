from typing import Dict, Tuple

import bpy

from freemocap_blender_addon.core_functions.meshes.rigid_body_meshes.helpers.make_rigid_body_mesh import \
    make_rigid_body_mesh
from freemocap_blender_addon.freemocap_data.data_paths.default_path_enums import RightLeft
from freemocap_blender_addon.freemocap_data_handler.operations.rigid_body_assumption.calculate_rigid_body_trajectories import \
    RigidSegmentDefinitions
from freemocap_blender_addon.utilities.color_generator import generate_color, ColorType


def put_rigid_body_meshes_on_empties(empties: Dict[str, bpy.types.Object],
                                     segment_definitions: RigidSegmentDefinitions,
                                     parent_empty: bpy.types.Object,
                                     name_prefix: str = ""):
    if name_prefix:
        name_prefix += "_"

    axial_color  = generate_color(ColorType.JEWEL)
    right_color  = "#BB0033"
    left_color   = "#0033BB"
    axial_sqush = (1.0, 1.0, 1.0)
    appendicular_sqush = (.8, 1, 1)

    def get_color_and_squish(segment_name: str) -> Tuple[str, Tuple[float, float, float]]:
        if RightLeft.RIGHT.value in segment_name:
            color = right_color
            squish_scale = appendicular_sqush
        elif RightLeft.LEFT.value in segment_name:
            color = left_color
            squish_scale = appendicular_sqush
        else:
            color = axial_color
            squish_scale = axial_sqush
        return color, squish_scale

    for segment_name, segment in segment_definitions.items():
        print(
            f"Creating rigid body mesh for segment: {segment_name} with parent: {segment.parent} and child: {segment.child} and length: {segment.length:.3f}m")

        color, squish_scale = get_color_and_squish(segment_name)

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


