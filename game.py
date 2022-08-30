import arcade
import math
import random
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

SPRITE_SCALING = 0.25
MOVEMENT_SPEED = 5
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

PLAYER_MOVE_FORCE = 4000
BULLET_MOVE_FORCE = 2500

STONE_PATH = "assets/tiles/stone_1.png"
WOOD_PATH = "assets/tiles/wood_1.png"
CAT_PATH = "assets/sprites/Cat_front.PNG"

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

        #self.player_list = None
        #self.wall_list = None
        self.player_sprite = None

        #Our scene object
        self.scene = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
    
    def setup(self):
        #Initialise scene
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash = True)

        self.player_sprite = arcade.Sprite(CAT_PATH, SPRITE_SCALING) #diff might be in scaling, check val
        self.player_sprite.center_x = self.window.width/2
        self.player_sprite.center_y = self.window.height/2
        self.scene.add_sprite("Player", self.player_sprite)


        for x in range(0, self.window.width, SPRITE_SIZE):
            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = SPRITE_SIZE/2
            self.scene.add_sprite("Walls", wall)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """


    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.scene.draw()