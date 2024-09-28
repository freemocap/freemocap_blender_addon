import logging

import bpy

logger = logging.getLogger(__name__)


class VIEW3D_PT_freemocap(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "💀FreeMoCap"
    bl_label = "💀FreeMoCap"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        fmc_adapter_tool = scene.fmc_adapter_properties

        self._clear_scene_button(layout)

        self._run_all_panel(fmc_adapter_tool, layout)

        self._save_data_to_disk_panel(fmc_adapter_tool, layout)


    def _clear_scene_button(self, layout):
        # Clear scene button
        clear_scene_box = layout.box()
        clear_scene_box.operator('fmc_adapter._clear_scene', text='Clear Scene')

    def _run_all_panel(self, fmc_adapter_tool, layout):
        box = layout.box()
        row = box.row()
        row.label(text="FreeMoCap Recording:")
        row.prop(fmc_adapter_tool, "recording_path", text="")
        box.operator('fmc_adapter._run_all', text='RUN ALL')

    def _save_data_to_disk_panel(self, fmc_adapter_tool, layout):
        box = layout.box()
        box.prop(fmc_adapter_tool,
                 "data_parent_empty",
                 text="Data Parent Empty")
        # box.operator('fmc_adapter._save_data_to_disk', text='Save Data to Disk')

    def _fbx_export_panel(self, layout):
        # FBX Export
        fbx_export_box = layout.box()
        fbx_export_box.operator('fmc_adapter._export_fbx', text='5. Export FBX')

