import bpy


def create_base_of_support_geometry_nodes(base_of_support_mesh: bpy.types.Object,
                                          point_of_contact_radius: float,
                                          points_of_contact: list) -> None:
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    base_of_support_mesh.select_set(True)
    bpy.context.view_layer.objects.active = base_of_support_mesh

    # Add a geometry node to the angle base_of_support_mesh
    bpy.ops.node.new_geometry_nodes_modifier()

    # Change the name of the geometry node
    base_of_support_mesh.modifiers[0].name = "Geometry Nodes_" + base_of_support_mesh.name

    # Get the node tree and change its name
    node_tree = bpy.data.node_groups[0]
    node_tree.name = "Geometry Nodes_" + base_of_support_mesh.name

    # Get the Output node
    output_node = node_tree.nodes["Group Output"]

    # Add a Join Geometry Node
    join_geometry_node = node_tree.nodes.new(type='GeometryNodeJoinGeometry')

    # Add a Convex Hull Node
    convex_hull_node = node_tree.nodes.new(type='GeometryNodeConvexHull')

    # Add a Material node
    material_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")

    # Assign the material to the node
    node_tree.nodes["Material"].material = bpy.data.materials["Base of Support"]

    # Add a Set Material Node
    set_material_node = node_tree.nodes.new(type='GeometryNodeSetMaterial')

    # Connect the Material node to the Set Material Node
    node_tree.links.new(material_node.outputs["Material"], set_material_node.inputs["Material"])

    # Connect the Join Geometry node to the Convex Hull node
    node_tree.links.new(join_geometry_node.outputs["Geometry"], convex_hull_node.inputs["Geometry"])

    # Connect the Convex Hull node to the Set Material Node
    node_tree.links.new(convex_hull_node.outputs["Convex Hull"], set_material_node.inputs["Geometry"])

    # Connect the Set Material node to the Output node
    node_tree.links.new(set_material_node.outputs["Geometry"], output_node.inputs["Geometry"])

    # Add a new Circle Node for each point of contact
    for point in points_of_contact:
        # Add a new Circle Node
        mesh_circle_node = node_tree.nodes.new(type='GeometryNodeMeshCircle')

        # Change the node name
        mesh_circle_node.name = "Mesh Circle_" + point

        # Add a new Set Position Node
        set_position_node = node_tree.nodes.new(type='GeometryNodeSetPosition')

        # Change the node name
        set_position_node.name = "Set Position_" + point

        # Add a Switch Node
        switch_node = node_tree.nodes.new(type='GeometryNodeSwitch')
        switch_node.name = "Switch_" + point

        # Connect the Circle Node to the Set Position Node
        node_tree.links.new(mesh_circle_node.outputs["Mesh"], set_position_node.inputs["Geometry"])

        # Connect the Set Position Node to the Switch Node
        node_tree.links.new(set_position_node.outputs["Geometry"], switch_node.inputs["True"])

        # Connect the Switch Node to the Join Geometry node
        node_tree.links.new(switch_node.outputs["Output"], join_geometry_node.inputs["Geometry"])

        # Set the default values (radius and center)
        mesh_circle_node.inputs[1].default_value = point_of_contact_radius / 100
