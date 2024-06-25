import math as m
import time

from bpy.types import Operator


class SKELLY_BLENDER_OT_reduce_bone_length_dispersion(Operator):
    bl_idname = 'skelly_blender._reduce_bone_length_dispersion'
    bl_label = 'Freemocap Adapter - Reduce Bone Length Dispersion'
    bl_description = 'Reduce the bone length dispersion by moving the tail empty and its children along the bone projection so the bone new length is within the interval'
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        scene = context.scene
        skelly_blender_tool = scene.skelly_blender_properties

        recording_path = skelly_blender_tool.recording_path_str
        if recording_path == "":
            print("No recording path specified")
            return {'CANCELLED'}
        handler = FreemocapDataHandler.load_from_recording_path(recording_path=recording_path)

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
