from pathlib import Path

import bpy
from ajc27_freemocap_blender_addon.core_functions.empties import create_freemocap_empties
from ajc27_freemocap_blender_addon.core_functions.setup_scene import create_parent_empty
from ajc27_freemocap_blender_addon.core_functions.setup_scene import set_start_end_frame
from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import load_freemocap_data


class FMC_ADAPTER_load_freemocap_data(bpy.types.Operator):  # , bpy_extras.io_utils.ImportHelper):
    bl_idname = 'fmc_adapter._freemocap_data_operations'
    bl_label = "Load FreeMoCap Data"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        try:
            scene = context.scene
            fmc_adapter_tool = scene.fmc_adapter_properties

            recording_path = fmc_adapter_tool.recording_path
            if recording_path == "":
                print("No recording path specified")
                return {'CANCELLED'}

            recording_name = Path(recording_path).stem
            origin_name = f"{recording_name}_origin"
            freemocap_origin_axes = create_parent_empty(name=origin_name)
            fmc_adapter_tool.data_parent_empty = freemocap_origin_axes

            print("Loading freemocap data....")
            handler = load_freemocap_data(recording_path=recording_path)
            handler.mark_processing_stage("original_from_file")
            set_start_end_frame(number_of_frames=handler.number_of_frames)
        except Exception as e:
            print(e)
            return {'CANCELLED'}

        try:
            print("Creating keyframed empties....")
            empties = create_freemocap_empties(handler=handler,
                                               parent_object=freemocap_origin_axes, )
            print(f"Finished creating keyframed empties: {empties.keys()}")
        except Exception as e:
            print(f"Failed to create keyframed empties: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}
