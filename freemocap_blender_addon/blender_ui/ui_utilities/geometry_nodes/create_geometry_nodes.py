import bpy
def create_geometry_nodes(meshes: dict, mesh_type: str)->None:

    if mesh_type in ['angle', 'text']:

        for mesh_key in meshes:

            # Get the mesh object
            mesh = meshes[mesh_key]

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select the angle mesh
            mesh.select_set(True)
            bpy.context.view_layer.objects.active = mesh

            # Add a geometry node to the angle mesh
            bpy.ops.node.new_geometry_nodes_modifier()

            # Change the name of the geometry node
            mesh.modifiers[0].name = "Geometry Nodes_" + mesh.name

            # Get the node tree and change its name
            node_tree = bpy.data.node_groups[0]
            node_tree.name = "Geometry Nodes_" + mesh.name

            # Get the Output node
            output_node = node_tree.nodes["Group Output"]

            # Add nodes depending on the type of mesh
            if mesh_type == 'angle':

                # Add a new Arc Node
                arc_node = node_tree.nodes.new(type='GeometryNodeCurveArc')

                # Add a Fill Curve Node
                fill_curve_node = node_tree.nodes.new(type='GeometryNodeFillCurve')

                # Add a Material node
                material_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")

                # Assign the material to the node
                node_tree.nodes["Material"].material = bpy.data.materials["Angle Mesh"]

                # Add a Set Material Node
                set_material_node =  node_tree.nodes.new(type="GeometryNodeSetMaterial")

                # Connect the Material node to the Set Material Node
                node_tree.links.new(material_node.outputs["Material"], set_material_node.inputs["Material"])

                # Connect the Arc node to the Fill Curve node
                node_tree.links.new(arc_node.outputs["Curve"], fill_curve_node.inputs["Curve"])

                # Connect the Fill Curve node to the Set Material Node
                node_tree.links.new(fill_curve_node.outputs["Mesh"], set_material_node.inputs["Geometry"])

                # Connect the Set Material Node to the Output node
                node_tree.links.new(set_material_node.outputs["Geometry"], output_node.inputs["Geometry"])

                # Set the default values (number of sides, radius and connect center)
                arc_node.inputs[0].default_value = 32
                arc_node.inputs[4].default_value = 0.07
                arc_node.inputs[8].default_value = True

            elif mesh_type == 'text':

                # Add a new Value To String Function Node
                value_to_string_function_node = node_tree.nodes.new(type='FunctionNodeValueToString')

                # Add a new String to Curves Node
                string_to_curves_node = node_tree.nodes.new(type='GeometryNodeStringToCurves')

                # Add a new Fill Curve Node
                fill_curve_node = node_tree.nodes.new(type='GeometryNodeFillCurve')

                # Add a Material node
                material_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")

                # Assign the material to the node
                node_tree.nodes["Material"].material = bpy.data.materials["Angle Text"]

                # Add a Set Material Node
                set_material_node =  node_tree.nodes.new(type="GeometryNodeSetMaterial")

                # Connect the Material node to the Set Material Node
                node_tree.links.new(material_node.outputs["Material"], set_material_node.inputs["Material"])

                # Connect the Value To String Function node to the String to Curves node
                node_tree.links.new(value_to_string_function_node.outputs["String"], string_to_curves_node.inputs["String"])

                # Connect the String to Curves node to the Fill Curve node
                node_tree.links.new(string_to_curves_node.outputs["Curve Instances"], fill_curve_node.inputs["Curve"])

                # Connect the Fill Curve node to the Set Material Node
                node_tree.links.new(fill_curve_node.outputs["Mesh"], set_material_node.inputs["Geometry"])

                # Connect the Set Material node to the Output node
                node_tree.links.new(set_material_node.outputs["Geometry"], output_node.inputs["Geometry"])

                # Mute the Fill Curve Node
                fill_curve_node.mute = False

                # Set the default values (text and font size)
                value_to_string_function_node.inputs[0].default_value = 0
                string_to_curves_node.inputs[1].default_value = 0.1

