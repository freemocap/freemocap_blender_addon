import bpy

def create_parent_empty(name: str,
                        type: str,
                        display_scale: float,
                        parent_object: bpy.types.Object = None):
    print("Creating freemocap parent empty...")
    bpy.ops.object.empty_add(type=type)
    parent_empty = bpy.context.active_object
    parent_empty.empty_display_size = display_scale
    parent_empty.name = name
 

    if parent_object is not None:
        print(f"Setting parent of {parent_empty.name} to {parent_object.name}")
        parent_empty.parent = parent_object


    return parent_empty
