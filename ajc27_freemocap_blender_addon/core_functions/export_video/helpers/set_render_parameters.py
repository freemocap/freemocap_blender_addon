import bpy
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    RENDER_PARAMETERS
)

def set_render_parameters() -> None:

    # Set the rendering properties
    for key, value in RENDER_PARAMETERS.items():

        # Split the key into context and property names
        key_parts = key.split(".")

        # Start with the bpy.context object
        context = bpy.context

        # Traverse through the key parts to access the correct context and
        # property
        for part in key_parts[:-1]:
            context = getattr(context, part)

        # Set the property
        setattr(context, key_parts[-1], value)

    return
