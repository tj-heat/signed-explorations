import arcade
import math
import random
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

SPRITE_SCALING = 0.25
MOVEMENT_SPEED = 3
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

PLAYER_MOVE_FORCE = 3000
BULLET_MOVE_FORCE = 2500

STONE_PATH = "assets/tiles/stone_1.png"
WOOD_PATH = "assets/tiles/wood_1.png"
CAT_PATH = "assets/sprites/Cat_front.PNG"

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

        #Our scene object
        self.scene = None
        #player object
        self.player_sprite = None
        #phys engine
        self.physics_engine = None

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

            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = self.window.height - SPRITE_SIZE/2
            self.scene.add_sprite("Walls", wall)

        for y in range(SPRITE_SIZE, self.window.height, SPRITE_SIZE):
            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = SPRITE_SIZE/2
            wall.center_y = y
            self.scene.add_sprite("Walls", wall)

            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = self.window.width - SPRITE_SIZE/2
            wall.center_y = y
            self.scene.add_sprite("Walls", wall)
        
        #Create physics engine
        """self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )"""

        self.physics_engine = PymunkPhysicsEngine(damping=0.7, gravity=(0,0))
        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("Player"),
            friction = 0.6,
            moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
            damping = 0.01,
            collision_type="player")

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("Walls"),
            friction = 0.6,
            collision_type="wall",
            body_type = PymunkPhysicsEngine.STATIC)
        


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            force = (0, PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
        elif self.down_pressed and not self.up_pressed:
            force = (0, -PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
            force = (-PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
        elif self.right_pressed and not self.left_pressed:
            force = (PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)

        # --- Move items in the physics engine
        self.physics_engine.step()


    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.scene.draw()