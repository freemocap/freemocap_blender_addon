import bpy
import re

def clear_motion_path(
    context: bpy.context,
    data_object_basename: str,
) -> None:

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get reference to the object
    data_parent_empty = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]
    data_object_name = None
    for child in data_parent_empty.children_recursive:
        if re.search(data_object_basename, child.name):
            data_object_name = child.name
            break
    if not data_object_name:
        raise ValueError(f'Object with name {data_object_basename} not found in children of `data_parent_empty`: {data_parent_empty.name}')

    obj = bpy.data.objects[data_object_name]

    # Select the object
    obj.select_set(True)

    # Set the object as active object
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.paths_clear(only_selected=True)

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    return
