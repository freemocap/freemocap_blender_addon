import os
import addon_utils
import bpy
import random
from math import radians

def add_render_background(
    scene: bpy.types.Scene=None,
    export_profile: str = None,
) -> None:
    
    if export_profile == 'showcase':

        # Create the background material
        background_material = bpy.data.materials.new(name="Background_Material")
        background_material.use_nodes = True

        # Get the material node tree
        material_node_tree = background_material.node_tree

        # Create the texture node
        texture_node = material_node_tree.nodes.new(type="ShaderNodeTexGradient")
        texture_node.gradient_type = 'SPHERICAL'

        # Link the node to the material
        material_node_tree.links.new(
            texture_node.outputs["Color"],
            material_node_tree.nodes["Principled BSDF"].inputs["Base Color"]
        )

        # Add a plane mesh
        bpy.ops.mesh.primitive_plane_add(
            enter_editmode=False,
            align='WORLD',
            size=10.0,
            location=(0, 4.3, 0),
            rotation=(radians(90), 0, 0),
            scale=(1, 1, 1)
        )

        # Change the name of the plane mesh
        bpy.context.active_object.name = "background"

        #  Get reference to the plane mesh
        background = bpy.data.objects["background"]

        # Select the mesh
        background.select_set(True)
        bpy.context.view_layer.objects.active = background

        # Add a geometry node to the angle mesh
        bpy.ops.node.new_geometry_nodes_modifier()

        # Change the name of the geometry node
        background.modifiers[0].name = "Geometry_Nodes_Background"

        # Get the node tree and change its name
        node_tree = bpy.data.node_groups[0]
        node_tree.name = "Geometry_Nodes_Background"

        # Get the Input and Output nodes
        input_node = node_tree.nodes["Group Input"]
        input_node.location = (-600, 300)
        output_node = node_tree.nodes["Group Output"]
        output_node.location = (1200, 300)

        # Add the modification nodes
        subdivide_mesh_node = node_tree.nodes.new(type='GeometryNodeSubdivideMesh')
        subdivide_mesh_node.inputs[1].default_value = 6
        triangulate_node = node_tree.nodes.new(type='GeometryNodeTriangulate')
        triangulate_node.location = (200, 300)

        combine_xyz_node = node_tree.nodes.new(type='ShaderNodeCombineXYZ')
        combine_xyz_node.location = (-200, -300)
        random_x_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
        random_y_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
        random_z_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
        random_x_node.location = (-500, -300)
        random_y_node.location = (-500, -500)
        random_z_node.location = (-500, -700)

        # Set min and max values
        random_x_node.inputs[2].default_value = -0.01
        random_y_node.inputs[2].default_value = -0.01
        random_z_node.inputs[2].default_value = 0
        random_x_node.inputs[3].default_value = 0.01
        random_y_node.inputs[3].default_value = 0.01
        random_z_node.inputs[3].default_value = 0.3
        # Set the random seed values
        random_x_node.inputs[8].default_value = random.randrange(0, 100)
        random_y_node.inputs[8].default_value = random.randrange(0, 100)
        random_z_node.inputs[8].default_value = random.randrange(0, 100)
        # Connect the random nodes
        node_tree.links.new(random_x_node.outputs[1], combine_xyz_node.inputs['X'])
        node_tree.links.new(random_y_node.outputs[1], combine_xyz_node.inputs['Y'])
        node_tree.links.new(random_z_node.outputs[1], combine_xyz_node.inputs['Z'])

        dual_mesh_node = node_tree.nodes.new(type='GeometryNodeDualMesh')
        dual_mesh_node.location = (400, 300)

        transform_node = node_tree.nodes.new(type='GeometryNodeTransform')
        transform_node.inputs[2].default_value[2] = 0.785398
        transform_node.inputs[3].default_value[0] = 3
        transform_node.inputs[3].default_value[1] = 3
        transform_node.location = (600, 300)

        extrude_mesh_node = node_tree.nodes.new(type='GeometryNodeExtrudeMesh')
        extrude_mesh_node.location = (800, 300)

        set_material_node = node_tree.nodes.new(type='GeometryNodeSetMaterial')
        set_material_node.inputs[2].default_value = bpy.data.materials["Background_Material"]
        set_material_node.location = (1000, 300)

        # Connect the nodes
        node_tree.links.new(input_node.outputs["Geometry"],
                            subdivide_mesh_node.inputs["Mesh"])
        node_tree.links.new(subdivide_mesh_node.outputs["Mesh"],
                            triangulate_node.inputs["Mesh"])
        node_tree.links.new(triangulate_node.outputs["Mesh"],
                            dual_mesh_node.inputs["Mesh"])
        node_tree.links.new(dual_mesh_node.outputs["Dual Mesh"],
                            transform_node.inputs["Geometry"])
        node_tree.links.new(transform_node.outputs["Geometry"],
                            extrude_mesh_node.inputs["Mesh"])
        node_tree.links.new(combine_xyz_node.outputs["Vector"],
                            extrude_mesh_node.inputs["Offset"])
        node_tree.links.new(extrude_mesh_node.outputs["Mesh"],
                            set_material_node.inputs["Geometry"])
        node_tree.links.new(set_material_node.outputs["Geometry"],
                            output_node.inputs["Geometry"])

    return
