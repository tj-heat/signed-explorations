from pickle import NONE
import arcade

# Constants
MURAL_INTERACTIBLE = "mural"
TORCH_LIT_INTERACTIBLE = "torch_lit"
RUBY_INTERACTIBLE = "ruby_table"
BOOKSHELF_INTERACTIBLE = "bookshelf"
_INTERACTIBLE = ""

class _Interactible(arcade.Sprite):
    """ An abstract class that represents an interactible object """
    _TEX_PATH = NONE
    _X_OFFSET = 0
    _Y_OFFSET = 0

    def __init__(self, tile_size: int, **kwargs):
        super().__init__(**kwargs)

        self._tile_size = tile_size
        self.texture = arcade.load_texture(self._TEX_PATH)

    def set_center(self, x, y) -> None:
        """ Set the center position of the object's body """
        self.center_x = x + (self._tile_size * self._X_OFFSET)
        self.center_y = y + (self._tile_size * self._Y_OFFSET)


class BookShelf(_Interactible):
    """ A sparsely populated bookshelf """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf.png"
    _Y_OFFSET = -0.5


class Mural(_Interactible):
    """ A mural object that hangs on walls """
    _TEX_PATH = "assets/sprites/interactibles/Object_Sign.png"


class TableRuby(_Interactible):
    """ A table with a ruby on it"""
    _TEX_PATH = "assets/sprites/interactibles/Object_Table.png"


class TorchLit(_Interactible):
    """ A tall lit torch """
    _TEX_PATH = "assets/sprites/interactibles/Object_Light.png"
    _Y_OFFSET = 1


INTERACTIBLES = {
    BOOKSHELF_INTERACTIBLE: BookShelf,
    MURAL_INTERACTIBLE: Mural,
    RUBY_INTERACTIBLE: TableRuby,
    TORCH_LIT_INTERACTIBLE: TorchLit,
}