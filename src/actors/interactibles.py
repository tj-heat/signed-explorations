from typing import List
import arcade

# Constants
MURAL_INTERACTIBLE = "mural"
TORCH_LIT_INTERACTIBLE = "torch_lit"
RUBY_INTERACTIBLE = "ruby_table"
BOOKSHELF_INTERACTIBLE = "bookshelf"
_INTERACTIBLE = ""

class Interactible(arcade.Sprite):
    """ An abstract class that represents an interactible object """
    _TEX_PATH = None
    _PRE_MSGS = ["Nothing"]
    _POST_MSGS = ["Nothing again"]
    _DISPLAY_IMG = None
    _X_OFFSET = 0
    _Y_OFFSET = 0

    def __init__(self, tile_size: int, **kwargs):
        super().__init__(**kwargs)

        self._tile_size = tile_size
        self.texture = arcade.load_texture(self._TEX_PATH)

    def get_pre_msgs(self) -> List[str]:
        """ Return the pre-interaction messages for the object """
        return self._PRE_MSGS

    def get_post_msgs(self) -> List[str]:
        """ Return the post-interaction messages for the object """
        return self._POST_MSGS

    def get_focus_texture(self) -> arcade.Texture:
        """ Return the texture to display upon interaction """
        return self._DISPLAY_IMG

    def set_center(self, x, y) -> None:
        """ Set the center position of the object's body """
        self.center_x = x + (self._tile_size * self._X_OFFSET)
        self.center_y = y + (self._tile_size * self._Y_OFFSET)


class BookShelf(Interactible):
    """ A sparsely populated bookshelf """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf.png"
    _Y_OFFSET = 0


class Mural(Interactible):
    """ A mural object that hangs on walls """
    _TEX_PATH = "assets/sprites/interactibles/Object_Sign.png"


class TableRuby(Interactible):
    """ A table with a ruby on it"""
    _TEX_PATH = "assets/sprites/interactibles/Object_Table.png"
    _X_OFFSET = -0.5


class TorchLit(Interactible):
    """ A tall lit torch """
    _TEX_PATH = "assets/sprites/interactibles/Object_Light.png"
    _Y_OFFSET = 1


INTERACTIBLES = {
    BOOKSHELF_INTERACTIBLE: BookShelf,
    MURAL_INTERACTIBLE: Mural,
    RUBY_INTERACTIBLE: TableRuby,
    TORCH_LIT_INTERACTIBLE: TorchLit,
}