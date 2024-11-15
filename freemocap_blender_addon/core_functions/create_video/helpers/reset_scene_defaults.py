import bpy

def reset_scene_defaults() -> None:

    # Enable all elements in render
    for obj in bpy.data.objects:
        obj.hide_render = False

    # Hide the background if present
    if "background" in bpy.data.objects:
        bpy.data.objects["background"].hide_set(True)

    return
