import traceback
from pathlib import Path

import bpy


class FREEMOCAP_OT_load_data(bpy.types.Operator):
    bl_idname = 'freemocap._load_data'
    bl_label = "Load Data"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        from ...core_functions.main_controller import MainController
        from ...data_models.parameter_models.load_parameters_config import load_default_parameters_config
        recording_path = context.scene.freemocap_properties.recording_path
        if recording_path == "":
            print("No recording path specified")
            return {'CANCELLED'}
        config = load_default_parameters_config()
        try:
            print(f"Executing `main_controller.load_data() with config:{config}")
            controller = MainController(recording_path=recording_path,
                                        blend_file_path=str(Path(recording_path) / (Path(recording_path).stem + ".blend")),
                                        config=config)
            context.scene.freemocap_properties.data_parent_empty = controller.data_parent_empty
            controller.load_data()
        except Exception as e:
            print(f"Failed to run main_controller.load_data() with config:{config}: `{e}`")
            print(traceback.format_exc())
            return {'CANCELLED'}
        return {'FINISHED'}


