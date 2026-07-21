import bpy

def reset_scene_defaults() -> None:

    # Enable all elements in render
    for obj in bpy.data.objects:
        obj.hide_render = False

    # Hide the background if present
    background_name = bpy.app.translations.pgettext_data("background")
    if background_name in bpy.data.objects:
        bpy.data.objects[background_name].hide_set(True)

    return
