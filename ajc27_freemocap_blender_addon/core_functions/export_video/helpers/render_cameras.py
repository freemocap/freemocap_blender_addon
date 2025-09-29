import bpy
from ajc27_freemocap_blender_addon.data_models.parameter_models.video_config import (
    EXPORT_PROFILES,
)

def render_cameras(
    export_profile: dict,
) -> None:

    # For each camera in the export profile cameras, render the animation
    for camera in export_profile['render_cameras']:

        # Change to the corresponding scene
        bpy.context.window.scene = bpy.data.scenes[f"Render_Camera_{camera}"]

        # Turn off use nodes in compositor for individual render cameras
        bpy.context.scene.use_nodes = False

        # Render the animation
        bpy.ops.render.render(animation=True)

    return
