import bpy
from ajc27_freemocap_blender_addon.blender_ui.properties.property_types import PropertyTypes


class Export3DModelProperties(bpy.types.PropertyGroup):
    show_export_fbx_format_options: PropertyTypes.Bool(
        description = 'Toggle Export FBX Format Options'
    ) # type: ignore

    model_destination_folder: PropertyTypes.Path(
        name='',
        description='Folder where the 3D model will be saved',
    ) # type: ignore

    model_format: PropertyTypes.Enum(
        name='',
        description='Format of the 3D model',
        items=[
            ('fbx', 'FBX', 'FBX'),
            ('bvh', 'BVH', 'BVH'),
        ],
        default='FBX',
    ) # type: ignore

    bones_naming_convention: PropertyTypes.Enum(
        name='',
        description='Naming convention for the bones',
        items=[
            ('default', 'Default', 'Default'),
            ('metahuman', 'Metahuman', 'Metahuman'),
            ('daz_g8.1', 'DAZ G8.1', 'DAZ G8.1'),
        ],
        default='Default',
    ) # type: ignore

    rest_pose_type: PropertyTypes.Enum(
        name='',
        description='Type of the rest pose',
        items=[
            ('default', 'Default', 'Default'),
            ('metahuman', 'Metahuman', 'Metahuman'),
            ('daz_g8.1', 'DAZ G8.1', 'DAZ G8.1'),
        ],
        default='Default',
    ) # type: ignore

    restore_defaults_after_export: PropertyTypes.Bool(
        name='',
        description='Restore the original bone names, rest pose and added/deleted bone after exporting the model',
        default=True,
    ) # type: ignore

    fbx_add_leaf_bones: PropertyTypes.Bool(
        name='',
        description='Add leaf bones to the FBX file (requires Blender 2.80 or newer)',
        default=False,
    ) # type: ignore
    fbx_primary_bone_axis: PropertyTypes.Enum(
        name='',
        description='Primary bone axis.',
        items=[
            ('Y', 'Y', 'Y'),
            ('X', 'X', 'X'),
            ('Z', 'Z', 'Z'),
            ('-X', '-X', '-X'),
            ('-Y', '-Y', '-Y'),
            ('-Z', '-Z', '-Z'),
        ],
    ) # type: ignore
    fbx_secondary_bone_axis: PropertyTypes.Enum(
        name='',
        description='Secondary bone axis.',
        items=[
            ('X', 'X', 'X'),
            ('Y', 'Y', 'Y'),
            ('Z', 'Z', 'Z'),
            ('-X', '-X', '-X'),
            ('-Y', '-Y', '-Y'),
            ('-Z', '-Z', '-Z'),
        ],
    ) # type: ignore
