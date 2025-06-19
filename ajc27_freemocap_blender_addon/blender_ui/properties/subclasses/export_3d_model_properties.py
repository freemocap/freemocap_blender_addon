import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes
from ajc27_freemocap_blender_addon.freemocap_data_handler.utilities.load_data import get_test_recording_path

# def get_blank_default_value() -> str:
#     return ""

class Export3DModelProperties(bpy.types.PropertyGroup):
    show_export_fbx_format_options: PropertyTypes.Bool(
        description = 'Toggle Export FBX Format Options'
    ) # type: ignore

    model_destination_path: PropertyTypes.Path(
        name='',
        description='Path where the 3D model will be saved',
    ) # type: ignore

    fbx_add_leaf_bones: PropertyTypes.Bool(
        name='',
        description='Add leaf bones to the FBX file (requires Blender 2.80 or newer)',
        default=False,
    ) # type: ignore

