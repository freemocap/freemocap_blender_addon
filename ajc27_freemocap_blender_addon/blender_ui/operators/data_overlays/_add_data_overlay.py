import bpy

from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_manager import OverlayManager
from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlays.time_series_plot import TimeSeriesOverlay


class FREEMOCAP_OT_add_data_overlay(bpy.types.Operator):
    bl_idname = 'freemocap._add_data_overlay'
    bl_label = 'Add Data Overlay'
    bl_description = "Add Data Overlay"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Adding Data Overlay.......")
        ui_props = context.scene.freemocap_ui_properties
        core_props = context.scene.freemocap_properties
        overlay_manager = OverlayManager()
        overlay_manager.remove("Elbow Angle")
        angle_overlay = TimeSeriesOverlay(
            "Elbow Angle",
            # data_path="C:/Users/andre/freemocap_data/recording_sessions/freemocap_test_data/output_data/joint_angles.npy",
            data_path=core_props.recording_path + "output_data\\joint_angles.npy",
            column_index=9,  # Which column to use from the numpy file
            window_size=100,  # Number of frames to show
            pos=(50, 50),     # Screen position
            size=(300, 200)   # Overlay size
        )
        overlay_manager.add(angle_overlay)
        overlay_manager.enable()

        return {'FINISHED'}
