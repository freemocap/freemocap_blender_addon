import bpy
from math import atan, sqrt

def place_lights(
    scene: bpy.types.Scene=None,
    cameras_positions: list=None
) -> None:

    # Lights vertical offset in Blender units
    lights_vertical_offset = 2

    # Create the light
    light_data = bpy.data.lights.new(name="Front_Light", type='SPOT')
    light = bpy.data.objects.new(name="Front_Light", object_data=light_data)
    scene.collection.objects.link(light)

    # Set the strength of the light
    light.data.energy = (
        200
        * sqrt(lights_vertical_offset**2 + cameras_positions[0][1]**2)
    )

    # Set the location of the light
    light.location = (cameras_positions[0][0],
                      cameras_positions[0][1],
                      cameras_positions[0][2] + lights_vertical_offset
    )

    # Set the rotation of the light so it points to the point lights_vertical_offset
    light.rotation_euler = (
        atan(abs(cameras_positions[0][1]) / lights_vertical_offset),
        0,
        0
    )

    return
