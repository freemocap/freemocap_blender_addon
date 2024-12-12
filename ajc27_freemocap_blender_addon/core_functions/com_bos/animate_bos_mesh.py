import bpy

from ajc27_freemocap_blender_addon.core_functions.com_bos.add_com_vertical_projection import COM_PROJECTION_MESH_NAME

import numpy as np

def animate_base_of_support(data_parent_empty:bpy.types.Object,
                            ground_contact_point_names: list,
                            base_of_support: bpy.types.Object,
                            z_threshold: float):
    try:
        from shapely.geometry import Point, Polygon
        from scipy.spatial import ConvexHull

    except ImportError:
        print("shapely module is not installed. Please install `shapely` and `scipy` to visualize the BOS mesh.")
        return


    scene = bpy.context.scene

    #get relevant objst
    contact_point_objects = []
    com_projection_mesh = None
    for point_name in ground_contact_point_names:
        for child in data_parent_empty.children_recursive:
            if point_name in child.name:
                contact_point_objects.append(child)
                break

    for child in data_parent_empty.children_recursive:
        if COM_PROJECTION_MESH_NAME in child.name:
            com_projection_mesh = child
            break
    if com_projection_mesh is None:
        raise ValueError("COM Projection Mesh not found")

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

            # If the z coordinate is less than the threshold, update the point circle mesh node location and enable it
            if contact_point_z < z_threshold:

                base_of_support_visible = True

                # Update the x and y coordinates of the offset of the Set Position node
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Set Position_" + contact_point_object.name].inputs[3].default_value[0] = contact_point_object.matrix_world.translation.x
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Set Position_" + contact_point_object.name].inputs[3].default_value[1] = contact_point_object.matrix_world.translation.y

                # Insert a keyframe to the corresponding point
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Set Position_" + contact_point_object.name].inputs[3].keyframe_insert(data_path='default_value', frame=frame)

                # Enable the Mesh Switch node
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].default_value = True

                # Insert a keyframe to the corresponding point
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)

            else:

                # Disable the Circle Mesh node
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].default_value = False

                # Insert a keyframe to the corresponding point
                bpy.data.node_groups["Geometry Nodes_base_of_support"].nodes["Switch_" + contact_point_object.name].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)

        # Check if the COM Vertical Projection is intersecting with the base of support to change its material accordingly
        if base_of_support_visible:

            # Enable the BOS Visible Switch
            bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["BOS Visible Switch"].inputs[switch_node_index].default_value = True

            # Get the location of the COM Vertical Projection
            com_vertical_projection_location = com_projection_mesh.matrix_world.translation
            # Get the evaluated object with applied Geometry Nodes
            evaluated_object = base_of_support.evaluated_get(bpy.context.evaluated_depsgraph_get())

            # Get the a list of the coordinates of the points comforming the base of support
            BOS_points = [v.co for v in evaluated_object.data.vertices]
            if len(BOS_points) < 3:
                continue
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
                bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["In-Out BOS Switch"].inputs[switch_node_index].default_value = True
            else:
                # Change the material of the COM Vertical Projection to Out Base of Support
                bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["In-Out BOS Switch"].inputs[switch_node_index].default_value = False

        else:
            # Disable the BOS Visible Switch
            bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["BOS Visible Switch"].inputs[switch_node_index].default_value = False

        # Insert a keyframe to the COM Vertical Projection switch nodes
        bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["In-Out BOS Switch"].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)
        bpy.data.node_groups["Geometry Nodes_COM_Vertical_Projection"].nodes["BOS Visible Switch"].inputs[switch_node_index].keyframe_insert(data_path='default_value', frame=frame)

    # Restore the current frame
    scene.frame_current = current_frame


