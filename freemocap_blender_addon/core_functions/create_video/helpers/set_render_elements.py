from typing import List, Any, Dict

import bpy


def set_render_elements(render_elements: Dict[str, Any]):
    def set_hide_render_recursive(obj):
        obj.hide_render = False
        for child in obj.children:
            set_hide_render_recursive(child)

    # Set hide_render equal to True for all the objects
    for obj in bpy.data.objects:
        if obj.name not in ['Front_Camera', 'Front_Light']:
            obj.hide_render = True

    # Set hide_render equal to False for the render elements
    for obj in bpy.data.objects:
        if any(element in obj.name for element in render_elements):
            print("Setting Render Hide: " + obj.name)
            set_hide_render_recursive(obj)

