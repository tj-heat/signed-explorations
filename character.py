import arcade
from enum import Enum

SPRITE_SCALING = 0.3
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)
CAT_PATH = "assets/sprites/cat/Cat_"
DOG_PATH = "assets/sprites/dog/Dog_"

FRONT_FACING = 0
BACK_FACING = 1
RIGHT_FACING = 0
LEFT_FACING = 1

DEAD_ZONE = 0.1

#Dog tasks
FOLLOW = 0
KEY = 1
DOOR = 2
DOG_TASKS = [FOLLOW, KEY, DOOR]

class Task(Enum):
    NONE = 0
    KEY = 1
    DOOR = 2
    FOLLOW = 3

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Animal(arcade.Sprite):
    def __init__(self, path):
        super().__init__()

        self.cur_texture= 0
        self.scale = SPRITE_SCALING

        #texture 0 is right facing
        self.side_texture_pair = load_texture_pair(f"{path}side.PNG")
        #texture 0 is front
        self.front_texture_pair = [arcade.load_texture(f"{path}front.PNG"),
                                    arcade.load_texture(f"{path}back.PNG")]

        self.texture = self.front_texture_pair[0]

        self.hit_box = self.texture.hit_box_points

        self.actual_force = (0,0)

        self.x_odometer = 0
        self.y_odometer = 0

    def update_animation(self, delta_time: float = 1 / 60):
        x, y = self.actual_force
        if x < 0:
            self.texture = self.side_texture_pair[LEFT_FACING]
        if x > 0:
            self.texture = self.side_texture_pair[RIGHT_FACING]
        if y > 0:
            self.texture = self.front_texture_pair[BACK_FACING]
        if y < 0:
            self.texture = self.front_texture_pair[FRONT_FACING]
        if x == 0 and y == 0:
            self.texture = self.front_texture_pair[FRONT_FACING]
        return

"""
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dy < -DEAD_ZONE:
            self.texture = self.front_texture_pair[FRONT_FACING]
        if dy > DEAD_ZONE:
            self.texture = self.front_texture_pair[BACK_FACING]
        if dx < -DEAD_ZONE:
            self.texture = self.side_texture_pair[LEFT_FACING]
        if dx > DEAD_ZONE:
            self.texture = self.side_texture_pair[RIGHT_FACING]

        #self.x_odometer += dx // only needed for walk cycles
        #self.y_odometer += dy
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.front_texture_pair[FRONT_FACING]
            return
"""


class Cat(Animal):
    def __init__(self):
        super().__init__(CAT_PATH)
        self.npc_interaction = None
        self.touched = False

    def set_npc_interaction(self, npc):
        self.npc_interaction = npc

    def null_npc_interaction(self):
        self.npc_interaction = None

    def untouched(self):
        self.touched = False

    def is_touched(self):
        return self.touched

class Dog(Animal):
    def __init__(self):
        super().__init__(DOG_PATH)

        self.force = 2000
        self.task = Task.NONE
        self.inventory = []

    def change_task(self, task):
        self.task = task

    def get_actions(self):
        return self.task