import bpy

# Function to force absolute path in the UI
def get_blank_default_value() -> str:
    return ""

class PropertyTypes:
    Bool = lambda **kwargs: bpy.props.BoolProperty(
                name=kwargs.get('name', ''),
                default=kwargs.get('default', False),
                description=kwargs.get('description', '')
    )
    Enum = lambda **kwargs: bpy.props.EnumProperty(
                name=kwargs.get('name', ''),
                description=kwargs.get('description', ''),
                items=kwargs.get('items', [])
    )
    Float = lambda **kwargs: bpy.props.FloatProperty(
                name=kwargs.get('name', ''),
                default=kwargs.get('default', 0.0),
                precision=kwargs.get('precision', 3),
                description=kwargs.get('description', '')
    )
    Int = lambda **kwargs: bpy.props.IntProperty(
                name=kwargs.get('name', ''),
                default=kwargs.get('default', 0),
                description=kwargs.get('description', '')
    )
    Collection = lambda **kwargs: bpy.props.CollectionProperty(
                name=kwargs.get('name', ''),
                description=kwargs.get('description', ''),
                type=kwargs.get('type', bpy.types.PropertyGroup)
    )
    String = lambda **kwargs: bpy.props.StringProperty(
                name=kwargs.get('name', ''),
                default=kwargs.get('default', ''),
                description=kwargs.get('description', '')
    )
    Path = lambda **kwargs: bpy.props.StringProperty(
        name=kwargs.get('name', ''),
        default=get_blank_default_value(),
        subtype='DIR_PATH',
        description=kwargs.get('description', '')
    )
    FilePath = lambda **kwargs: bpy.props.StringProperty(
        name=kwargs.get('name', ''),
        default=get_blank_default_value(),
        subtype='FILE_PATH',
        description=kwargs.get('description', '')
    )
