import bpy

from freemocap_blender_addon.freemocap_data_handler.operations import \
    freemocap_empties_from_parent_object


class SKELLY_BLENDER_save_data_to_disk(bpy.types.Operator):
    bl_idname = 'skelly_blender._save_data_to_disk'
    bl_label = "Save Data to Disk"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        from freemocap_blender_addon.main_controller import MainController
        from freemocap_blender_addon.pipelines.pipeline_parameters.load_pipeline_config import \
            load_default_parameters_config
        skelly_blender_tool = context.scene.skelly_blender_properties
        recording_path = skelly_blender_tool.recording_path_str
        if recording_path == "":
            print("No recording path specified")
            return {'CANCELLED'}
        config = load_default_parameters_config()
        try:
            print(f"Executing `main_controller.run_all() with config:{config}")
            controller = MainController(recording_path=recording_path,
                                        pipeline_config=config)
            empties = freemocap_empties_from_parent_object(skelly_blender_tool.data_parent_empty)
            controller.freemocap_data_handler.extract_data_from_empties(empties=empties)
            controller.save_data_to_disk()
        except Exception as e:
            print(f"Failed to run main_controller.run_all() with config:{config}: `{e}`")
            print(e)
            return {'CANCELLED'}
        return {'FINISHED'}
