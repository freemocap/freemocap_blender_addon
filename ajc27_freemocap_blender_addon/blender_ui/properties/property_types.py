import bpy

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
    