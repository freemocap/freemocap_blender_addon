import os

import addon_utils
import bpy
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import export_profiles, render_background


def add_render_background(scene: bpy.types.Scene = None,
                          export_profile: str = None, ):
    # Set the path to the PNG image
    image_path = os.path.dirname(os.path.realpath(__file__)) + export_profiles[export_profile]['background_path']
    print(image_path)

    # check if the addon is enabled
    loaded_default, loaded_state = addon_utils.check('io_import_images_as_planes')
    if not loaded_state:
        # enable the addon
        addon_utils.enable('io_import_images_as_planes')

    # Import the image as plane
    bpy.ops.import_image.to_plane(files=[{"name": str(image_path)}],
                                  size_mode='ABSOLUTE',
                                  height=render_background['height'],
                                  )

    # Change the location of the plane ot be behind the video_0 element
    bpy.data.objects['charuco_board'].location = (bpy.data.objects['charuco_board'].location[0],
                                                  bpy.data.objects['video_0'].location[1] + render_background[
                                                      'y_axis_offset'],
                                                  bpy.data.objects['Front_Camera'].location[2])
