import bpy

class FREEMOCAP_OT_clear_all_motion_paths(bpy.types.Operator):
    bl_idname = 'freemocap._clear_all_motion_paths'
    bl_label = 'Clear All Motion Paths'
    bl_description = "Clear All Motion Paths"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        print("Clearing All Motion Paths.......")
        ui_props = context.scene.freemocap_ui_properties

        data_parent_empty = bpy.data.objects[context.scene.freemocap_properties.scope_data_parent]

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select all children of the data parent empty
        for child in data_parent_empty.children_recursive:
            child.select_set(True)

        bpy.ops.object.paths_clear(only_selected=True)

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}
