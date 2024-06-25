import traceback
from pathlib import Path

import bpy

from skelly_blender.core.needs_bpy.empties.create_parent_empty import create_parent_empty
from skelly_blender.pipelines.blender_skeleton_pipeline import BlenderSkeletonBuilderPipeline


class SKELLY_BLENDER_run_all(bpy.types.Operator):
    bl_idname = 'skelly_blender._run_all'
    bl_label = "Run All"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        skelly_blender_tool = context.scene.skelly_blender_properties
        recording_path = skelly_blender_tool.recording_path
        if recording_path == "":
            print("No recording path specified")
            return {'CANCELLED'}
        try:
            recording_name = Path(recording_path).name
            parent_emtpy = create_parent_empty(name=recording_name)
            pipeline = BlenderSkeletonBuilderPipeline(recording_path_str=recording_path,
                                                      parent_empty=parent_emtpy)
            pipeline.run(show_stages=skelly_blender_tool.show_stages)

        except Exception as e:
            print(traceback.format_exc())
            return {'CANCELLED'}
        return {'FINISHED'}
