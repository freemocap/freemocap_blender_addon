import bpy


class SKELLY_BLENDER_clear_scene(bpy.types.Operator):
    bl_idname = 'skelly_blender._clear_scene'
    bl_label = "Clear Scene"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        self.clear_scene()
        return {'FINISHED'}


    def clear_scene(self):
        ###%% clear the scene - Scorch the earth \o/
        import bpy
        try:
            bpy.ops.object.mode_set(mode="OBJECT")  
        except:
            pass

        print("Clearing scene...")
        bpy.ops.object.hide_view_clear()
        print("Selecting all objects...")
        bpy.ops.object.select_all(action="SELECT")  # select all objects
        print("Deleting all objects from all scenes...")
        bpy.ops.object.delete(use_global=True)  # delete all objects from all scenes
        print("Purging orphans...")
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        print("Scorch the earth \o/")
        bpy.ops.view3d.snap_cursor_to_center()



