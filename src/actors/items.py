import arcade
from src.actors.character import Task

KEY_PATH = "assets/sprites/items/interact_key.PNG"
DOOR_PATH = "assets/sprites/door/Door_stone"


class Key(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.type = "Key"
        self.task = Task.KEY
        self.texture = arcade.load_texture(KEY_PATH)
        self.hit_box = self.texture.hit_box_points

class Door(arcade.Sprite):
    def __init__(self, option, key, orientation):
        super().__init__()

        self.type = "Door"
        self.task = Task.DOOR
        self.key = key

        self.open_texture_pair = None

        if option == "side" and orientation == "left":
            self.open_texture_pair = [arcade.load_texture(f"{DOOR_PATH}_side.png"), arcade.load_texture(f"{DOOR_PATH}_side_open.png")]
        elif option == "side" and orientation == "right":
            self.open_texture_pair = [arcade.load_texture(f"{DOOR_PATH}_side.png", flipped_horizontally=True), arcade.load_texture(f"{DOOR_PATH}_side_open.png", flipped_horizontally=True)]
        else:
            self.open_texture_pair = [arcade.load_texture(f"{DOOR_PATH}.png"), arcade.load_texture(f"{DOOR_PATH}_open.png")]

        self.texture = self.open_texture_pair[0]

        self.hit_box = self.texture.hit_box_points

    def open_door(self):
        self.texture = self.open_texture_pair[1]

    

