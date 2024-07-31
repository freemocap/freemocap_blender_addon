import bpy
from mathutils import Vector
from math import radians, atan
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    LENS_FOVS,
)

def place_cameras(
    scene: bpy.types.Scene=None,
    export_profile: str='debug'
) -> list:
    
    camera_horizontal_fov = LENS_FOVS['50mm']['horizontal_fov']
    camera_vertical_fov = LENS_FOVS['50mm']['vertical_fov']

    # Camera angle margin to show more area than the capture movement
    angle_margin = 0.9

    # List of cameras positions
    cameras_positions = []

    # Create the camera
    camera_data = bpy.data.cameras.new(name="Front_Camera")
    camera = bpy.data.objects.new(name="Front_Camera", object_data=camera_data)
    scene.collection.objects.link(camera)

    # Assign the camera to the scene
    scene.camera = camera

    # Set the starting extreme points
    highest_point = Vector([0, 0, 0])
    lowest_point = Vector([0, 0, 0])
    leftmost_point = Vector([0, 0, 0])
    rightmost_point = Vector([0, 0, 0])

    # Find the extreme points as the highest, lowest, leftmost,
    # and rightmost considering all the frames
    for frame in range (scene.frame_start, scene.frame_end):
        
        scene.frame_set(frame)

        for object in scene.objects:
            if (object.type == 'EMPTY'
                and object.name not in (
                    'freemocap_origin_axes',
                    'world_origin',
                    'center_of_mass_data_parent',
                    'head',
                )
            ):
                if object.matrix_world.translation[2] > highest_point[2]:
                    highest_point = object.matrix_world.translation.copy()
                if object.matrix_world.translation[2] < lowest_point[2]:
                    lowest_point = object.matrix_world.translation.copy()
                if object.matrix_world.translation[0] < leftmost_point[0]:
                    leftmost_point = object.matrix_world.translation.copy()
                if object.matrix_world.translation[0] > rightmost_point[0]:
                    rightmost_point = object.matrix_world.translation.copy()

    # Calculate the position of the camera assuming is centered at 0 on
    # the x axis and pointing towards the y axis and covers the extreme
    # points including a margin

    # Camera distances to just cover the leftmost and rightmost points
    camera_y_axis_distance_leftmost = (
        leftmost_point[1]
        - abs(leftmost_point[0])
        / atan(radians(camera_horizontal_fov * angle_margin / 2))
    )
    camera_y_axis_distance_rightmost = (
        rightmost_point[1]
        - abs(rightmost_point[0])
        / atan(radians(camera_horizontal_fov * angle_margin / 2))
    )

    # Camera distances to just cover the highest and lowest points
    # considering its centered between the two points on the z axis
    camera_y_axis_distance_highest = (
        highest_point[1]
        - ((highest_point[2] - lowest_point[2]) / 2)
        / atan(radians(camera_vertical_fov * angle_margin / 2))
    )
    camera_y_axis_distance_lowest = (
        lowest_point[1]
        - ((highest_point[2] - lowest_point[2]) / 2)
        / atan(radians(camera_vertical_fov * angle_margin / 2))
    )

    # Calculate the final y position of the camera as the minimum distance
    camera_y_axis_distance = min(camera_y_axis_distance_leftmost,
                                 camera_y_axis_distance_rightmost,
                                 camera_y_axis_distance_highest,
                                 camera_y_axis_distance_lowest)

    camera.location = (
        0,
        camera_y_axis_distance,
        highest_point[2] - (highest_point[2] - lowest_point[2]) / 2
    )
    camera.rotation_euler = (radians(90), 0, 0)

    # Add the camera position to the cameras position list
    cameras_positions.append(camera.location)

    return cameras_positions
