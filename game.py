import arcade
import math
import random
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

SPRITE_SCALING = 0.3
MOVEMENT_SPEED = 3
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)


TILE_SCALING = 1
TILE_SIZE = 62
GRID_SIZE = TILE_SCALING * TILE_SIZE

PLAYER_START_X = 124
PLAYER_START_Y = 124

PLAYER_MOVE_FORCE = 3000
BULLET_MOVE_FORCE = 2500

LAYER_NAME_WALLS = "Walls"
LAYER_NAME_NO_PHYS_WALLS = "Lower Walls"
LAYER_NAME_FLOOR = "Floor"
LAYER_NAME_DOORS = "Doors"
LAYER_NAME_KEY = "Keys"

STONE_PATH = "assets/tiles/stone_1.png"
WOOD_PATH = "assets/tiles/wood_1.png"
CAT_PATH = "assets/sprites/Cat_front.PNG"

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

        #Tilemap
        self.tile_map = None
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

        self.camera = arcade.Camera(self.window.width, self.window.height)

        #set up tilemap

        map_name = "assets/tilemaps/lvl1.json"

        layer_options = {
            LAYER_NAME_WALLS: {
                "use_spation_hash": True,
            },
            LAYER_NAME_KEY: {
                "use_spation_hash": True,
            },
            LAYER_NAME_DOORS: {
                "use_spation_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = arcade.Sprite(CAT_PATH, SPRITE_SCALING) #diff might be in scaling, check val
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        #Create physics engine

        self.physics_engine = PymunkPhysicsEngine(damping=0.7, gravity=(0,0))
        
        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("Player"),
            friction = 0.6,
            moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
            damping = 0.01,
            collision_type="player")

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(LAYER_NAME_WALLS),
            friction = 0.6,
            collision_type="wall",
            body_type = PymunkPhysicsEngine.STATIC)
        
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


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

        # Position the camera
        self.center_camera_to_player()


    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.camera.use()
        self.scene.draw()