import bpy

from skellyblender.core.needs_bpy.blender_type_hints import ParentEmpty


def create_parent_empty(name:str) -> ParentEmpty:
    """
    Create a parent empty object.

    Returns
    -------
    ParentEmpty
        The parent empty object.
    """
    print("Creating parent empty...")
    bpy.ops.object.empty_add(type="ARROWS")
    parent_empty = bpy.context.active_object

    parent_empty.name = name

    return parent_empty