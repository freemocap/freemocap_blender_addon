import bpy


def print_all_blender_objects_in_scene():
    print("Objects in scene:")
    for obj in bpy.data.objects:
        print(obj)
