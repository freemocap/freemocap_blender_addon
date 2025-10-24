import bpy
from typing import List

from ajc27_freemocap_blender_addon.blender_ui.operators.data_overlays.overlay_component import OverlayComponent

class OverlayManager:
    def __init__(self):
        self.overlays: List[OverlayComponent] = []
        self.horizontal_overlays: List[OverlayComponent] = []
        self.vertical_overlays: List[OverlayComponent] = []
        self.handler = None
        self.enabled = False

    def add(self, overlay, alignment='HORIZONTALLY_ALIGNED'):
        self.overlays.append(overlay)

        if alignment != 'CUSTOM':
            # If this is the first overlay and no specific alignment requested,
            # add to both lists (though this might not be the desired behavior)
            if not self.horizontal_overlays and not self.vertical_overlays:
                self.horizontal_overlays.append(overlay)
                self.vertical_overlays.append(overlay)
            elif alignment == 'HORIZONTALLY_ALIGNED':
                self.horizontal_overlays.append(overlay)
            elif alignment == 'VERTICALLY_ALIGNED':
                self.vertical_overlays.append(overlay)

    def remove(self, name):
        """Remove an overlay by name"""
        self.overlays = [ov for ov in self.overlays if ov.name != name]

    def remove_all(self):
        """Remove all overlays and disable drawing"""
        self.overlays = []
        self.horizontal_overlays = []
        self.vertical_overlays = []
        if self.enabled:
            self.disable()
        
    def get(self, name):
        """Get an overlay by name"""
        for ov in self.overlays:
            if ov.name == name:
                return ov
        return None

    def draw_all(self):
        for ov in self.overlays:
            if ov.visible:
                ov.draw()

    def enable(self):
        if not self.enabled:
            self.handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_all, (), 'WINDOW', 'POST_PIXEL'
            )
            self.enabled = True

    def disable(self):
        if self.enabled and self.handler is not None:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
                self.handler = None
                self.enabled = False
            except Exception as e:
                print(f"Error disabling overlay manager: {e}")
                # Force disable even if removal fails
                self.handler = None
                self.enabled = False

    def get_overlay_aligned_position(self, alignment, margin=10):
        if alignment == 'HORIZONTALLY_ALIGNED':
            if not self.horizontal_overlays:
                # First horizontally aligned overlay
                return (margin, margin)
            else:
                # Position after the last horizontally aligned overlay
                last_overlay = self.horizontal_overlays[-1]
                x = last_overlay.position[0] + last_overlay.size[0] + margin
                y = last_overlay.position[1]  # Keep same Y position
                return (x, y)
                
        elif alignment == 'VERTICALLY_ALIGNED':
            if not self.vertical_overlays:
                # First vertically aligned overlay
                return (margin, margin)
            else:
                # Position below the last vertically aligned overlay
                last_overlay = self.vertical_overlays[-1]
                x = last_overlay.position[0]  # Keep same X position
                y = last_overlay.position[1] + last_overlay.size[1] + margin
                return (x, y)
                
        else:
            # Default position for custom alignment
            return (margin, margin)
