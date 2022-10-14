import arcade
from enum import Enum
from typing import Optional
import random

SPRITE_SCALING = 0.3
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)
CAT_PATH = "assets/sprites/cat/Cat_"
DOG_PATH = "assets/sprites/dog/Dog_"

FRONT_FACING = 0
BACK_FACING = 1
RIGHT_FACING = 0
LEFT_FACING = 1

#Dog tasks
FOLLOW = 0
KEY = 1
DOOR = 2
DOG_TASKS = [FOLLOW, KEY, DOOR]

#Cat Constants
MEOW = ["Meow!", "meow...", "Meow!!!", "Meowver here!", "Meow", "Nya..."]

class Task(Enum):
    NONE = 0
    KEY = 1
    DOOR = 2
    FOLLOW = 3
    LEVER = 4

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

    def update_animation(self, delta_time: float = 1 / 60):
        x, y = self.actual_force
        if x < 0:
            self.texture = self.side_texture_pair[LEFT_FACING]
        elif x > 0:
            self.texture = self.side_texture_pair[RIGHT_FACING]
        elif y > 0:
            self.texture = self.front_texture_pair[BACK_FACING]
        elif y < 0:
            self.texture = self.front_texture_pair[FRONT_FACING]
        elif x == 0 and y == 0:
            self.texture = self.front_texture_pair[FRONT_FACING]
        return


class Cat(Animal):
    def __init__(self):
        super().__init__(CAT_PATH)
        self.npc_interaction = None
        self.touched = False
        self.meow = False
        self.meow_count = 0
        self.meow_text = None

    def start_meow(self, duration: int, text: str = None):
        if self.meow == False:
            self.meow = True
            self.meow_count = duration
            self.meow_text = text if text else random.choice(MEOW) 

    def cat_meowing(self):
        return self.meow

    def end_meow(self):
        self.meow = False

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

        self.force = 1000
        self.task : Optional[Task]= Task.NONE
        self.inventory = []

        self.follow = False
        self.goal = (0,0)

    def follow_cat(self):
        self.follow = True

    def set_goal(self, goal : tuple):
        #goal must be coordinates of tuple (0,0)
        self.goal = goal

    def stop_follow(self):
        self.follow = False
        self.goal = (0,0)
        if self.task == Task.FOLLOW:
            self.change_task(Task.NONE)

    def change_task(self, task):
        self.task = task

    def get_actions(self):
        return self.task