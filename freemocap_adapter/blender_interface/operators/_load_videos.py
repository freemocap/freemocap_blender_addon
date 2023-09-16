import logging

import bpy

logger = logging.getLogger(__name__)

from freemocap_adapter.core_functions.freemocap_data_operations.load_videos import load_videos


class FMC_ADAPTER_load_videos(bpy.types.Operator):
    bl_idname = 'fmc_adapter._load_videos'
    bl_label = "Load Videos as planes"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        logger.info("Loading videos as planes...")
        scene = context.scene
        fmc_adapter_tool = scene.fmc_adapter_tool

        try:
            load_videos(recording_path=fmc_adapter_tool.recording_path)
        except Exception as e:
            logger.error(e)
            logger.exception(e)
            return {'CANCELLED'}
        return {'FINISHED'}