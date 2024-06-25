from pathlib import Path

import bpy
from freemocap_blender_addon.core_functions.empties.creation.create_freemocap_empties import create_freemocap_empties
from freemocap_blender_addon.core_functions.setup_scene.make_parent_empties import create_parent_empty
from freemocap_blender_addon.core_functions.setup_scene.set_start_end_frame import set_start_end_frame
from freemocap_blender_addon.freemocap_data_handler.handler import FreemocapDataHandler


class SKELLY_BLENDER_load_freemocap_data(bpy.types.Operator):  # , bpy_extras.io_utils.ImportHelper):
    bl_idname = 'skelly_blender._freemocap_data_operations'
    bl_label = "Load FreeMoCap Data"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        try:
            scene = context.scene
            skelly_blender_tool = scene.skelly_blender_properties

            recording_path = skelly_blender_tool.recording_path_str
            if recording_path == "":
                print("No recording path specified")
                return {'CANCELLED'}

            recording_name = Path(recording_path).stem
            origin_name = f"{recording_name}_origin"
            freemocap_origin_axes = create_parent_empty(name=origin_name)
            skelly_blender_tool.data_parent_empty = freemocap_origin_axes

            print("Loading freemocap data....")
            handler = FreemocapDataHandler.from_recording_path(recording_path=recording_path)
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
