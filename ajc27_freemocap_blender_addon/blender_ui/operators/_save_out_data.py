import bpy

from ajc27_freemocap_blender_addon.freemocap_data_handler.operations.freemocap_empties_from_parent_object import \
    empties_from_parent_object


class FREEMOCAP_save_data_to_disk(bpy.types.Operator):
    bl_idname = 'freemocap._save_data_to_disk'
    bl_label = "Save Data to Disk"
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
                                        config=config)
            empties = empties_from_parent_object(context.scene.freemocap_properties.data_parent_empty)
            controller.freemocap_data_handler.extract_data_from_empties(empties=empties)
            controller.save_data_to_disk()
        except Exception as e:
            print(f"Failed to run main_controller.load_data() with config:{config}: `{e}`")
            print(e)
            return {'CANCELLED'}
        return {'FINISHED'}
