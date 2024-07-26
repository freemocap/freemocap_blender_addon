import math as m
import time

from ajc27_freemocap_blender_addon.core_functions.empties import reduce_shakiness
from bpy.types import Operator


class FMC_ADAPTER_OT_reduce_shakiness(Operator):
    bl_idname = 'fmc_adapter._reduce_shakiness'
    bl_label = 'Freemocap Adapter - Reduce Shakiness'
    bl_description = 'Reduce the shakiness of the capture empties by restricting their acceleration to a defined threshold'
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        fmc_adapter_tool = scene.fmc_adapter_properties

        # Get start time
        start = time.time()
        print('Executing Reduce Shakiness...')

        reduce_shakiness(recording_fps=fmc_adapter_tool.recording_fps)

        # Get end time and print execution time
        end = time.time()
        print('Finished. Execution time (s): ' + str(m.trunc((end - start) * 1000) / 1000))

        return {'FINISHED'}
