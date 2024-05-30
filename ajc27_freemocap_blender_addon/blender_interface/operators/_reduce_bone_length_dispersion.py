import math as m
import time

from ajc27_freemocap_blender_addon.freemocap_data_handler.operations.enforce_rigid_bodies import enforce_rigid_bodies
from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import load_freemocap_data
from bpy.types import Operator


class FMC_ADAPTER_OT_reduce_bone_length_dispersion(Operator):
    bl_idname = 'fmc_adapter._reduce_bone_length_dispersion'
    bl_label = 'Freemocap Adapter - Reduce Bone Length Dispersion'
    bl_description = 'Reduce the bone length dispersion by moving the tail empty and its children along the bone projection so the bone new length is within the interval'
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_adapter_tool = scene.fmc_adapter_properties

        recording_path = fmc_adapter_tool.recording_path
        if recording_path == "":
            print("No recording path specified")
            return {'CANCELLED'}
        handler = load_freemocap_data(recording_path=recording_path)

        frame_number = scene.frame_current  # grab the current frame number so we can set it back after we're done
        # Get start time
        start = time.time()
        print('Executing Reduce Bone Length Dispersion...')

        enforce_rigid_bones(handler=handler)

        # Get end time and print execution time
        end = time.time()
        print('Finished! Execution time (s): ' + str(m.trunc((end - start) * 1000) / 1000))
        scene.frame_set(frame_number)  # set the frame back to what it was before we started
        return {'FINISHED'}
