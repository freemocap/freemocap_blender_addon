from math import sqrt
from typing import Dict

import bpy


def create_lights(
        scene: bpy.types.Scene = None,
        camera_objects_by_key: Dict[str, bpy.types.Object] = None,
) -> None:
    #  Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Create a nested collection to store the lights
    scene_collection = bpy.data.collections.new('Lights')
    scene.collection.children.link(scene_collection)

    # Delete the current lights
    for obj in scene.objects:
        if obj.type == 'LIGHT':
            obj.select_set(True)
            bpy.ops.object.delete()

    # Delete the current lights
    for obj in scene.objects:
        if obj.type == 'LIGHT':
            obj.select_set(True)
            bpy.ops.object.delete()

    # For each camera in the scene create a light
    for camera_key, camera_object in camera_objects_by_key.items():
        camera_position = camera_object.matrix_world.translation

        # Create the light
        light_data = bpy.data.lights.new(name=camera_key + "_Light", type='SPOT')
        light = bpy.data.objects.new(name=camera_key + "_Light", object_data=light_data)
        # Add the light to the nested collection
        scene_collection.objects.link(light)

        # Set the strength of the light based on the distance to (0, 0, 0)
        light.data.energy = (
                200
                * sqrt(sum([(coord) ** 2 for coord in camera_position]))
        )

        # Set the location and rotation of the light
        light.location = (camera_position.x, camera_position.y, camera_position.z)
        light.rotation_euler = camera_object.rotation_euler

        # Add a copy transform constraint to the light
        constraint = light.constraints.new(type='COPY_TRANSFORMS')
        constraint.target = camera_object
