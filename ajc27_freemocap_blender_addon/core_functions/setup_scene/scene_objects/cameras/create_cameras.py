import math

import bpy
import mathutils


def calculate_extreme_points(scene: bpy.types.Scene) -> tuple:
    highest_point = mathutils.Vector([float('-inf')] * 3)
    lowest_point = mathutils.Vector([float('inf')] * 3)
    leftmost_point = mathutils.Vector([float('inf')] * 3)
    rightmost_point = mathutils.Vector([float('-inf')] * 3)

    for frame in range(scene.frame_start, scene.frame_end):
        scene.frame_set(frame)

        for obj in scene.objects:
            if obj.type == 'EMPTY' and obj.name not in ['freemocap_origin_axes', 'world_origin', 'center_of_mass_data_parent', 'head']:
                translation = obj.matrix_world.translation

                highest_point = max(highest_point, translation, key=lambda v: v[2])
                lowest_point = min(lowest_point, translation, key=lambda v: v[2])
                leftmost_point = min(leftmost_point, translation, key=lambda v: v[0])
                rightmost_point = max(rightmost_point, translation, key=lambda v: v[0])

    return highest_point, lowest_point, leftmost_point, rightmost_point

def calculate_camera_distance(
        scene: bpy.types.Scene,
        camera_horizontal_fov: float,
        camera_vertical_fov: float,
        angle_margin: float
) -> float:
    highest_point, lowest_point, leftmost_point, rightmost_point = calculate_extreme_points(scene)

    camera_y_axis_distance_leftmost = leftmost_point[1] - abs(leftmost_point[0]) / math.atan(
        math.radians(camera_horizontal_fov * angle_margin / 2))
    camera_y_axis_distance_rightmost = rightmost_point[1] - abs(rightmost_point[0]) / math.atan(
        math.radians(camera_horizontal_fov * angle_margin / 2))
    camera_y_axis_distance_highest = highest_point[1] - ((highest_point[2] - lowest_point[2]) / 2) / math.atan(
        math.radians(camera_vertical_fov * angle_margin / 2))
    camera_y_axis_distance_lowest = lowest_point[1] - ((highest_point[2] - lowest_point[2]) / 2) / math.atan(
        math.radians(camera_vertical_fov * angle_margin / 2))

    camera_y_axis_distance = min(camera_y_axis_distance_leftmost, camera_y_axis_distance_rightmost,
                                 camera_y_axis_distance_highest, camera_y_axis_distance_lowest)

    return camera_y_axis_distance

def create_cameras(
        scene: bpy.types.Scene,
        export_profile: str = 'debug'
) -> list:
    from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import export_profiles, lens_FOVs
    
    print(f"Creating cameras for export profile: {export_profile}")
    if export_profiles[export_profile]['resolution_x'] / export_profiles[export_profile]['resolution_y'] >= 1:
        camera_horizontal_fov = lens_FOVs['50mm']['horizontal_fov']
        camera_vertical_fov = lens_FOVs['50mm']['vertical_fov']
    else:
        camera_horizontal_fov = lens_FOVs['50mm']['vertical_fov']
        camera_vertical_fov = lens_FOVs['50mm']['horizontal_fov']

    angle_margin = 0.9
    cameras_positions = []

    camera_data = bpy.data.cameras.new(name="Front_Camera")
    camera = bpy.data.objects.new(name="Front_Camera", object_data=camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    if len(scene.objects) > 1:
        highest_point, lowest_point, leftmost_point, rightmost_point = calculate_extreme_points(scene)
        camera_x_position = 0
        camera_y_position = calculate_camera_distance(scene, camera_horizontal_fov, camera_vertical_fov, angle_margin)
        camera_z_position = highest_point[2] - (highest_point[2] - lowest_point[2]) / 2
    else:
        camera_y_position = 0
        camera_x_position = 0
        camera_z_position = 0

    print("Creating camera at: ", camera_x_position, camera_y_position, camera_z_position)
    camera.location = (camera_x_position, camera_y_position, camera_z_position)
    camera.rotation_euler = (math.radians(90), 0, 0)

    cameras_positions.append(camera.location)

    return cameras_positions

if __name__ == "__main__":
    create_cameras(bpy.context.scene, export_profile='debug')