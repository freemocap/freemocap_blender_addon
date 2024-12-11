from math import radians, atan
from typing import Dict, Any

import bpy
from mathutils import Vector


def create_cameras_objects(
        scene: bpy.types.Scene,
        render_camera_configs: Dict[str, Any],
        camera_horizontal_fov: float,
        camera_vertical_fov: float,
) -> Dict[str, bpy.types.Object]:
    # Delete existing cameras
    while bpy.data.cameras:
        bpy.data.cameras.remove(bpy.data.cameras[0])

    # Create a nested collection to store the cameras
    scene_collection = bpy.data.collections.new('Render_Cameras')
    scene.collection.children.link(scene_collection)

    # Set the starting extreme points
    lowest_x = Vector([0, 0, 0])
    highest_x = Vector([0, 0, 0])
    lowest_y = Vector([0, 0, 0])
    highest_y = Vector([0, 0, 0])
    lowest_z = Vector([0, 0, 0])
    highest_z = Vector([0, 0, 0])

    # Find the extreme points
    # TODO - JSM NOTE - Much faster/easier to get these values by analysis of the raw trajecotry data. I think it might already exist in the `FreeMoCap Data Handler` somewhere
    for frame in range(scene.frame_start, scene.frame_end):
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
                if object.matrix_world.translation[0] < lowest_x[0]:
                    lowest_x = object.matrix_world.translation.copy()
                if object.matrix_world.translation[0] > highest_x[0]:
                    highest_x = object.matrix_world.translation.copy()
                if object.matrix_world.translation[1] < lowest_y[1]:
                    lowest_y = object.matrix_world.translation.copy()
                if object.matrix_world.translation[1] > highest_y[1]:
                    highest_y = object.matrix_world.translation.copy()
                if object.matrix_world.translation[2] < lowest_z[2]:
                    lowest_z = object.matrix_world.translation.copy()
                if object.matrix_world.translation[2] > highest_z[2]:
                    highest_z = object.matrix_world.translation.copy()

    # Reset the scene frame to the start
    scene.frame_set(scene.frame_start)

    # Create the cameras of the export profile
    camera_objects_by_key = {}
    for camera_key, camera_config in render_camera_configs.items():
        camera_name = 'Camera_' + camera_key
        # Create the camera
        camera_data = bpy.data.cameras.new(name=camera_name)
        camera_object = bpy.data.objects.new(name=camera_name, object_data=camera_data)
        scene_collection.objects.link(camera_object)

        # Get the camera view margin
        view_margin = camera_config['view_margin']

        # Set the view leftmost, rightmost, lowest and highest points
        # depending on the camera
        if camera_key == 'Front':
            leftmost_point = lowest_x
            rightmost_point = highest_x
            lowest_point = lowest_z
            highest_point = highest_z
        elif camera_key == 'Right':
            leftmost_point = lowest_y
            rightmost_point = highest_y
            lowest_point = lowest_z
            highest_point = highest_z
        elif camera_key == 'Left':
            leftmost_point = highest_y
            rightmost_point = lowest_y
            lowest_point = lowest_z
            highest_point = highest_z
        elif camera_key == 'Back':
            leftmost_point = highest_x
            rightmost_point = lowest_x
            lowest_point = lowest_z
            highest_point = highest_z
        elif camera_key == 'Top':
            leftmost_point = lowest_x
            rightmost_point = highest_x
            lowest_point = lowest_y
            highest_point = highest_y
        elif camera_key == 'Bottom':
            leftmost_point = lowest_x
            rightmost_point = highest_x
            lowest_point = lowest_y
            highest_point = highest_y
        else:
            raise ValueError('Invalid camera name')

        # Camera distances to cover the view extreme points
        camera_distance_leftmost = (
                leftmost_point[1]
                - abs(leftmost_point[0])
                / atan(radians(camera_horizontal_fov * (1 - view_margin) / 2))
        )
        camera_distance_rightmost = (
                rightmost_point[1]
                - abs(rightmost_point[0])
                / atan(radians(camera_horizontal_fov * (1 - view_margin) / 2))
        )
        camera_distance_lowest = (
                lowest_point[1]
                - ((highest_point[2] - lowest_point[2]) / 2)
                / atan(radians(camera_vertical_fov * (1 - view_margin) / 2))
        )
        camera_distance_highest = (
                highest_point[1]
                - ((highest_point[2] - lowest_point[2]) / 2)
                / atan(radians(camera_vertical_fov * (1 - view_margin) / 2))
        )

        # Calculate the final position of the camera
        camera_distance_on_axis = max(
            abs(camera_distance_leftmost),
            abs(camera_distance_rightmost),
            abs(camera_distance_lowest),
            abs(camera_distance_highest),
        )

        #  Set the location and rotation depending on the camera
        if camera_key == 'Front':
            camera_object.location = (
                0,
                -camera_distance_on_axis,
                highest_point[2] - (highest_point[2] - lowest_point[2]) / 2
            )
            camera_object.rotation_euler = (radians(90), 0, 0)
        elif camera_key == 'Right':
            camera_object.location = (
                camera_distance_on_axis,
                0,
                highest_point[2] - (highest_point[2] - lowest_point[2]) / 2
            )
            camera_object.rotation_euler = (radians(90), 0, radians(90))
        elif camera_key == 'Left':
            camera_object.location = (
                -camera_distance_on_axis,
                0,
                highest_point[2] - (highest_point[2] - lowest_point[2]) / 2
            )
            camera_object.rotation_euler = (radians(90), 0, radians(-90))
        elif camera_key == 'Back':
            camera_object.location = (
                0,
                camera_distance_on_axis,
                highest_point[2] - (highest_point[2] - lowest_point[2]) / 2
            )
            camera_object.rotation_euler = (radians(90), 0, radians(180))
        elif camera_key == 'Top':
            camera_object.location = (
                0,
                0,
                camera_distance_on_axis
            )
            camera_object.rotation_euler = (0, 0, 0)

        camera_objects_by_key[camera_key] = camera_object
    return camera_objects_by_key