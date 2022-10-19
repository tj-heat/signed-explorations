from typing import List
import random

import arcade

# Constants
MURAL_INTERACTIBLE = "mural"
TORCH_LIT_INTERACTIBLE = "torch_lit"
TABLE_INTERACTIBLE = "table_empty"
RUBY_INTERACTIBLE = "table_ruby"
SHELF_BOOKS_INTERACTIBLE = "bookshelf_books"
SHELF_EMPTY_INTERACTIBLE = "bookshelf_empty"
SHELF_FULL_INTERACTIBLE = "bookshelf_full"
SHELF_JARS_INTERACTIBLE = "bookshelf_jars"
_INTERACTIBLE = ""

# Learn letter messages
INITIAL_LEARN = [
    "I think I just learnt a new letter!",
    "I should check my spell book to be sure.",
    "I wonder if there's anything else I can learn from around here."
]
LEARN_MSGS = [
    ["I think I just learnt something."],
    ["It feels like knowledge just entered my head."],
    ["Did I just get smarter?"],
]

def get_random_learn() -> List[str]:
    """ Returns a random learn message set. """
    return random.choice(LEARN_MSGS)

class Interactible(arcade.Sprite):
    """ An abstract class that represents an interactible object """
    _TEX_PATH = None
    _PRE_MSGS = []
    _POST_MSGS = []
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

    def get_focus_texture(self) -> str:
        """ Return the path of the texture to display upon interaction """
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
    _PRE_MSGS = ["I can't get any of the books out."]


class ShelfEmpty(Shelves):
    """ An empty set of shelves """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf_Empty.png"
    _PRE_MSGS = ["There's nothing here"]


class ShelfFull(Shelves):
    """ A Bookshelf full of items """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf_Full.png"
    _PRE_MSGS = ["That's a lot of stuff!"]


class ShelfJars(Shelves):
    """ A Bookshelf with jars on its shelves """
    _TEX_PATH = "assets/sprites/interactibles/Object_Bookshelf_Jars.png"
    _PRE_MSGS = ["I wonder what's in those jars..."]


class Mural(Interactible):
    """ A mural object that hangs on walls """
    _TEX_PATH = "assets/sprites/interactibles/Object_Sign.png"
    _PRE_MSGS = ["It looks like something is written here..."]
    _POST_MSGS = get_random_learn()
    _DISPLAY_IMG = "assets/screens/K_screen.png"

    def __init__(self, tile_size: int, **kwargs):
        super().__init__(tile_size, **kwargs)
        self.texture = arcade.load_texture(
            self._TEX_PATH, 
            hit_box_algorithm="None"
        )

        self._interacted = False

    def get_post_msgs(self) -> List[str]:
        if not self._interacted:
            self._interacted = True
            return INITIAL_LEARN
        else:
            return super().get_post_msgs()


class Table(Interactible):
    """ Base class for the table objects """
    _X_OFFSET = -0.5


class TableEmpty(Table):
    """ An empty table """
    _TEX_PATH = "assets/sprites/interactibles/Object_Table_Empty.png"
    _PRE_MSGS = ["I could knock so much stuff off of this..."]


class TableRuby(Table):
    """ A table with a ruby on it"""
    _TEX_PATH = "assets/sprites/interactibles/Object_Table_Ruby.png"
    _PRE_MSGS = ["Wow, that looks shiny!"]
    _POST_MSGS = get_random_learn()
    _DISPLAY_IMG = "assets/screens/Y_screen.png"


class TorchLit(Interactible):
    """ A tall lit torch """
    _TEX_PATH = "assets/sprites/interactibles/Object_Light.png"
    _Y_OFFSET = 1
    _PRE_MSGS = ["There's something etched into the shaft."]
    _POST_MSGS = get_random_learn()
    _DISPLAY_IMG = "assets/screens/E_screen.png"


INTERACTIBLES = {
    MURAL_INTERACTIBLE: Mural,
    RUBY_INTERACTIBLE: TableRuby,
    SHELF_BOOKS_INTERACTIBLE: ShelfBooks,
    SHELF_EMPTY_INTERACTIBLE: ShelfEmpty,
    SHELF_FULL_INTERACTIBLE: ShelfFull,
    SHELF_JARS_INTERACTIBLE: ShelfJars,
    TABLE_INTERACTIBLE: TableEmpty,
    TORCH_LIT_INTERACTIBLE: TorchLit,
}