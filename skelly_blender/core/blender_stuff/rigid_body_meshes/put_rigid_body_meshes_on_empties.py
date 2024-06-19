from typing import Tuple

from skelly_blender.core.blender_stuff.armature_rig.bone_constraints.bone_constraint_types import ConstraintType
from skelly_blender.core.blender_stuff.blender_type_hints import BlenderizedSegmentDefinitions
from skelly_blender.core.blender_stuff.color_generator import ColorType, generate_color
from skelly_blender.core.blender_stuff.keyframed_empties.empties_dataclasses import ParentedEmpties
from skelly_blender.core.blender_stuff.rigid_body_meshes.make_rigid_body_mesh import \
    make_rigid_body_mesh

DEFAULT_APPENDICULAR_RIGID_BODY_MESH_SQUISH = (.8, 1, 1)

DEFAULT_AXIAL_RIGID_BODY_MESH_SQUISH = (1.0, 1.0, 1.0)

DEFAULT_LEFT_SIDE_COLOR = "#0033BB"

DEFAULT_RIGHT_SIDE_COLOR = "#BB0033"


def put_rigid_body_meshes_on_empties(parented_empties: ParentedEmpties,
                                     segment_definitions: BlenderizedSegmentDefinitions,
                                     ):
    axial_color = generate_color(ColorType.JEWEL)
    right_color = DEFAULT_RIGHT_SIDE_COLOR
    left_color = DEFAULT_LEFT_SIDE_COLOR
    axial_squish = DEFAULT_AXIAL_RIGID_BODY_MESH_SQUISH
    appendicular_squish = DEFAULT_APPENDICULAR_RIGID_BODY_MESH_SQUISH

    def get_color_and_squish(segment_name: str) -> Tuple[str, Tuple[float, float, float]]:
        if ".R" in segment_name:
            mesh_color = right_color
            mesh_squish = appendicular_squish
        elif ".L" in segment_name:
            mesh_color = left_color
            mesh_squish = appendicular_squish
        else:
            mesh_color = axial_color
            mesh_squish = axial_squish
        return mesh_color, mesh_squish

    for segment_name, segment in segment_definitions.items():
        print(
            f"Creating rigid body mesh for segment: {segment_name} with length: {segment.length:.3f}m")
        color, squish = get_color_and_squish(segment_name)

        bone_mesh = make_rigid_body_mesh(
            name=f"{parented_empties.parent_name}_rigid_body_mesh_{segment_name}",
            length=segment.length,
            squish_scale=squish,
            joint_color=color,
            cone_color=color,
            axis_visible=False
        )
        location_constraint = bone_mesh.constraints.new(type=ConstraintType.COPY_LOCATION.value)
        location_constraint.target = parented_empties.empties[segment.parent]

        track_to_constraint = bone_mesh.constraints.new(type=ConstraintType.DAMPED_TRACK.value)
        track_to_constraint.target = parented_empties.empties[segment.child]
        track_to_constraint.track_axis = "TRACK_Z"
        bone_mesh.parent = parented_empties.parent_object
