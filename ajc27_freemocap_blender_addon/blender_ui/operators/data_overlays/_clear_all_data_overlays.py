import bpy

from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_manager import OverlayManager

class FREEMOCAP_OT_clear_all_data_overlays(bpy.types.Operator):
    bl_idname = 'freemocap._clear_all_data_overlays'
    bl_label = 'Clear All Data Overlays'
    bl_description = "Clear All Data Overlays"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Clearing All Data Overlays.......")
        overlay_manager = context.scene.freemocap_overlay_manager
        overlay_manager.remove_all()
        overlay_manager.disable()
        # Force a redraw to update the viewport
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}