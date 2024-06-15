import traceback
from pathlib import Path

import bpy

from freemocap_blender_addon.pipelines.blender_skeleton_builder_pipeline import BlenderSkeletonBuilderPipeline


class FMC_ADAPTER_run_all(bpy.types.Operator):
    bl_idname = 'fmc_adapter._run_all'
    bl_label = "Run All"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        fmc_adapter_tool = context.scene.fmc_adapter_properties
        recording_path = fmc_adapter_tool.recording_path
        if recording_path == "":
            print("No recording path specified")
            return {'CANCELLED'}
        try:
            bpy.ops.object.empty_add(type="ARROWS")
            empty_object = bpy.context.editable_objects[-1]
            empty_object.name = Path(recording_path).stem
            fmc_adapter_tool.data_parent_empty = empty_object
            pipeline = BlenderSkeletonBuilderPipeline(recording_path_str=recording_path)
            pipeline.run()
            
        except Exception as e:
            print(traceback.format_exc())
            return {'CANCELLED'}
        return {'FINISHED'}


