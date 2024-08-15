import bpy

def add_background_planes(
    scene: bpy.types.Scene,
) -> None:
    background_plane = add_plane(
        scene=scene,
        location=(0, 0, 0),
        normal=(0, 0, 0),
        side_length=14,
        name='background_plane',
    )

    add_checkerboard_material(background_plane)

    return

def add_plane(
    scene: bpy.types.Scene,
    location: tuple[float, float, float],
    normal: tuple[float, float, float],
    side_length: float,
    name: str,
) -> bpy.types.Object:
    plane = bpy.ops.mesh.primitive_plane_add(
        size=side_length,
        enter_editmode=False,
        align='WORLD',
        location=location,
        scale=(1, 1, 1)
    )

    # Set plane name
    plane = bpy.context.active_object
    plane.name = name

    scene.collection.objects.link(plane)

    return plane

def add_checkerboard_material(
    plane_object: bpy.types.Object
) -> None:
    # Create the background material
    background_material = bpy.data.materials.new(name=plane_object.name + "_Material")
    background_material.use_nodes = True

    # Get the material node tree
    material_node_tree = background_material.node_tree

    # Create the texture node
    texture_node = material_node_tree.nodes.new(type="ShaderNodeTexChecker")
    # Set second color
    texture_node.inputs[2].default_value = (0, 0, 0, 1)
    # Set total scale as the side of the plane
    texture_node.inputs[3].default_value = plane_object.dimensions.x

    # Link the node to the material
    material_node_tree.links.new(
        texture_node.outputs["Color"],
        material_node_tree.nodes["Principled BSDF"].inputs["Base Color"]
    )

    # Assign the material to the object
    plane_object.data.materials.append(background_material)
    plane_object.active_material.use_backface_culling = True

    return
    