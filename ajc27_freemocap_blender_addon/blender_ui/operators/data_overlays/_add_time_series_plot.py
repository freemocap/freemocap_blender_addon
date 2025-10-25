import bpy

from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_manager import OverlayManager
from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlays.time_series_plot import TimeSeriesPlot

# TODO: Probably generate the joint angle numpy file as a npz file to include the column names
# and then load the npz file here to get the column names dynamically
# and don't rely on a hardcoded dictionary or a separate csv file

def get_column_names_from_csv(csv_filepath):
    with open(csv_filepath, 'r') as f:
        header_line = f.readline().strip()
    # Split the first line by commas to get the list of names
    column_names = header_line.split(',')
    return column_names

class FREEMOCAP_OT_add_time_series_plot(bpy.types.Operator):
    bl_idname = 'freemocap._add_time_series_plot'
    bl_label = 'Add Time Series Plot Overlay'
    bl_description = "Add Time Series Plot Overlay"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    def execute(self, context):
        print("Adding Data Overlay.......")
        ui_props = context.scene.freemocap_ui_properties
        data_overlay_props = ui_props.add_data_overlays_properties
        core_props = context.scene.freemocap_properties
        overlay_manager = context.scene.freemocap_overlay_manager

        # Get the type and name of the parameter to plot
        parameter = data_overlay_props.time_series_plot_parameter
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
            value_unit = "°"

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
        elif parameter_type == 'com':
            data_path = core_props.recording_path + "output_data\\center_of_mass\\mediapipe_total_body_center_of_mass_xyz.npy"
            value_unit = "mm"
            if parameter_name == 'center_of_mass_x': parameter_index = 0
            elif parameter_name == 'center_of_mass_y': parameter_index = 1
            elif parameter_name == 'center_of_mass_z': parameter_index = 2
            
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
        time_series_plot_overlay = TimeSeriesPlot(
            name=parameter_name,
            data_path=data_path,
            column_index=parameter_index,  # Which column to use from the numpy file
            window_size=data_overlay_props.time_series_window_size,  # Number of frames to show
            position=(
                position_x,
                position_y,
            ),
            size=(
                data_overlay_props.common_overlay_width,
                data_overlay_props.common_overlay_height,
            ),
            plot_title=parameter_title,
            line_color=tuple(data_overlay_props.time_series_line_color),
            current_frame_line_color=tuple(data_overlay_props.time_series_current_frame_line_color),
            background_color=tuple(data_overlay_props.time_series_background_color),
            line_width=data_overlay_props.time_series_line_width,
            current_frame_line_width=data_overlay_props.time_series_current_frame_line_width,
            border_line_width=data_overlay_props.time_series_border_line_width,
            value_unit=value_unit,
        )

        overlay_manager.add(time_series_plot_overlay, alignment=data_overlay_props.common_viewport_position)
        overlay_manager.enable()

        # Force a redraw to update the viewport
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}
