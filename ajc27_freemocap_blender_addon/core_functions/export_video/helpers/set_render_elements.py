import bpy
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES
)

def set_render_elements(
    export_profile: str='debug',
) -> None:
    
    def set_hide_render_recursive(obj):
        obj.hide_render = False
        for child in obj.children:
            set_hide_render_recursive(child)

    # Set hide_render equal to True for all the objects excepts cameras and lights
    for obj in bpy.data.objects:
        if obj.type not in ['CAMERA', 'LIGHT']:
            obj.hide_render = True

    # Set hide_render equal to False for the render elements
    for obj in bpy.data.objects:
        if any(element in obj.name for element in EXPORT_PROFILES[export_profile]['render_elements']):
            print("Unhiding for render: " + obj.name)
            set_hide_render_recursive(obj)

    return
