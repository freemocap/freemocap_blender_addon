import bpy
import re
import mathutils
import math as m



# Function to draw a vector for debbuging purposes
def draw_vector(origin, angle, name):
    bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=origin,
                             rotation=mathutils.Vector([0, 0, 1]).rotation_difference(angle).to_euler(),
                             scale=(0.002, 0.002, 0.002))
    bpy.data.objects["Empty"].name = name

    bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(origin + angle * 0.5), scale=(0.001, 0.001, 0.001))
    bpy.data.objects["Empty"].scale = (0.01, 0.01, 0.01)
    bpy.data.objects["Empty"].name = 'Sphere_' + name

    return


# Function to check if a point is inside a polygon
def is_point_inside_polygon(x, y, polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


# Function to find the convex hull of a set of points
def graham_scan(points):
    # Function to determine the orientation of 3 points (p, q, r)
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else -1  # Clockwise or Counterclockwise

    # Sort the points based on their x-coordinates
    sorted_points = sorted(points, key=lambda point: (point[0], point[1]))

    # Initialize the stack to store the convex hull points
    stack = []

    # Iterate through the sorted points to find the convex hull
    for point in sorted_points:
        while len(stack) > 1 and orientation(stack[-2], stack[-1], point) != -1:
            stack.pop()
        stack.append(point)

    return stack


# Function to toggle the visibility of the output elements.
# It uses the parent_pattern to operate on the correct elements

# Function to add the COM Vertical Projection as COM mesh copy locked to the z axis floor plane

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
