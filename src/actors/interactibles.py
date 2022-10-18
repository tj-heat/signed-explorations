from typing import List
import arcade

# Constants
MURAL_INTERACTIBLE = "mural"
TORCH_LIT_INTERACTIBLE = "torch_lit"
RUBY_INTERACTIBLE = "ruby_table"
SHELF_BOOKS_INTERACTIBLE = "bookshelf_books"
SHELF_EMPTY_INTERACTIBLE = "bookshelf_empty"
SHELF_FULL_INTERACTIBLE = "bookshelf_full"
SHELF_JARS_INTERACTIBLE = "bookshelf_jars"
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


class Shelves(Interactible):
    """ An abstract class representing a set of shelf """

class ShelfBooks(Shelves):
    """ A Bookshelf full of books """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf_Books.png"

class ShelfEmpty(Shelves):
    """ An empty set of shelves """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf_Empty.png"

class ShelfFull(Shelves):
    """ A Bookshelf full of items """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf_Full.png"

class ShelfJars(Shelves):
    """ A Bookshelf with jars on its shelves """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf_Jars.png"

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
    MURAL_INTERACTIBLE: Mural,
    RUBY_INTERACTIBLE: TableRuby,
    SHELF_BOOKS_INTERACTIBLE: ShelfBooks,
    SHELF_EMPTY_INTERACTIBLE: ShelfEmpty,
    SHELF_FULL_INTERACTIBLE: ShelfFull,
    SHELF_JARS_INTERACTIBLE: ShelfJars,
    TORCH_LIT_INTERACTIBLE: TorchLit,
}