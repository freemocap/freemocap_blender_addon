import shutil

import bpy


def set_bpy_binary_path():
    # https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html#usage
    blender_bin = shutil.which("blender")
    if blender_bin:
        print("Setting Blender binary path to:", blender_bin)
        bpy.app.binary_path = blender_bin
    else:
        print("Unable to find blender!")


if __name__ == "__main__":
    set_bpy_binary_path()