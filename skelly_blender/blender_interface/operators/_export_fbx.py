import math as m
import time

from bpy.types import Operator
from freemocap_blender_addon.core_functions.fbx_export.fbx import export_fbx


class SKELLY_BLENDER_OT_export_fbx(Operator):
    bl_idname = 'skelly_blender._export_fbx'
    bl_label = 'Freemocap Adapter - Export FBX'
    bl_description = 'Exports a FBX file containing the rig, the mesh and the baked animation'
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print('Executing Export FBX...')
        scene = context.scene
        skelly_blender_tool = scene.skelly_blender_properties

        recording_path = skelly_blender_tool.recording_path_str
        if recording_path == "":
            print("No recording path specified")
            return {'CANCELLED'}

        # Get start time
        start = time.time()

        # Execute export fbx function
        export_fbx(recording_path=recording_path, )

        # Get end time and print execution time
        end = time.time()
        print('Finished. Execution time (s): ' + str(m.trunc((end - start) * 1000) / 1000))

        return {'FINISHED'}
