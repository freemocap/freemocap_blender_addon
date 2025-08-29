import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes

class AddDataOverlaysProperties(bpy.types.PropertyGroup):
    show_add_data_overlays_options: PropertyTypes.Bool(
        description = 'Toggle Add Data Overlays Options'
    ) # type: ignore

    # Common Overlay Properties
    common_viewport_position: PropertyTypes.Enum(
        items = [
            ('HORIZONTALLY_ALIGNED', 'Horizontally Aligned', ''),
            ('VERTICALLY_ALIGNED', 'Vertically Aligned', ''),
            ('CUSTOM', 'Custom', ''),
        ],
        default = 'HORIZONTALLY_ALIGNED',
        description = 'Viewport position for new overlays. If Custom is selected, use the X and Y fields below to set the position manually.' \
        ' For horizontally or vertically aligned, the overlay is position next to the existing data overlays.'
    ) # type: ignore
    common_custom_position_x: PropertyTypes.Int(
        default = 10,
        min = 0,
    ) # type: ignore
    common_custom_position_y: PropertyTypes.Int(
        default = 10,
        min = 0,
    ) # type: ignore
    common_overlay_margin: PropertyTypes.Int(
        default = 10,
        min = 0,
    ) # type: ignore
    common_overlay_width: PropertyTypes.Int(
        default = 400,
        min = 10,
    ) # type: ignore
    common_overlay_height: PropertyTypes.Int(
        default = 300,
        min = 10,
    ) # type: ignore

    # Time Series Plot Properties
    show_time_series_plot_options: PropertyTypes.Bool(
        description = 'Toggle Time Series Plot Options'
    ) # type: ignore
    time_series_plot_parameter: PropertyTypes.Enum(
        items = [
            ('angle#left_elbow_extension_flexion', 'Angle: Left Elbow Extension/Flexion', ''),
            ('angle#left_shoulder_extension_flexion', 'Angle: Left Shoulder Extension/Flexion', ''),
            ('angle#left_shoulder_abduction_adduction', 'Angle: Left Shoulder Abduction/Adduction', ''),
            ('angle#right_elbow_extension_flexion', 'Angle: Right Elbow Extension/Flexion', ''),
            ('angle#right_shoulder_extension_flexion', 'Angle: Right Shoulder Extension/Flexion', ''),
            ('angle#right_shoulder_abduction_adduction', 'Angle: Right Shoulder Abduction/Adduction', ''),
            ('angle#left_knee_extension_flexion', 'Angle: Left Knee Extension/Flexion', ''),
            ('angle#left_hip_extension_flexion', 'Angle: Left Hip Extension/Flexion', ''),
            ('angle#left_hip_abduction_adduction', 'Angle: Left Hip Abduction/Adduction', ''),
            ('angle#right_knee_extension_flexion', 'Angle: Right Knee Extension/Flexion', ''),
            ('angle#right_hip_extension_flexion', 'Angle: Right Hip Extension/Flexion', ''),
            ('angle#right_hip_abduction_adduction', 'Angle: Right Hip Abduction/Adduction', ''),
            ('angle#neck_extension_flexion', 'Angle: Neck Extension/Flexion', ''),
            ('angle#neck_lateral_flexion', 'Angle: Neck Lateral/Flexion', ''),
            ('angle#neck_rotation', 'Angle: Neck Rotation', ''),
            ('angle#left_ankle_dorsiflexion_plantarflexion', 'Angle: Left Ankle Dorsiflexion/Plantarflexion', ''),
            ('angle#left_ankle_inversion_eversion', 'Angle: Left Ankle Inversion/Eversion', ''),
            ('angle#right_ankle_dorsiflexion_plantarflexion', 'Angle: Right Ankle Dorsiflexion/Plantarflexion', ''),
            ('angle#right_ankle_inversion_eversion', 'Angle: Right Ankle Inversion/Eversion', ''),
            ('angle#spine_extension_flexion', 'Angle: Spine Extension/Flexion', ''),
            ('angle#spine_lateral_flexion', 'Angle: Spine Lateral/Flexion', ''),
            ('angle#left_hand_extension_flexion', 'Angle: Left Hand Extension/Flexion', ''),
            ('angle#right_hand_extension_flexion', 'Angle: Right Hand Extension/Flexion', ''),
            ('com#center_of_mass_z', 'Center of Mass: Z Position', ''),
        ],
        default = 'angle#left_elbow_extension_flexion',
        description = 'Which parameter to plot in the time series overlay.'
    ) # type: ignore
    time_series_window_size: PropertyTypes.Int(
        default = 200,
        min = 10,
        description = 'Number of frames to display in the time series plot window.'
    ) # type: ignore
    time_series_line_color: PropertyTypes.FloatVector(
        default = tuple((0.371235,0.672444,0.693872,1.0))
    ) # type: ignore
    time_series_current_frame_line_color: PropertyTypes.FloatVector(
        default = tuple((0.693868,0.082283,0.095308,1.0))
    ) # type: ignore
    time_series_background_color: PropertyTypes.FloatVector(
        default = tuple((0.0185,0.056129,0.05448, 0.2))
    ) # type: ignore
    time_series_line_width: PropertyTypes.Float(
        default = 1.0,
        min = 0.1,
        precision = 1,
        description = 'Width of the time series plot line.'
    ) # type: ignore
    time_series_current_frame_line_width: PropertyTypes.Float(
        default = 1.5,
        min = 0.1,
        precision = 1,
        description = 'Width of the current frame indicator line.'
    ) # type: ignore
    time_series_border_line_width: PropertyTypes.Float(
        default = 1.0,
        min = 0.1,
        precision = 1,
        description = 'Width of the border around the time series plot.'
    ) # type: ignore

    # ROM Gauge Properties
    show_rom_gauge_options: PropertyTypes.Bool(
        description = 'Toggle ROM Gauge Options'
    ) # type: ignore
    rom_gauge_parameter: PropertyTypes.Enum(
        items = [
            ('angle#left_elbow_extension_flexion', 'Angle: Left Elbow Extension/Flexion', ''),
            ('angle#left_shoulder_extension_flexion', 'Angle: Left Shoulder Extension/Flexion', ''),
            ('angle#left_shoulder_abduction_adduction', 'Angle: Left Shoulder Abduction/Adduction', ''),
            ('angle#right_elbow_extension_flexion', 'Angle: Right Elbow Extension/Flexion', ''),
            ('angle#right_shoulder_extension_flexion', 'Angle: Right Shoulder Extension/Flexion', ''),
            ('angle#right_shoulder_abduction_adduction', 'Angle: Right Shoulder Abduction/Adduction', ''),
            ('angle#left_knee_extension_flexion', 'Angle: Left Knee Extension/Flexion', ''),
            ('angle#left_hip_extension_flexion', 'Angle: Left Hip Extension/Flexion', ''),
            ('angle#left_hip_abduction_adduction', 'Angle: Left Hip Abduction/Adduction', ''),
            ('angle#right_knee_extension_flexion', 'Angle: Right Knee Extension/Flexion', ''),
            ('angle#right_hip_extension_flexion', 'Angle: Right Hip Extension/Flexion', ''),
            ('angle#right_hip_abduction_adduction', 'Angle: Right Hip Abduction/Adduction', ''),
            ('angle#neck_extension_flexion', 'Angle: Neck Extension/Flexion', ''),
            ('angle#neck_lateral_flexion', 'Angle: Neck Lateral/Flexion', ''),
            ('angle#neck_rotation', 'Angle: Neck Rotation', ''),
            ('angle#left_ankle_dorsiflexion_plantarflexion', 'Angle: Left Ankle Dorsiflexion/Plantarflexion', ''),
            ('angle#left_ankle_inversion_eversion', 'Angle: Left Ankle Inversion/Eversion', ''),
            ('angle#right_ankle_dorsiflexion_plantarflexion', 'Angle: Right Ankle Dorsiflexion/Plantarflexion', ''),
            ('angle#right_ankle_inversion_eversion', 'Angle: Right Ankle Inversion/Eversion', ''),
            ('angle#spine_extension_flexion', 'Angle: Spine Extension/Flexion', ''),
            ('angle#spine_lateral_flexion', 'Angle: Spine Lateral/Flexion', ''),
            ('angle#left_hand_extension_flexion', 'Angle: Left Hand Extension/Flexion', ''),
            ('angle#right_hand_extension_flexion', 'Angle: Right Hand Extension/Flexion', ''),
        ],
        default = 'angle#left_elbow_extension_flexion',
        description = 'Which parameter to plot in the ROM gauge.'
    ) # type: ignore