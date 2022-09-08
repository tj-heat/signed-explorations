import arcade
from typing import Optional
from character import Task

KEY_PATH = "assets/tilemaps/Key.PNG"

# class Item(arcade.Sprite):
#     def __init__(self):
#         super().__init__()

#         self.task : Optional[Task] = None


class Key(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.type = "Key"
        self.task = Task.KEY
        self.texture = arcade.load_texture(KEY_PATH)
        self.hit_box = self.texture.hit_box_points