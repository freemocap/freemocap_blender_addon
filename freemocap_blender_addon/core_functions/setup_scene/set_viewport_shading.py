"""Set viewport shading mode across all open 3D Viewports."""

import bpy


def set_viewport_to_material_preview():
    """Set all 3D viewports to Material Preview shading mode.

    Iterates over every open window, screen, and area to find
    VIEW_3D spaces and switches their shading type to ``"MATERIAL"``
    (Material Preview / Look Dev mode).
    """
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.shading.type = "MATERIAL"
