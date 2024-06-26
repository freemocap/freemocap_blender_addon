import logging
import math as m
import time

from bpy.types import Operator
from freemocap_blender_addon.core_functions.empties.reorient_empties import reorient_empties
from freemocap_blender_addon.core_functions.rig.add_rig import generate_rig

from old.freemocap_blender_addon.freemocap_data_handler.operations.freemocap_empties_from_parent_object import \
    freemocap_empties_from_parent_object
from ...ui.operators._add_body_mesh import REORIENT_EMPTIES_EXECUTED

logger = logging.getLogger(__name__)


class SKELLY_BLENDER_OT_add_rig(Operator):
    bl_idname = 'skelly_blender._add_rig'
    bl_label = 'Freemocap Adapter - Add Rig'
    bl_description = 'Add a Rig to the capture empties. The method sets the rig rest pose as a TPose'
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print(f"Executing {__name__}...")
        scene = context.scene
        skelly_blender_tool = scene.skelly_blender_properties
        parent_empty = skelly_blender_tool.data_parent_empty
        empties = freemocap_empties_from_parent_object(parent_empty)
        # Get start time
        start = time.time()

        # Reset the scene frame to the start
        current_frame = scene.frame_current
        scene.frame_set(scene.frame_start)

        if not REORIENT_EMPTIES_EXECUTED:
            print('Executing First Adjust Empties...')

            # Execute Adjust Empties first
            reorient_empties(z_align_ref_empty=skelly_blender_tool.vertical_align_reference,
                             z_align_angle_offset=skelly_blender_tool.vertical_align_angle_offset,
                             ground_ref_empty=skelly_blender_tool.ground_align_reference,
                             z_translation_offset=skelly_blender_tool.vertical_align_position_offset,
                             empties=empties,
                             parent_object=parent_empty,
                             correct_fingers_empties=skelly_blender_tool.correct_fingers_empties,
                             )

        print('Executing Add Rig...')

        rig = generate_rig(empties=empties,
                           bone_length_method=skelly_blender_tool.bone_length_method,
                           keep_symmetry=skelly_blender_tool.keep_symmetry,
                           add_fingers_constraints=skelly_blender_tool.add_fingers_constraints,
                           use_limit_rotation=skelly_blender_tool.use_limit_rotation)

        # Get end time and print execution time
        end = time.time()
        print('Finished. Execution time (s): ' + str(m.trunc((end - start) * 1000) / 1000))
        scene.frame_set(current_frame)  # set the frame back to what it was before we started
        return {'FINISHED'}
