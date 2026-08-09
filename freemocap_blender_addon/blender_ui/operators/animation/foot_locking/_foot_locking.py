import bpy
import numpy as np
import math

from freemocap_blender_addon.data_models.mediapipe_names.mediapipe_heirarchy import get_mediapipe_hierarchy

from freemocap_blender_addon.blender_ui.operators.animation.foot_locking.methods.foot_group_movement import run_foot_group_movement

MEDIAPIPE_HIERARCHY = get_mediapipe_hierarchy()

class FREEMOCAP_OT_foot_locking(bpy.types.Operator):
    bl_idname = 'freemocap._foot_locking'
    bl_label = 'Foot Locking'
    bl_description = "Foot Locking"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):

        props = context.scene.freemocap_ui_properties.foot_locking_properties

        if props.foot_locking_method == 'foot_group_movement':
            run_foot_group_movement(context)

        return {'FINISHED'}
