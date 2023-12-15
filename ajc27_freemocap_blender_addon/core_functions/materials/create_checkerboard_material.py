import bpy


def create_material_for_mesh(name: str):
    material = bpy.data.materials.new('')
    material.name = name
    material.use_nodes = True
    return material


def create_checker_texture(material,
                            color1: tuple,
                            color2: tuple,
                            scale: float):
    nodes = material.node_tree.nodes
    nodes.remove(nodes.get('Principled BSDF'))
    checker_node = nodes.new(type='ShaderNodeTexChecker')

    checker_node.inputs[1].default_value = (0, .5, 1, 1)  # color1
    checker_node.inputs[2].default_value = (1, 0, 1, 1)  # color2
    checker_node.inputs[3].default_value = 2.0  # scale

    return nodes, checker_node


def create_bsdf_and_output_nodes(nodes):
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    output_node = nodes.get('Material Output')
    return bsdf_node, output_node


def create_checkerboard_material(name: str,
                                 color1: tuple = (0, .5, 1, 1),
                                 color2: tuple = (1, 0, 1, 1),
                                 scale: float = 2.0,
                                 roughness: float = 0.5,
                                 metallic: float = 0.0,
                                 noise_scale: float = 0.5):
    material = bpy.data.materials.get(name)
    if material is None:
        material = create_material_for_mesh(name)
        nodes, checker_node = create_checker_texture(material=material,
                                                     color1=color1,
                                                     color2=color2,
                                                     scale=scale)
        bsdf_node, output_node = create_bsdf_and_output_nodes(nodes)
        # Connect the Checker Texture node to the BSDF
        material.node_tree.links.new(bsdf_node.inputs['Base Color'], checker_node.outputs['Color'])
        # Connect the BSDF to the output
        material.node_tree.links.new(output_node.inputs['Surface'], bsdf_node.outputs['BSDF'])
    return material
