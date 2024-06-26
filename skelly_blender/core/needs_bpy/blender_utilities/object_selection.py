import bpy


def deselect_all_objects():
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.data.objects:
        obj.select_set(False)


def set_active_object(bpy_object: bpy.types.Object):
    bpy_object.select_set(True)
    bpy.context.view_layer.objects.active = bpy_object


