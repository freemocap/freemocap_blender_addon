import bpy
import re
from mathutils import Vector
import math as m

from ajc27_freemocap_blender_addon.blender_ui.ui_utilities.common_bone_names import COMMON_BONE_NAMES

# Function to draw a vector for debbuging purposes
def draw_vector(origin, angle, name):
    bpy.ops.object.empty_add(
        type='SINGLE_ARROW', align='WORLD', location=origin,
        rotation=Vector([0, 0, 1]).rotation_difference(angle).to_euler(),
        scale=(0.002, 0.002, 0.002))
    bpy.data.objects["Empty"].name = name

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


# Function to parent meshes (create parent if it doesn't exist)
def parent_meshes(
    data_parent_empty: bpy.types.Object,
    parent: str,
    meshes: dict
) -> None:

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get or create the parent object
    try:
        parent_object = bpy.data.objects[parent]
    except KeyError:
        bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.name = parent
        parent_object = bpy.data.objects[parent]

    # Parent the angle meshes to the empty object
    bpy.ops.object.select_all(action='DESELECT')
    for mesh in meshes:
        meshes[mesh].select_set(True)
    bpy.context.view_layer.objects.active = parent_object
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

    # Parent the joint_angles_parent object to the capture origin empty
    parent_object.parent = data_parent_empty

    # Hide the joint_angles_parent object
    bpy.data.objects[parent].hide_set(True)

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')


# Function to find the matching bone target for the retargeting the animation UI
def find_matching_bone_in_target_list(
    bone_name: str,
    target_list: list
)->str:
    
    # Direct name match
    if bone_name in target_list:
        return bone_name
    
    # Both bones in common bones names list
    for bone_list in COMMON_BONE_NAMES:
        if bone_name in bone_list:
            for target_bone in target_list:
                if target_bone in bone_list:
                    return target_bone
        
    # Case-insensitive match
    lower_name = bone_name.lower()
    for target_bone in target_list:
        if target_bone.lower() == lower_name:
            return target_bone
            
    # Remove prefixes/suffixes
    clean_name = bone_name.replace("Source_", "").replace("_L", "_Left")
    if clean_name in target_list:
        return clean_name
        
    # Regex substitution
    import re
    modified_name = re.sub(r'_([A-Z])', lambda m: m.group(1).upper(), bone_name)
    if modified_name in target_list:
        return modified_name
    
    # No match found
    return ""


def get_edit_bones_adjusted_axes(
    armature: bpy.types.Object,
    x_axis_convention: str,
    y_axis_convention: str,
    z_axis_convention: str,
):
    bones_adjusted_axes = {}

    axes_indexes = {
        "x": 0,
        "y": 1,
        "z": 2,
        "-x": 0,
        "-y": 1,
        "-z": 2
    }

    axes_signs = {
        "x": 1,
        "y": 1,
        "z": 1,
        "-x": -1,
        "-y": -1,
        "-z": -1
    }

    # Set Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    # Select the armature
    armature.select_set(True)

    # Set Edit Mode
    bpy.ops.object.mode_set(mode="EDIT")

    for bone in armature.data.edit_bones:
        adjusted_vectors = [
            Vector([
                axes_signs[x_axis_convention] * bone.x_axis[axes_indexes[x_axis_convention]],
                axes_signs[y_axis_convention] * bone.x_axis[axes_indexes[y_axis_convention]],
                axes_signs[z_axis_convention] * bone.x_axis[axes_indexes[z_axis_convention]]
            ]),
            Vector([
                axes_signs[x_axis_convention] * bone.y_axis[axes_indexes[x_axis_convention]],
                axes_signs[y_axis_convention] * bone.y_axis[axes_indexes[y_axis_convention]],
                axes_signs[z_axis_convention] * bone.y_axis[axes_indexes[z_axis_convention]]
            ]),
            Vector([
                axes_signs[x_axis_convention] * bone.z_axis[axes_indexes[x_axis_convention]],
                axes_signs[y_axis_convention] * bone.z_axis[axes_indexes[y_axis_convention]],
                axes_signs[z_axis_convention] * bone.z_axis[axes_indexes[z_axis_convention]]
            ])
        ]

        bones_adjusted_axes[bone.name] = adjusted_vectors

    # Set Object Mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Deselect all objects
    for object in bpy.data.objects:
        object.select_set(False)

    return bones_adjusted_axes
