import bpy

from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_manager import OverlayManager
from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlays.rom_gauge.rom_gauge import ROMGauge

# TODO: Probably generate the joint angle numpy file as a npz file to include the column names
# and then load the npz file here to get the column names dynamically
# and don't rely on a hardcoded dictionary or a separate csv file

def get_column_names_from_csv(csv_filepath):
    with open(csv_filepath, 'r') as f:
        header_line = f.readline().strip()
    # Split the first line by commas to get the list of names
    column_names = header_line.split(',')
    return column_names

class FREEMOCAP_OT_add_rom_gauge(bpy.types.Operator):
    bl_idname = 'freemocap._add_rom_gauge'
    bl_label = 'Add ROM Gauge Overlay'
    bl_description = "Add ROM Gauge Overlay"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Adding Data Overlay.......")
        ui_props = context.scene.freemocap_ui_properties
        data_overlay_props = ui_props.add_data_overlays_properties
        core_props = context.scene.freemocap_properties
        overlay_manager = context.scene.freemocap_overlay_manager

        # Get the type and name of the parameter to plot
        parameter = data_overlay_props.rom_gauge_parameter
        parameter_type, parameter_name = parameter.split('#')
        # Get the parameter plot title by replacing underscores with spaces
        # and capitalizing each word
        parameter_title = parameter_name.replace('_', ' ').title()

        # Get the recording path, add a \ if not present at the end
        if not core_props.recording_path.endswith('\\'):
            core_props.recording_path += '\\'

        # Get the data path and column index based on the selected parameter
        if parameter_type == 'angle':
            data_path = core_props.recording_path + "output_data\\joint_angles.npy"
            csv_filepath = core_props.recording_path + "output_data\\joint_angles.csv"

            # Get the column names from the CSV file
            try:
                column_names = get_column_names_from_csv(csv_filepath)
            except Exception as e:
                self.report({'ERROR'}, f"Error reading CSV file: {e}")
                return {'CANCELLED'}

            # Get the parameter index from the column names
            if parameter_name in column_names:
                parameter_index = column_names.index(parameter_name)
            else:
                self.report({'ERROR'}, f"Parameter '{parameter_name}' not found in CSV file.")
                return {'CANCELLED'}
            
        # Get the aligned position if not custom
        if data_overlay_props.common_viewport_position != 'CUSTOM':
            position_x, position_y = overlay_manager.get_overlay_aligned_position(
                data_overlay_props.common_viewport_position,
                margin=data_overlay_props.common_overlay_margin
            )
        else:
            position_x = data_overlay_props.common_custom_position_x
            position_y = data_overlay_props.common_custom_position_y

        # Create the overlay
        rom_gauge_overlay = ROMGauge(
            name=parameter_name,
            data_path=data_path,
            column_index=parameter_index,  # Which column to use from the numpy file
            position=(
                position_x,
                position_y,
            ),
            size=(
                data_overlay_props.common_overlay_width,
                data_overlay_props.common_overlay_height,
            ),
            plot_title=parameter_title,
        )

        overlay_manager.add(rom_gauge_overlay, alignment=data_overlay_props.common_viewport_position)
        overlay_manager.enable()

        # Force a redraw to update the viewport
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}
