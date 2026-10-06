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
            props = context.scene.freemocap_properties
            if props.import_route != 'legacy_npy':
                from ...core_functions.parquet_import import load_parquet
                load_parquet(bpy.path.abspath(recording_path), route=props.import_route,
                             trajectory_channel=props.trajectory_channel if props.import_route == 'parquet_constraints' else 'LANDMARKS_3D',
                             run_id=None if props.parquet_run_id == -1 else props.parquet_run_id,
                             sensor_group=props.parquet_sensor_group.strip() or None)
                self.report({'INFO'}, 'Loaded Blender skeleton; save the scene to retain it')
                return {'FINISHED'}
            print(f"Executing `main_controller.load_data() with config:{config}")
            controller = MainController(recording_path=recording_path,
                                        blend_file_path=str(Path(recording_path) / (Path(recording_path).stem + ".blend")),
                                        config=config)
            controller.load_data()
        except Exception as e:
            self.report({'ERROR'}, str(e))
            print(f"Failed to run main_controller.load_data() with config:{config}: `{e}`")
            print(traceback.format_exc())
            return {'CANCELLED'}
        return {'FINISHED'}


