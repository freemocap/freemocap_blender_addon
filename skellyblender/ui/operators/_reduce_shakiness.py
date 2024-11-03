import math as m
import time

from bpy.types import Operator
from freemocap_blender_addon.core_functions.empties import reduce_shakiness


class SKELLY_BLENDER_OT_reduce_shakiness(Operator):
    bl_idname = 'skelly_blender._reduce_shakiness'
    bl_label = 'Freemocap Adapter - Reduce Shakiness'
    bl_description = 'Reduce the shakiness of the capture empties by restricting their acceleration to a defined threshold'
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        skelly_blender_tool = scene.skelly_blender_properties

        # Get start time
        start = time.time()
        print('Executing Reduce Shakiness...')

        reduce_shakiness(recording_fps=skelly_blender_tool.recording_fps)

        # Get end time and print execution time
        end = time.time()
        print('Finished. Execution time (s): ' + str(m.trunc((end - start) * 1000) / 1000))

        return {'FINISHED'}
