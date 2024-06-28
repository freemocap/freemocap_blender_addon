import bpy

from ajc27_freemocap_blender_addon.core_functions.materials.create_checkerboard_material import \
    create_checkerboard_material


def create_center_of_mass_mesh(parent_object: bpy.types.Object,
                               center_of_mass_empty: bpy.types.Object):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, enter_editmode=False,
                                         align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    mesh = bpy.context.active_object
    mesh.name = "center_of_mass_mesh"
    mesh.parent = parent_object
    mesh.parent = center_of_mass_empty
    location_constraint = mesh.constraints.new(type="COPY_LOCATION")
    location_constraint.target = center_of_mass_empty

    center_of_mass_material = create_checkerboard_material(name="center_of_mass_material",
                                                           square_scale=2,
                                                           color1=(0, .5, 1, 1),
                                                           color2=(1, 0, 1, 1),
                                                           roughness=0.5,
                                                           metallic=0.0,
                                                           noise_scale=0.5)

    mesh.active_material = center_of_mass_material
    mesh.data.materials.append(center_of_mass_material)
