import arcade
from arcade.pymunk_physics_engine import PymunkPhysicsEngine
import character
import math
from typing import Optional

MOVEMENT_SPEED = 3

TILE_SCALING = 1
TILE_SIZE = 62
GRID_SIZE = TILE_SCALING * TILE_SIZE

PLAYER_START_X = 124
PLAYER_START_Y = 124

PLAYER_MOVE_FORCE = 3000

LAYER_NAME_WALLS = "Walls"
LAYER_NAME_NO_PHYS_WALLS = "Lower Walls"
LAYER_NAME_FLOOR = "Floor"
LAYER_NAME_DOORS = "Doors"
LAYER_NAME_KEY = "Key"
LAYER_NAME_CHARACTERS = "Characters"

STONE_PATH = "assets/tiles/stone_1.png"
WOOD_PATH = "assets/tiles/wood_1.png"

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

        #Tilemap
        self.tile_map = None
        self.scene = None
        self.player_sprite: Optional[arcade.Sprite] = None
        self.physics_engine = None

                # Player sprite
        self.player_sprite: Optional[arcade.Sprite] = None

        # Sprite lists we need
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None

        self.camera = None
        self.gui_camera = None
        self.lvl = 1

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    
    def setup(self):

        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

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

        #self.wall_list = self.tile_map.sprite_lists[LAYER_NAME_WALLS]
        #self.item_list = self.tile_map.sprite_lists[LAYER_NAME_KEY]


        self.player_sprite = character.Cat()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)
        #self.player_list.append(self.player_sprite)

        npc_layer = self.tile_map.object_lists[LAYER_NAME_CHARACTERS]

        #Create physics engine

        for npc in npc_layer:
            cartesian = self.tile_map.get_cartesian(npc.shape[0], npc.shape[1])
            if npc.name == "Dog":
                body = character.Dog() 
            else: 
                raise Exception(f"Unknown npc type {npc.name}")
            body.center_x = math.floor(cartesian[0] * TILE_SCALING * self.tile_map.tile_width)
            body.center_y = math.floor((cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING))

            """
            if "boundary_left" in npc.properties:
                body.boundary_left = npc.properties["boundary_left"]
            if "boundary_right" in npc.properties:
                body.boundary_left = npc.properties["boundary_right"]
            if "boundary_top" in npc.properties:
                body.boundary_left = npc.properties["boundary_top"]
            if "boundary_bottom" in npc.properties:
                body.boundary_left = npc.properties["boundary_bottom"]
            """

            self.scene.add_sprite(LAYER_NAME_CHARACTERS, body)
            

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

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(LAYER_NAME_KEY),
            mass = 0.5,
            friction = 0.8,
            damping = 0.4,
            collision_type = "rock")

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(LAYER_NAME_CHARACTERS),
            friction = 0.6,
            moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
            damping = 0.01,
            collision_type="npc"
        )
        
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

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


    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        lvl_text = f"Level: {self.lvl}"
        arcade.draw_text(lvl_text, 10, 10, arcade.csscolor.WHITE, 18)


    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        force = (0,0)

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

        self.player_sprite.actual_force = force
        self.scene.update_animation(delta_time, ["Player", LAYER_NAME_CHARACTERS])

        """
        for npc in self.scene[LAYER_NAME_CHARACTERS]:
            if (
                npc.boundary_right 
                and npc.right > npc.boundary_right
                and npc.
            )
        """

        self.physics_engine.step()

        # Position the camera
        self.center_camera_to_player()
