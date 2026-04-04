from enum import Enum

import bpy


class COMVerticalProjectionMaterial(Enum):
    NEUTRAL = "_Neutral"
    IN_BOS = "_In_BOS"
    OUT_BOS = "_Out_BOS"


COM_PROJECTION_MESH_NAME = "com_vertical_projection"


def add_com_vertical_projection(data_parent_empty: bpy.types.Object,
                                neutral_color: tuple,
                                in_bos_color: tuple,
                                out_bos_color: tuple) -> bpy.types.Object:
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Check if the COM_Vertical_Projection object exists, if it does, break
    for child in data_parent_empty.children:
        if COM_PROJECTION_MESH_NAME in child.name:
            print("COM Vertical Projection already exists, returning...")
            return

    # Add a sphere mesh to the scene
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False,
                                         align='WORLD',
                                         location=(0, 0, 0),
                                         scale=(0.025, 0.025, 0.025))

    # Get the newly created mesh object
    com_projection_mesh = bpy.context.active_object

    # Change the name of the sphere mesh
    bpy.context.active_object.name = COM_PROJECTION_MESH_NAME

    # Parent the sphere mesh to the Data Parent empty
    com_projection_mesh.parent = data_parent_empty

    # Add a copy location constraint to the COM vertical projection
    bpy.ops.object.constraint_add(type='COPY_LOCATION')

    # Set the copy location target as the Center of Mass emtpy
    for child in data_parent_empty.children:
        if "center_of_mass" in child.name and "mesh" not in child.name:
            com_projection_mesh.constraints["Copy Location"].target = child

    # Disable the constraint on the z axis constraint
    com_projection_mesh.constraints["Copy Location"].use_z = False

    # Create the materials for the COM vertical projection
    create_com_vertical_projection_materials(com_projection_mesh=com_projection_mesh,
                                             neutral_color=neutral_color,
                                             in_bos_color=in_bos_color,
                                             out_bos_color=out_bos_color)
    
    return com_projection_mesh


def create_com_vertical_projection_materials(com_projection_mesh: bpy.types.Object,
                                             neutral_color: tuple,
                                             in_bos_color: tuple,
                                             out_bos_color: tuple) -> None:
    
    # Create the mesh materials
    color_map = {
        COMVerticalProjectionMaterial.NEUTRAL: neutral_color,
        COMVerticalProjectionMaterial.IN_BOS: in_bos_color,
        COMVerticalProjectionMaterial.OUT_BOS: out_bos_color
    }

    for material_type in COMVerticalProjectionMaterial:
        bpy.ops.material.new()
        material_name = com_projection_mesh.name + material_type.value
        bpy.data.materials["Material"].name = material_name
        com_projection_mesh.data.materials.append(bpy.data.materials[material_name])
        # Change the color of the material
        bpy.data.materials[material_name].node_tree.nodes["Principled BSDF"].inputs[
            0].default_value = color_map[material_type]
        bpy.data.materials[material_name].diffuse_color = color_map[material_type]

    # Create a Geometry Nodes modifier to switch the material depending on the BOS intersection
    bpy.ops.node.new_geometry_nodes_modifier()

    # Change the name of the geometry node
    com_projection_mesh.modifiers[0].name = "Geometry Nodes_" + com_projection_mesh.name

    # Get the node tree and change its name
    node_tree = bpy.data.node_groups[0]
    node_tree.name = "Geometry Nodes_" + com_projection_mesh.name

    # Get the Input and Output nodes
    input_node = node_tree.nodes["Group Input"]
    output_node = node_tree.nodes["Group Output"]

    # Add the Material node for the Neutral Material
    material_neutral_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")
    # Change the node name
    material_neutral_node.name = "Material Neutral"
    # Assign the material to the node
    node_tree.nodes["Material Neutral"].material = bpy.data.materials[com_projection_mesh.name + COMVerticalProjectionMaterial.NEUTRAL.value]

    # Add the Material node for the In BOS Material
    material_in_bos_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")
    # Change the node name
    material_in_bos_node.name = "Material In BOS"
    # Assign the material to the node
    node_tree.nodes["Material In BOS"].material = bpy.data.materials[com_projection_mesh.name + COMVerticalProjectionMaterial.IN_BOS.value]

    # Add the Material node for the Out BOS Material
    material_out_bos_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")
    # Change the node name
    material_out_bos_node.name = "Material Out BOS"
    # Assign the material to the node
    node_tree.nodes["Material Out BOS"].material = bpy.data.materials[com_projection_mesh.name + COMVerticalProjectionMaterial.OUT_BOS.value]

    # Add a Switch Node for the In-Out BOS materials
    in_out_bos_switch_node = node_tree.nodes.new(type='GeometryNodeSwitch')
    # Change the node name
    in_out_bos_switch_node.name = "In-Out BOS Switch"

    # Change the input type of the in_out_bos switch node
    node_tree.nodes["In-Out BOS Switch"].input_type = 'MATERIAL'

    # Add a Switch Node for the BOS visible status
    bos_visible_switch_node = node_tree.nodes.new(type='GeometryNodeSwitch')
    # Change the node name
    bos_visible_switch_node.name = "BOS Visible Switch"

    # Change the input type of the in_out_bos switch node
    node_tree.nodes["BOS Visible Switch"].input_type = 'MATERIAL'

    # Add a Set Material Node
    set_material_node = node_tree.nodes.new(type="GeometryNodeSetMaterial")

    # Connect the material nodes to the two inputs of the switch node
    node_tree.links.new(material_out_bos_node.outputs["Material"], in_out_bos_switch_node.inputs["False"])
    node_tree.links.new(material_in_bos_node.outputs["Material"], in_out_bos_switch_node.inputs["True"])

    # Connect the neutral material node to the bos visible switch node
    node_tree.links.new(material_neutral_node.outputs["Material"], bos_visible_switch_node.inputs["False"])

    # Connect the in_out_bos switch node to the bos visible switch node
    node_tree.links.new(in_out_bos_switch_node.outputs["Output"], bos_visible_switch_node.inputs["True"])

    # Connect the bos visible switch node to the set material node
    node_tree.links.new(bos_visible_switch_node.outputs["Output"], set_material_node.inputs["Material"])

    # Connect the input node to the set material node
    node_tree.links.new(input_node.outputs["Geometry"], set_material_node.inputs["Geometry"])

    # Connect the set material node to the output node
    node_tree.links.new(set_material_node.outputs["Geometry"], output_node.inputs["Geometry"])
