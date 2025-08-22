class OverlayComponent:
    def __init__(self, name, pos=(10,10), size=(200,150)):
        self.name = name
        self.pos = pos
        self.size = size
        self.visible = True

    def draw(self):
        """Override in subclass"""
        raise NotImplementedError
