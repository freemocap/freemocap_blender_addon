import bpy


class SKELLY_BLENDER_show_names(bpy.types.Operator):
    """Toggle visibility of names for all empty objects, mesh objects, and bones"""
    bl_idname = "object.toggle_name_visibility"
    bl_label = "Toggle Name Visibility"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Toggle visibility for empty objects and mesh objects
        for obj in bpy.data.objects:
            if hasattr(obj, 'show_name'):
                obj.show_name = not obj.show_name

        return {'FINISHED'}