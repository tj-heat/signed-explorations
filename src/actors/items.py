import arcade
from src.actors.character import Task

KEY_PATH = "assets/sprites/items/interact_key.PNG"
DOOR_SIDE_PATH = "assets/sprites/door/Door_stone_side_open.png"
DOOR_ORTHOGONAL_PATH = "assets/sprites/door/Door_stone_open.png"



class Key(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.type = "Key"
        self.task = Task.KEY
        self.texture = arcade.load_texture(KEY_PATH)
        self.hit_box = self.texture.hit_box_points

class Door(arcade.Sprite):
    def __init__(self, option, key):
        super().__init__()

        self.type = "Door"
        self.task = Task.DOOR
        self.hit_box = self.texture.hit_box_points
        self.key = key

        if option == "side":
            self.open_texture = arcade.load_texture(DOOR_SIDE_PATH)
        else:
            self.open_texture = arcade.load_texture(DOOR_ORTHOGONAL_PATH)

