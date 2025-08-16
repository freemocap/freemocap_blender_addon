import bpy
from ajc27_freemocap_blender_addon.data_models.joint_angles.joint_angles import joint_angles

def create_angle_geometry_nodes(
    meshes: dict,
    mesh_type: str,
    angle_radius: float = 10,
    overwrite_colors: bool = False,
    angle_mesh_color: tuple = (0.694,0.082,0.095,1.0),
    angle_text_color: tuple = (1.0,0.365,0.048,1.0),
    angle_text_size: float = 5.0,
    angle_text_local_x_offset: float = 3.0,
    angle_text_local_y_offset: float = 0.0,
) -> None:

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

            # Create the angle material if it doesn't exist
            material_name = 'angle_' + mesh_key
            if material_name not in bpy.data.materials.keys():
                bpy.data.materials.new(name = material_name)
            if overwrite_colors:
                bpy.data.materials[material_name].diffuse_color = angle_mesh_color
            else:
                bpy.data.materials[material_name].diffuse_color = joint_angles[mesh_key]['angle_color']

            # Assign the material to the node
            node_tree.nodes["Material"].material = bpy.data.materials[material_name]

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
            arc_node.inputs[4].default_value = angle_radius / 100
            arc_node.inputs[8].default_value = True

        elif mesh_type == 'angletext':

            # Add a new Value To String Function Node
            value_to_string_function_node = node_tree.nodes.new(type='FunctionNodeValueToString')

            # Add a new String to Curves Node
            string_to_curves_node = node_tree.nodes.new(type='GeometryNodeStringToCurves')

            # Add a new Fill Curve Node
            fill_curve_node = node_tree.nodes.new(type='GeometryNodeFillCurve')

            # Add a Material node
            material_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")

            # Create the angle material if it doesn't exist
            material_name = 'angletext_' + mesh_key
            if material_name not in bpy.data.materials.keys():
                bpy.data.materials.new(name = material_name)
            if overwrite_colors:
                bpy.data.materials[material_name].diffuse_color = angle_text_color
            else:
                bpy.data.materials[material_name].diffuse_color = joint_angles[mesh_key]['text_color']

            # Assign the material to the node
            node_tree.nodes["Material"].material = bpy.data.materials[material_name]

            # Add a Set Material Node
            set_material_node =  node_tree.nodes.new(type="GeometryNodeSetMaterial")

            # Add a Taansform Geometry Node
            transform_geometry_node = node_tree.nodes.new(type="GeometryNodeTransform")
            # Set the local transformations
            transform_geometry_node.inputs[1].default_value[0] = angle_text_local_x_offset / 100
            transform_geometry_node.inputs[1].default_value[1] = angle_text_local_y_offset / 100

            # Connect the Material node to the Set Material Node
            node_tree.links.new(material_node.outputs["Material"], set_material_node.inputs["Material"])

            # Connect the Value To String Function node to the String to Curves node
            node_tree.links.new(value_to_string_function_node.outputs["String"], string_to_curves_node.inputs["String"])

            # Connect the String to Curves node to the Fill Curve node
            node_tree.links.new(string_to_curves_node.outputs["Curve Instances"], fill_curve_node.inputs["Curve"])

            # Connect the Fill Curve node to the Set Material Node
            node_tree.links.new(fill_curve_node.outputs["Mesh"], set_material_node.inputs["Geometry"])

            # Connect the Set Material node to the Transform Geometry node
            node_tree.links.new(set_material_node.outputs["Geometry"], transform_geometry_node.inputs["Geometry"])

            # Connect the Transform Geometry node to the Output node
            node_tree.links.new(transform_geometry_node.outputs["Geometry"], output_node.inputs["Geometry"])

            # Mute the Fill Curve Node
            fill_curve_node.mute = False

            # Set the default values (text and font size)
            value_to_string_function_node.inputs[0].default_value = 0
            string_to_curves_node.inputs[1].default_value = angle_text_size / 100

    return
