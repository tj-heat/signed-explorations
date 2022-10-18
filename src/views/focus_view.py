import arcade

class FocusView(arcade.View):
    """ A view that will show a single image on the entire window. This view 
    will return to the originating view on key release.
    """
    def __init__(self, origin: arcade.View, texture_path: arcade.Texture):
        super().__init__()

        self._origin = origin
        self._texture = arcade.load_texture(texture_path)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            self.window.width / 2, self.window.height / 2,
            self._texture.width, self._texture.height,
            self._texture
        )

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.clear()
        self.window.show_view(self._origin)