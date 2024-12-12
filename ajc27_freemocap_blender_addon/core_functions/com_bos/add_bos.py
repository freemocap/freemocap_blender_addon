import bpy

from ajc27_freemocap_blender_addon.core_functions.com_bos.animate_bos_mesh import animate_base_of_support
from ajc27_freemocap_blender_addon.core_functions.com_bos.create_bos_geometry_nodes import \
    create_base_of_support_geometry_nodes
from ajc27_freemocap_blender_addon.data_models.mediapipe_names.mediapipe_biomechanics import ground_contact_points


def add_base_of_support(data_parent_empty: bpy.types.Object,
                        z_threshold: float,
                        point_of_contact_radius: float,
                        color: tuple) -> None:
    # Add a plane mesh
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False,
                                     align='WORLD',
                                     location=(0, 0, 0.002),
                                     scale=(1, 1, 1))

    # Change the name of the plane mesh
    bpy.context.active_object.name = "base_of_support"

    #  Get reference to the plane mesh
    base_of_support = bpy.data.objects["base_of_support"]
    base_of_support.parent = data_parent_empty

    # Create the material
    bpy.data.materials.new(name="Base of Support")
    bpy.data.materials["Base of Support"].diffuse_color = color

    # Create Geometry Nodes for the base of support
    create_base_of_support_geometry_nodes(
        base_of_support_mesh=base_of_support,
        point_of_contact_radius=point_of_contact_radius,
        points_of_contact=ground_contact_points

    )

    # Animate the base of support
    animate_base_of_support(data_parent_empty=data_parent_empty,
                            ground_contact_point_names=ground_contact_points,
                            base_of_support=base_of_support,
                            z_threshold=z_threshold)
