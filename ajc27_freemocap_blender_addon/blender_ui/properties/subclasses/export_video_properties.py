import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes


class ExportVideoProperties(bpy.types.PropertyGroup):
    export_profile: PropertyTypes.Enum(
        name='',
        description='Profile for exporting the video',
        items=[
            ('showcase', 'Showcase', 'Showcase'),
            ('debug', 'Debug', 'Debug'),
            ('scientific', 'Scientific', 'Scientific'),
            ('multiview', 'Multiview', 'Multiview'),
            ('custom', 'Custom', 'Custom'),
        ],
        default='Showcase',
    ) # type: ignore
    show_custom_profile_options: PropertyTypes.Bool(
        description = 'Toggle Custom Profile Options'
    ) # type: ignore
    custom_profile_width: PropertyTypes.Int(
        name='',
        description='Custom profile horizontal resolution',
        default=1920,
    ) # type: ignore
    custom_profile_height: PropertyTypes.Int(
        name='',
        description='Custom profile vertical resolution',
        default=1080,
    ) # type: ignore
    custom_use_front_camera: PropertyTypes.Bool(
        name='Front Camera',
        description='Use Front Camera in the export',
        default=True,
    ) # type: ignore
    custom_front_camera_width: PropertyTypes.Int(
        name='',
        description='Custom profile horizontal resolution for the Front camera',
        default=1920,
    ) # type: ignore
    custom_front_camera_height: PropertyTypes.Int(
        name='',
        description='Custom profile vertical resolution for the Front camera',
        default=1080,
    ) # type: ignore
    custom_front_camera_position_x: PropertyTypes.Float(
        name='',
        description='Horizontal position of the Front camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_front_camera_position_y: PropertyTypes.Float(
        name='',
        description='Vertical position of the Front camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_use_left_camera: PropertyTypes.Bool(
        name='Left Camera',
        description='Use Left Camera in the export',
        default=False,
    ) # type: ignore
    custom_left_camera_width: PropertyTypes.Int(
        name='',
        description='Custom profile horizontal resolution for the Left camera',
        default=1920,
    ) # type: ignore
    custom_left_camera_height: PropertyTypes.Int(
        name='',
        description='Custom profile vertical resolution for the Left camera',
        default=1080,
    ) # type: ignore
    custom_left_camera_position_x: PropertyTypes.Float(
        name='',
        description='Horizontal position of the Left camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_left_camera_position_y: PropertyTypes.Float(
        name='',
        description='Vertical position of the Left camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_use_right_camera: PropertyTypes.Bool(
        name='Right Camera',
        description='Use Right Camera in the export',
        default=False,
    ) # type: ignore
    custom_right_camera_width: PropertyTypes.Int(
        name='',
        description='Custom profile horizontal resolution for the Right camera',
        default=1920,
    ) # type: ignore
    custom_right_camera_height: PropertyTypes.Int(
        name='',
        description='Custom profile vertical resolution for the Right camera',
        default=1080,
    ) # type: ignore
    custom_right_camera_position_x: PropertyTypes.Float(
        name='',
        description='Horizontal position of the Right camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_right_camera_position_y: PropertyTypes.Float(
        name='',
        description='Vertical position of the Right camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_use_top_camera: PropertyTypes.Bool(
        name='Top Camera',
        description='Use Top Camera in the export',
        default=False,
    ) # type: ignore
    custom_top_camera_width: PropertyTypes.Int(
        name='',
        description='Custom profile horizontal resolution for the Top camera',
        default=1920,
    ) # type: ignore
    custom_top_camera_height: PropertyTypes.Int(
        name='',
        description='Custom profile vertical resolution for the Top camera',
        default=1080,
    ) # type: ignore
    custom_top_camera_position_x: PropertyTypes.Float(
        name='',
        description='Horizontal position of the Top camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_top_camera_position_y: PropertyTypes.Float(
        name='',
        description='Vertical position of the Top camera overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.0,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_overlays_add_freemocap_logo: PropertyTypes.Bool(
        name='FreeMoCap Logo',
        description='Add FreeMoCap logo.',
        default=True,
    ) # type: ignore
    custom_overlays_freemocap_logo_scale_x: PropertyTypes.Float(
        name='',
        description='Logo x axis scale',
        default=0.2,
        min=0.01,
        max=1.0,
    ) # type: ignore
    custom_overlays_freemocap_logo_scale_y: PropertyTypes.Float(
        name='',
        description='Logo y axis scale',
        default=0.2,
        min=0.01,
        max=1.0,
    ) # type: ignore
    custom_overlays_freemocap_logo_position_x: PropertyTypes.Float(
        name='',
        description='Horizontal position of the logo overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.45,
        min=-0.5,
        max=0.5,
    ) # type: ignore
    custom_overlays_freemocap_logo_position_y: PropertyTypes.Float(
        name='',
        description='Vertical position of the logo overlay in the video based on total resolution (from -0.5 to 0.5)',
        default=0.4,
        min=-0.5,
        max=0.5,
    ) # type: ignore

