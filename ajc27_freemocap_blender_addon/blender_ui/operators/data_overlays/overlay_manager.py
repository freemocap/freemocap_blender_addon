import bpy

class OverlayManager:
    def __init__(self):
        self.overlays = []
        self.handler = None
        self.enabled = False

    def add(self, overlay):
        self.overlays.append(overlay)

    def remove(self, name):
        """Remove an overlay by name"""
        self.overlays = [ov for ov in self.overlays if ov.name != name]

    def remove_all(self):
        """Remove all overlays"""
        self.overlays = []
        
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
        if self.enabled:
            bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
            self.handler = None
            self.enabled = False