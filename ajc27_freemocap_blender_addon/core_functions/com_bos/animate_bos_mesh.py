import bpy

from ajc27_freemocap_blender_addon.core_functions.com_bos.add_com_vertical_projection import COM_PROJECTION_MESH_NAME

import numpy as np

def animate_base_of_support(
    data_parent_empty:bpy.types.Object,
    ground_contact_point_names: list,
    base_of_support: bpy.types.Object,
    z_threshold: float,
    com_vertical_projection: bpy.types.Object,
) -> None:

    scene = bpy.context.scene

    # Get relevant objects
    contact_point_objects = []
    # com_projection_mesh = None
    for point_name in ground_contact_point_names:
        for child in data_parent_empty.children_recursive:
            if point_name in child.name:
                contact_point_objects.append(child)
                break

    # Set switch node index based on Blender version (to void an error)
    switch_node_index = 1 if bpy.app.version < (4, 1, 0) else 0

    # Get current frame to restore it at the end
    current_frame = scene.frame_current

    for frame in range(scene.frame_start, scene.frame_end):

        scene.frame_set(frame)

        # Variable to save if the base of support is visible or not (at least one point is below the threshold)
        base_of_support_visible = False
        for contact_point_object in contact_point_objects:

            # Get the z coordinate of the point
            contact_point_z = contact_point_object.matrix_world.translation.z

            bos_nodes_group = bpy.data.node_groups["Geometry Nodes_" + base_of_support.name]

            # If the z coordinate is less than the threshold, update the point circle mesh node location and enable it
            if contact_point_z < z_threshold:

                base_of_support_visible = True                

                # Update the x and y coordinates of the offset of the Set Position node
                bos_nodes_group.nodes["Set Position_" + contact_point_object.name].inputs[3].default_value[0] = contact_point_object.matrix_world.translation.x
                bos_nodes_group.nodes["Set Position_" + contact_point_object.name].inputs[3].default_value[1] = contact_point_object.matrix_world.translation.y

                # Insert a keyframe to the corresponding point
                bos_nodes_group.nodes["Set Position_" + contact_point_object.name].inputs[3].keyframe_insert(data_path='default_value', frame=frame)

                # Enable the Mesh Switch node
                bos_nodes_group.nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].default_value = True

                # Insert a keyframe to the corresponding point
                bos_nodes_group.nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)

            else:

                # Disable the Circle Mesh node
                bos_nodes_group.nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].default_value = False

                # Insert a keyframe to the corresponding point
                bos_nodes_group.nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)

        # Check if the COM Vertical Projection is intersecting with the base of support to change its material accordingly
        com_vert_projection_nodes_group = bpy.data.node_groups["Geometry Nodes_" + com_vertical_projection.name]

        if base_of_support_visible:

            # Enable the BOS Visible Switch
            com_vert_projection_nodes_group.nodes["BOS Visible Switch"].inputs[switch_node_index].default_value = True

            # Get the location of the COM Vertical Projection
            com_vertical_projection_location = com_vertical_projection.matrix_world.translation
            # Get the evaluated object with applied Geometry Nodes
            evaluated_object = base_of_support.evaluated_get(bpy.context.evaluated_depsgraph_get())

            # Get the a list of the coordinates of the points comforming the base of support
            BOS_points = [v.co for v in evaluated_object.data.vertices]
            if len(BOS_points) < 3:
                continue
            # Create the polygon object as a list of 2D points tuples from the x and y coordinates
            points = np.array([(v[0], v[1]) for v in BOS_points])

            # Create a convex hull from the list of 2D points
            hull = convex_hull(points)

            # Get the location of the COM Vertical Projection
            com_vertical_projection_location = (
                com_vertical_projection.matrix_world.translation[0],
                com_vertical_projection.matrix_world.translation[1]
            )

            # Check if the COM Vertical Projection is intersecting with the base of support
            if is_point_inside_polygon(com_vertical_projection_location, hull):
                # Change the material of the COM Vertical Projection to In Base of Support
                com_vert_projection_nodes_group.nodes["In-Out BOS Switch"].inputs[switch_node_index].default_value = True
            else:
                # Change the material of the COM Vertical Projection to Out Base of Support
                com_vert_projection_nodes_group.nodes["In-Out BOS Switch"].inputs[switch_node_index].default_value = False

        else:
            # Disable the BOS Visible Switch
            com_vert_projection_nodes_group.nodes["BOS Visible Switch"].inputs[switch_node_index].default_value = False

        # Insert a keyframe to the COM Vertical Projection switch nodes
        com_vert_projection_nodes_group.nodes["In-Out BOS Switch"].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)
        com_vert_projection_nodes_group.nodes["BOS Visible Switch"].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)

    # Restore the current frame
    scene.frame_current = current_frame


def is_point_inside_polygon(point, polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if point[1] > min(p1y, p2y):
            if point[1] <= max(p1y, p2y):
                if point[0] <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (point[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or point[0] <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def convex_hull(points):
    # Sort the points lexographically (first by x-coordinate, then by y-coordinate)
    points = sorted(points, key=lambda point: (point[0], point[1]))
    
    # Build the lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and not is_ccw(lower[-2], lower[-1], p):
            lower.pop()
        lower.append(p)
    
    # Build the upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and not is_ccw(upper[-2], upper[-1], p):
            upper.pop()
        upper.append(p)
    
    # Concatenate the lower and upper hulls, removing the last point of
    # each half because it's repeated at the beginning of the other half
    return lower[:-1] + upper[:-1]

def is_ccw(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0
