class _Interactible(arcade.Sprite):
    """ An abstract class that represents an interactible object """

class Mural(_Interactible):
    """ A mural object that hangs on walls """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #self.texture = arcade.load_texture()