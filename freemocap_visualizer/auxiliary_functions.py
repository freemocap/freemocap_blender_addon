import bpy
import mathutils

# Function to hide (or unhide) Blender objects
def hide_objects(data_object: bpy.types.Object,
                 hide: bool = True,
                 hide_children_not_parent: bool = False,)->None:

    if hide_children_not_parent:
        for child_object in data_object.children:
            # Hide child object
            child_object.hide_set(hide)
            # Execute the function recursively
            hide_objects(child_object, hide, hide_children_not_parent)
    else:
        data_object.hide_set(hide)

# Function to draw a vector for debbuging purposes
def draw_vector(origin, angle, name):
    
    bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=origin, rotation=mathutils.Vector([0,0,1]).rotation_difference(angle).to_euler(), scale=(0.002, 0.002, 0.002))
    bpy.data.objects["Empty"].name = name

    bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(origin+angle*0.5), scale=(0.001, 0.001, 0.001))
    bpy.data.objects["Empty"].scale = (0.01, 0.01, 0.01)
    bpy.data.objects["Empty"].name = 'Sphere_' + name

    return

# Function to check if a point is inside a polygon
def is_point_inside_polygon(x, y, polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n+1):
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

