import bpy

from ajc27_freemocap_blender_addon.core_functions.load_videos.load_videos import load_videos


class FMC_ADAPTER_load_videos(bpy.types.Operator):
    bl_idname = 'fmc_adapter._load_videos'
    bl_label = "Load Videos as planes"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Loading videos as planes...")
        scene = context.scene
        fmc_adapter_tool = scene.fmc_adapter_properties

        try:
            load_videos(recording_path=fmc_adapter_tool.recording_path)
        except Exception as e:
            print(e)
            print(e)
            return {'CANCELLED'}
        return {'FINISHED'}
