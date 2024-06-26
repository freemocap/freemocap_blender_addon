import bpy

from freemocap_blender_addon.core_functions.load_videos.load_videos import load_videos


class SKELLY_BLENDER_load_videos(bpy.types.Operator):
    bl_idname = 'skelly_blender._load_videos'
    bl_label = "Load Videos as planes"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Loading videos as planes...")
        scene = context.scene
        skelly_blender_tool = scene.skelly_blender_properties

        try:
            load_videos(recording_path=skelly_blender_tool.recording_path_str)
        except Exception as e:
            print(e)
            print(e)
            return {'CANCELLED'}
        return {'FINISHED'}
