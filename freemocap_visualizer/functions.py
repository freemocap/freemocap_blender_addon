import bpy
import re
import mathutils
import math as m
import numpy as np

try:
    from scipy.spatial import ConvexHull
except ImportError:
    print("scipy module is not installed. Please install scipy to use this addon.")
    print("run the command: 'C:\Program Files\Blender Foundation\Blender 3.6\3.6\python\bin> .\python.exe -m pip install scipy'")
    print("Replace the blender installation folder to match your installation.")

try:
    from shapely.geometry import Point, Polygon
except ImportError:
    print("shapely module is not installed. Please install shapely to use this addon.")
    print("run the command: 'C:\Program Files\Blender Foundation\Blender 3.6\3.6\python\bin> .\python.exe -m pip install shapely'")
    print("Replace the blender installation folder to match your installation.")

from .data_definitions import joints_angle_points, points_of_contact
from .auxiliary_functions import hide_objects

# Function to toggle the visibility of the output elements.
# It uses the parent_pattern to operate on the correct elements
def toggle_element_visibility(self,
                              context,
                              panel_property: str,
                              parent_pattern: str,
                              toggle_children_not_parent: bool,)->None:

    for data_object in bpy.data.objects:
        if re.search(parent_pattern, data_object.name):
            hide_objects(data_object,
                         not bool(self[panel_property]),
                         toggle_children_not_parent)

# Function to toggle the visibility of the motion paths
def toggle_motion_path(self,
                       context,
                       panel_property: str,
                       data_object: str,
                       show_line: bool = True,
                       line_thickness: int = 6,
                       use_custom_color: bool = False,
                       line_color: tuple = (0.5, 1.0, 0.8),
                       frames_before: int = 10,
                       frames_after: int = 10,
                       frame_step: int = 1,
                       show_frame_numbers: bool = False,
                       show_keyframes: bool = False,
                       show_keyframe_number: bool = False)->None:

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get reference to the object
    obj = bpy.data.objects[data_object]

    # Select the object
    obj.select_set(True)

    # Set the object as active object
    bpy.context.view_layer.objects.active = obj

    if bool(self[panel_property]):
        # Calculate paths
        bpy.ops.object.paths_calculate(display_type='CURRENT_FRAME', range='SCENE')
        # Set motion path properties for the specific object
        if obj.motion_path:
            obj.motion_path.lines = show_line
            obj.motion_path.line_thickness = line_thickness
            obj.motion_path.use_custom_color = use_custom_color
            obj.motion_path.color = line_color
            obj.animation_visualization.motion_path.frame_before = frames_before
            obj.animation_visualization.motion_path.frame_after = frames_after
            obj.animation_visualization.motion_path.frame_step = frame_step
            obj.animation_visualization.motion_path.show_frame_numbers = show_frame_numbers
            obj.animation_visualization.motion_path.show_keyframe_highlight = show_keyframes
            obj.animation_visualization.motion_path.show_keyframe_numbers = show_keyframe_number
    else:
        bpy.ops.object.paths_clear(only_selected=True)

# Function to add the COM Vertical Projection as COM mesh copy locked to the z axis floor plane
def add_com_vertical_projection(neutral_color: tuple,
                                in_bos_color: tuple,
                                out_bos_color: tuple)->None:

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Add a sphere mesh to the scene
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False,
                                         align='WORLD',
                                         location=(0, 0, 0),
                                         scale=(0.05, 0.05, 0.05))
    
    # Change the name of the sphere mesh
    bpy.context.active_object.name = "COM_Vertical_Projection"

    # Get the mesh object
    COM_mesh = bpy.data.objects["COM_Vertical_Projection"]

    # Parent the sphere mesh to the capture origin empty
    for data_object in bpy.data.objects:
        if re.search(r'_origin\Z', data_object.name):
            # Set the object as the COM vertical projection parent
            COM_mesh.parent = data_object
            break

    # Create the mesh materials
    bpy.ops.material.new()
    bpy.data.materials["Material"].name = "COM_Vertical_Projection_Neutral"
    COM_mesh.data.materials.append(bpy.data.materials["COM_Vertical_Projection_Neutral"])
    # Change the color of the material
    bpy.data.materials["COM_Vertical_Projection_Neutral"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = neutral_color
    bpy.data.materials["COM_Vertical_Projection_Neutral"].diffuse_color = neutral_color

    bpy.ops.material.new()
    bpy.data.materials["Material"].name = "COM_Vertical_Projection_In_BOS"
    COM_mesh.data.materials.append(bpy.data.materials["COM_Vertical_Projection_In_BOS"])
    # Change the color of the material
    bpy.data.materials["COM_Vertical_Projection_In_BOS"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = in_bos_color
    bpy.data.materials["COM_Vertical_Projection_In_BOS"].diffuse_color = in_bos_color

    bpy.ops.material.new()
    bpy.data.materials["Material"].name = "COM_Vertical_Projection_Out_BOS"
    COM_mesh.data.materials.append(bpy.data.materials["COM_Vertical_Projection_Out_BOS"])
    # Change the color of the material
    bpy.data.materials["COM_Vertical_Projection_Out_BOS"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = out_bos_color
    bpy.data.materials["COM_Vertical_Projection_Out_BOS"].diffuse_color = out_bos_color

    # Create a Geometry Nodes modifier to switch the material depending on the BOS intersection
    bpy.ops.node.new_geometry_nodes_modifier()

    # Change the name of the geometry node
    COM_mesh.modifiers[0].name = "Geometry Nodes_" + COM_mesh.name
   
    # Get the node tree and change its name
    node_tree = bpy.data.node_groups[0]
    node_tree.name = "Geometry Nodes_" + COM_mesh.name

    # Get the Input and Output nodes
    input_node = node_tree.nodes["Group Input"]
    output_node = node_tree.nodes["Group Output"]

    # Add the Material node for the Neutral Material
    material_neutral_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")
    # Change the node name
    material_neutral_node.name = "Material Neutral"
    # Assign the material to the node
    node_tree.nodes["Material Neutral"].material = bpy.data.materials["COM_Vertical_Projection_Neutral"]

    # Add the Material node for the In BOS Material
    material_in_bos_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")
    # Change the node name
    material_in_bos_node.name = "Material In BOS"
    # Assign the material to the node
    node_tree.nodes["Material In BOS"].material = bpy.data.materials["COM_Vertical_Projection_In_BOS"]

    # Add the Material node for the Out BOS Material
    material_out_bos_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")
    # Change the node name
    material_out_bos_node.name = "Material Out BOS"
    # Assign the material to the node
    node_tree.nodes["Material Out BOS"].material = bpy.data.materials["COM_Vertical_Projection_Out_BOS"]

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
    set_material_node =  node_tree.nodes.new(type="GeometryNodeSetMaterial")

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

    # Add a copy location constraint to the COM vertical projection
    bpy.ops.object.constraint_add(type='COPY_LOCATION')

    # Set the copy location target as the Center of Mass mesh
    COM_mesh.constraints["Copy Location"].target = bpy.data.objects["center_of_mass_mesh"]

    # Disable the constraint on the z axis constraint
    COM_mesh.constraints["Copy Location"].use_z = False

# Function to add angle meshes, set a copy location constraint to a joint
def add_angle_meshes(points: dict,
                     mesh_type: str)->dict:

    angle_meshes = {}

    for point in points:

        if mesh_type == 'angle':
            # Add a circle mesh to the scene
            bpy.ops.mesh.primitive_circle_add(enter_editmode=False,
                                            align='WORLD',
                                            location=(0, 0, 0),
                                            radius=0.05,
                                            fill_type='NGON')
        
            # Change the name of the circle mesh
            bpy.context.active_object.name = "angle_" + point

            # Add a copy location constraint to the angle mesh
            bpy.ops.object.constraint_add(type='COPY_LOCATION')

            # Set the copy location target as the joint object
            bpy.context.object.constraints["Copy Location"].target = bpy.data.objects[point]

            # Append the angle mesh to the angle meshes dictionary
            angle_meshes[point] = bpy.data.objects["angle_" + point]

        elif mesh_type == 'text':

            # Add a text mesh to the scene
            bpy.ops.object.text_add(enter_editmode=False,
                                    align='WORLD',
                                    location=(0, 0, 0),
                                    rotation=(m.radians(90), 0, 0),
                                    scale=(1, 1, 1))

            # Change the name of the text mesh
            bpy.context.active_object.name = "angleText_" + point

            # Add a copy location constraint to the text mesh
            bpy.ops.object.constraint_add(type='COPY_LOCATION')

            # Set the copy location target as the joint object
            bpy.context.object.constraints["Copy Location"].target = bpy.data.objects[point]

            # Append the text mesh to the angle meshes dictionary
            angle_meshes[point] = bpy.data.objects["angleText_" + point]

    return angle_meshes

# Function to parent meshes (create parent if it doesn't exist)
def parent_meshes(parent: str,
                  meshes: dict)->None:

    # Create a new empty object to be the parent of the angle meshes
    if bpy.data.objects.get(parent) is None:
        bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        # Rename the empty object
        bpy.context.active_object.name = parent

    # Parent the angle meshes to the empty object
    bpy.ops.object.select_all(action='DESELECT')
    for mesh in meshes:
        meshes[mesh].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[parent]
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

    # Parent the joint_angles_parent object to the capture origin empty
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[parent].select_set(True)
    for data_object in bpy.data.objects:
        if re.search(r'_origin\Z', data_object.name):
            bpy.context.view_layer.objects.active = data_object
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

    # Hide the joint_angles_parent object
    bpy.data.objects[parent].hide_set(True)

# Function to create geometry nodes
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

    elif mesh_type == 'base_of_support':

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Get the mesh object
        mesh = meshes['base_of_support']

        # Select the mesh
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
            mesh_circle_node.inputs[1].default_value = meshes['point_of_contact_radius'] / 100
            
# Function to animate the angle meshes rotation, arc nodes sweep angle and text mesh
def animate_angle_meshes(joints_angle_points: dict,
                         meshes: dict,
                         text_meshes: dict)->None:

    scene = bpy.context.scene

    # Get current frame
    current_frame = scene.frame_current

    for frame in range(scene.frame_start, scene.frame_end):

        scene.frame_set(frame)

        for mesh in meshes:

            # Get reference to the joint point
            joint_point = bpy.data.objects[mesh]

            # Get reference to the points comforming the angle
            parent_point = bpy.data.objects[joints_angle_points[mesh]['parent']]
            child_point = bpy.data.objects[joints_angle_points[mesh]['child']]

            # Get the parent and child vectors
            parent_vector = parent_point.matrix_world.translation - joint_point.matrix_world.translation
            child_vector = child_point.matrix_world.translation - joint_point.matrix_world.translation

            # Calculate the cross vector of the parent and child vectors to get their location plane
            cross_vector = parent_vector.cross(child_vector)

            # Get the local z-axis of the angle mesh
            local_z = meshes[mesh].matrix_world.to_quaternion() @ mathutils.Vector((0, 0, 1))

            # Calculate the rotation matrix to align the local z with the cross vector
            rotation_matrix = local_z.rotation_difference(cross_vector).to_matrix().to_4x4()

            # Apply the rotation to the angle mesh
            meshes[mesh].matrix_world = rotation_matrix @ meshes[mesh].matrix_world

            # Insert a keyframe for the mesh rotation
            meshes[mesh].keyframe_insert(data_path="rotation_euler", frame=frame)

            # Get the new local x and y axis
            new_local_x = meshes[mesh].matrix_world.to_quaternion() @ mathutils.Vector((1, 0, 0))
            new_local_y = meshes[mesh].matrix_world.to_quaternion() @ mathutils.Vector((0, 1, 0))

            # Get the angles between the new local x axis and the parent and child vectors
            nlx_parent_angle = m.degrees(new_local_x.angle(parent_vector))
            nlx_child_angle = m.degrees(new_local_x.angle(child_vector))

            # Get the dot product between the new local y axis and the parent and child vectors
            nly_parent_dot = new_local_y.dot(parent_vector)
            nly_child_dot = new_local_y.dot(child_vector)

            # Get the angles around the cross vector (if the dot product is negative, angle = 360 - angle)
            if nly_parent_dot >= 0:
                nlx_parent_angle_norm = 360 - nlx_parent_angle
            else:
                nlx_parent_angle_norm = nlx_parent_angle

            if nly_child_dot < 0:
                nlx_child_angle = 360 - nlx_child_angle
            
            # Get the arc start angle
            arc_start_angle = 360 - nlx_parent_angle_norm

            # Get the arc sweep angle
            arc_sweep_angle = (nlx_parent_angle_norm + nlx_child_angle) % 360

            # Set the arc node start angle
            meshes[mesh].modifiers[0].node_group.nodes["Arc"].inputs[5].default_value = m.radians(arc_start_angle)
            # Set the arc node sweep angle
            meshes[mesh].modifiers[0].node_group.nodes["Arc"].inputs[6].default_value = m.radians(arc_sweep_angle)

            # Insert a keyframe for the arc node sweep angle
            meshes[mesh].modifiers[0].node_group.nodes["Arc"].inputs[5].keyframe_insert(data_path='default_value', frame=frame)
            meshes[mesh].modifiers[0].node_group.nodes["Arc"].inputs[6].keyframe_insert(data_path='default_value', frame=frame)

            # Set the sweep angle in the String to Curves string value
            text_meshes[mesh].modifiers[0].node_group.nodes["Value to String"].inputs[0].default_value = round(arc_sweep_angle, 1)

            # Insert a keyframe to the corresponding text mesh
            text_meshes[mesh].modifiers[0].node_group.nodes["Value to String"].inputs[0].keyframe_insert(data_path='default_value', frame=frame)

    # Restore the current frame
    scene.frame_current = current_frame

# Function to animate the base of support depending on the z coordinate of the contact points
def animate_base_of_support(points_of_contact: list, base_of_support: bpy.types.Object, z_threshold: float):
    
    scene = bpy.context.scene

    # Get the current frame
    current_frame = scene.frame_current

    for frame in range(scene.frame_start, scene.frame_end):

        scene.frame_set(frame)

        # Variable to save if the base of support is visible or not (at least one point is below the threshold)
        base_of_support_visible = False

        for point in points_of_contact:
            
            # Get the z coordinate of the point
            point_z = bpy.data.objects[point].matrix_world.translation.z

            # If the z coordinate is less than the threshold, update the point circle mesh node location and enable it
            if point_z < z_threshold:

                base_of_support_visible = True

                # Update the x and y coordinates of the offset of the Set Position node
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Set Position_" + point].inputs[3].default_value[0] = bpy.data.objects[point].matrix_world.translation.x
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Set Position_" + point].inputs[3].default_value[1] = bpy.data.objects[point].matrix_world.translation.y

                # Insert a keyframe to the corresponding point
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Set Position_" + point].inputs[3].keyframe_insert(data_path='default_value', frame=frame)

                # Enable the Mesh Switch node
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + point].inputs[1].default_value = True

                # Insert a keyframe to the corresponding point
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + point].inputs[1].keyframe_insert(data_path='default_value', frame=frame)

            else:

                # Disable the Circle Mesh node
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + point].inputs[1].default_value = False

                # Insert a keyframe to the corresponding point
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + point].inputs[1].keyframe_insert(data_path='default_value', frame=frame)

        # Check if the COM Vertical Projection is intersecting with the base of support to change its material accordingly
        if base_of_support_visible:

            # Enable the BOS Visible Switch
            bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["BOS Visible Switch"].inputs[1].default_value = True
            
            # Get the location of the COM Vertical Projection
            com_vertical_projection_location = bpy.data.objects["COM_Vertical_Projection"].matrix_world.translation
            # Get the evaluated object with applied Geometry Nodes
            evaluated_object = base_of_support.evaluated_get(bpy.context.evaluated_depsgraph_get())

            # Get the a list of the coordinates of the points comforming the base of support
            BOS_points = [v.co for v in evaluated_object.data.vertices]
            # Create the polygon object as a list of 2D points tuples from the x and y coordinates
            points = np.array([(v[0], v[1]) for v in BOS_points])

            # Create a convex hull from the list of 2D points
            hull = ConvexHull(points)

            # Get the indices of the points that form the convex hull
            indices = hull.vertices

            # Create a new list of consecutive points based on the convex hull indices
            consecutive_points = [points[i] for i in indices]
            
            # Initiate the Shapely objects
            point = Point(com_vertical_projection_location[0], com_vertical_projection_location[1])
            polygon = Polygon(consecutive_points)

            # Check if the COM Vertical Projection is intersecting with the base of support
            if polygon.contains(point):
                # Change the material of the COM Vertical Projection to In Base of Support
                bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["In-Out BOS Switch"].inputs[1].default_value = True
            else:
                # Change the material of the COM Vertical Projection to Out Base of Support
                bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["In-Out BOS Switch"].inputs[1].default_value = False

        else:
            # Disable the BOS Visible Switch
            bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["BOS Visible Switch"].inputs[1].default_value = False

        # Insert a keyframe to the COM Vertical Projection switch nodes
        bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["In-Out BOS Switch"].inputs[1].keyframe_insert(data_path='default_value', frame=frame)
        bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["BOS Visible Switch"].inputs[1].keyframe_insert(data_path='default_value', frame=frame)

    # Restore the current frame
    scene.frame_current = current_frame

# Function to add the joint angles
def add_joint_angles(angles_color: tuple,
                     text_color: tuple)->None:

    # Create the materials
    bpy.data.materials.new(name = "Angle Mesh")
    bpy.data.materials["Angle Mesh"].diffuse_color = angles_color
    bpy.data.materials.new(name = "Angle Text")
    bpy.data.materials["Angle Text"].diffuse_color = text_color

    # Add the angle meshes
    angle_meshes = add_angle_meshes(joints_angle_points, 'angle')

    # Add the text meshes
    angleText_meshes = add_angle_meshes(joints_angle_points, 'text')

    # Parent the angle and text meshes to a empty object
    parent_meshes('joint_angles_parent', angle_meshes)
    parent_meshes('joint_angles_parent', angleText_meshes)

    # Create Geometry Nodes for each angle mesh
    create_geometry_nodes(angle_meshes, 'angle')

    # Create the Geometry Nodes for each text mesh
    create_geometry_nodes(angleText_meshes, 'text')

    # Animate the angle meshes
    animate_angle_meshes(joints_angle_points, angle_meshes, angleText_meshes)

    return

# Function to add the base of support
def add_base_of_support(z_threshold: float,
                        point_of_contact_radius: float,
                        color: tuple)->None:

    # Create the material
    bpy.data.materials.new(name = "Base of Support")
    bpy.data.materials["Base of Support"].diffuse_color = color

    # Add a plane mesh
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False,
                                    align='WORLD',
                                    location=(0, 0, 0.01),
                                    scale=(1, 1, 1))

    # Change the name of the plane mesh
    bpy.context.active_object.name = "base_of_support"

    #  Get reference to the plane mesh
    base_of_support = bpy.data.objects["base_of_support"]

    # Parent the sphere mesh to the capture origin empty
    for data_object in bpy.data.objects:
        if re.search(r'_origin\Z', data_object.name):
            # Set the object as the COM vertical projection parent
            base_of_support.parent = data_object
            break

    # Create Geometry Nodes for the base of support
    create_geometry_nodes(
        {
            'base_of_support': base_of_support,
            'point_of_contact_radius': point_of_contact_radius,
        },
        'base_of_support'
    )

    # Animate the base of support
    animate_base_of_support(points_of_contact, base_of_support, z_threshold=z_threshold)

    return
