from typing import Optional

import arcade, math, threading
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

import src.actors.character as character
import src.actors.items as items
import src.views.pause_view as p
from src.actors.character import Task
import src.actors.items as items
from src.dialogue.dialogue_box import DialogueBox
from src.views.sign_view import SignView
from src.views.Book_view import BookView
from src.video.video_control import CAPTURING, display_video_t
from src.util.ring_buffer import RingBuffer
from src.util.thread_control import ThreadCloser, ThreadController
from src.video.video_control import CAPTURING, display_video_t

MOVEMENT_SPEED = 3

TILE_SCALING = 1
TILE_SIZE = 64
GRID_SIZE = TILE_SCALING * TILE_SIZE

SPRITE_SCALING = 0.3
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

PLAYER_MOVE_FORCE = 3000

RADIUS = 200.0

LAYER_WALLS = "Walls"
LAYER_LOW_WALLS = "Lower Walls"
LAYER_FLOOR = "Floor"
LAYER_DOORS = "Doors"
LAYER_ITEMS = "Items"
LAYER_CHARACTERS = "Characters"

TEXT_PATH = "assets/sprites/text_box.PNG"

class GameView(arcade.View):
    
    def __init__(self, cam_controller = None) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        #Tilemap
        self.tile_map = None
        self.scene = None
        self.player_sprite: Optional[character.Cat] = None
        self.dog_sprite: Optional[arcade.Sprite] = None
        self.npc_sprite: Optional[character.Dog] = None
        self.physics_engine: Optional[PymunkPhysicsEngine] = None

        # Player sprite
        self.player_sprite: Optional[arcade.Sprite] = None

        # Video capture
        self._cc = cam_controller

        self.camera = None
        self.gui_camera = None
        self._ui_manager = None
        self.lvl = 1

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

        #load necessary textures
        self.text_box = arcade.load_texture(TEXT_PATH)
    
    def setup(self):

        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()
        
        #set up tilemap
 
        map_name = "assets/tilemaps/tutorial/lvl1.json"
        layer_options = {
            LAYER_WALLS: {
                "use_spation_hash": True,
            },
            LAYER_ITEMS: {
                "use_spation_hash": True,
            },
            LAYER_DOORS: {
                "use_spation_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        # Create video capture display thread
        self._cam_buf = RingBuffer()
        print("d")
        self.video_t_closer = ThreadCloser()
        print("e")
        video_t = threading.Thread(
            target=display_video_t, 
            args=(self._cc, self._cam_buf, self.video_t_closer)
        )
        # Track the video thread and closer
        self._video_t = ThreadController(video_t, self.video_t_closer)
        print("f")
        if CAPTURING:
            print("g")
            self._video_t.start()

        #Create physics engine

        npc_layer = self.tile_map.object_lists[LAYER_CHARACTERS]

        for npc in npc_layer:
            cartesian = self.tile_map.get_cartesian(npc.shape[0], npc.shape[1])
            if npc.name == "Dog":
                body = character.Dog() 
                self.npc_sprite = body
                body.center_x = math.floor(cartesian[0] * TILE_SCALING * self.tile_map.tile_width)
                body.center_y = math.floor((cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING))
                self.dog_sprite = body
                self.scene.add_sprite(LAYER_CHARACTERS, body)
            elif npc.name == "Cat":
                self.player_sprite = character.Cat()
                self.player_sprite.center_x = math.floor(cartesian[0] * TILE_SCALING * self.tile_map.tile_width)
                self.player_sprite.center_y = math.floor((cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING))
                self.scene.add_sprite("Player", self.player_sprite)
            else: 
                raise Exception(f"Unknown npc type {npc.name}")

        item_layer = self.tile_map.object_lists[LAYER_ITEMS]
        for item in item_layer:
            cartesian = self.tile_map.get_cartesian(item.shape[0], item.shape[1])
            if item.name == "Key":
                body = items.Key()
            else:
                raise Exception (f"Unknown item type {item.name}")
            body.center_x = math.floor(cartesian[0] * TILE_SCALING * self.tile_map.tile_width)
            body.center_y = math.floor((cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING))

            self.scene.add_sprite(LAYER_ITEMS, body)

        self.physics_engine = PymunkPhysicsEngine(damping=2, gravity=(0,0))
        

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("Player"),
            friction = 0.6,
            moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
            damping = 0.01,
            collision_type = "player"
        )

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(LAYER_WALLS),
            friction = 0.6,
            collision_type = "wall",
            body_type = PymunkPhysicsEngine.STATIC
        )

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(LAYER_ITEMS),
            mass = 0.5,
            friction = 0.8,
            damping = 0.4,
            collision_type = "item"
        )

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(LAYER_CHARACTERS),
            friction = 0.6,
            moment_of_intertia = PymunkPhysicsEngine.MOMENT_INF,
            damping = 0.01,
            collision_type = "npc"
        )

        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(LAYER_DOORS),
            friction = 0.6,
            collision_type = "door",
            body_type = PymunkPhysicsEngine.STATIC
        )

        def npc_hit_handler(player_sprite, npc_sprite, _arbiter, _space, _data):
            player_sprite.touched = True
            npc_sprite.stop_follow()


        def item_hit_handler(npc_sprite, item_sprite, _arbiter, _space, _data):
            if npc_sprite.task == item_sprite.task:
                if npc_sprite.task == Task.KEY:
                    self.key_task(npc_sprite, item_sprite)

        def door_hit_handler(npc_sprite, door_sprite, _arbiter, _space, _data):
            if npc_sprite.task == Task.DOOR:
                self.door_task(npc_sprite, door_sprite)

        self.physics_engine.add_collision_handler("player", "npc", post_handler = npc_hit_handler)
        self.physics_engine.add_collision_handler("npc", "item", post_handler = item_hit_handler)
        self.physics_engine.add_collision_handler("npc", "door", post_handler = door_hit_handler)

        # Dialogue box object tracker
        self._dbox = None

    def key_task(self, npc, key):
        npc.inventory.append(f"{key.type}")
        key.remove_from_sprite_lists()
        npc.task = Task.DOOR

    def door_task(self, npc, door):
        door.remove_from_sprite_lists()
        npc.task = Task.NONE

        # Set up for dialogue options
        self._dbox = None

    def in_dialogue(self) -> bool:
        """ (bool) Returns True if the game is currently in dialogue. False
        otherwise.
        """
        return self._dbox and self._dbox.is_active()

    def check_items_in_radius(self):
        items = self.scene.get_sprite_list(LAYER_ITEMS).sprite_list
        nearby = []
        for i in items:
            x = self.player_sprite.center_x - i.center_x
            y = self.player_sprite.center_y - i.center_y
            if abs(x) < RADIUS and abs(y) < RADIUS:
                nearby.append(i)
        return nearby

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def move_player(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        force = (0,0)
        if self.up_pressed and not self.down_pressed:
            force = (0, PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force) #probably can just take this out of loop
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
        else:
            self.physics_engine.set_friction(self.player_sprite, 1.0)


        self.player_sprite.actual_force = force
        self.player_sprite.untouched()

    def move_dog(self):
        force = (0,0)
        if self.dog_sprite.follow == True:
            self.dog_sprite.set_goal((self.dog_sprite.center_x - self.player_sprite.center_x, 
                self.dog_sprite.center_y - self.player_sprite.center_y))
        elif self.dog_sprite.task == Task.KEY:
            items = self.check_items_in_radius()
            if len(items) == 0:
                self.dog_sprite.set_goal(0,0)
            else:
                 self.dog_sprite.set_goal((self.dog_sprite.center_x - items[0].center_x, 
                self.dog_sprite.center_y - items[0].center_y))
        
        if self.dog_sprite.follow == True or self.dog_sprite.task == Task.KEY:
            x, y = self.dog_sprite.goal
            if x < 0:
                force = (self.dog_sprite.force, 0)
                self.physics_engine.apply_force(self.dog_sprite, force)
            elif x > 0:
                self.dog_sprite.change_x = -self.dog_sprite.force
                force = (-self.dog_sprite.force, 0)
                self.physics_engine.apply_force(self.dog_sprite, force)
            if y > 0:
                force = (0, -self.dog_sprite.force)
                self.physics_engine.apply_force(self.dog_sprite, force)
            elif y < 0:
                force = (0, self.dog_sprite.force)
                self.physics_engine.apply_force(self.dog_sprite, force)
            
            self.dog_sprite.actual_force = force


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
        elif key == arcade.key.E:
            pass


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
        
        elif key == arcade.key.E:
            print("a")
            items = self.check_items_in_radius()
            # FIXME This will need to pass the proper information to the sign
            # view, rather than hardcoding the target.
            if self.player_sprite.is_touched() and len(items) != 0:
                print("b")
                sign_view = SignView(
                    self, 
                    self.npc_sprite, 
                    goal="VUS", 
                    task=Task.KEY
                )
                print("c")
                sign_view.setup()
                self.window.show_view(sign_view)
            else:
                self.dog_sprite.follow_cat()
                self.player_sprite.start_meow()
        
        elif key == arcade.key.I:
            book_view = BookView(self, self.npc_sprite)
            book_view.setup()
            self.window.show_view(book_view)
        
        elif key == arcade.key.ESCAPE:
            self.pause_video()
            pause = p.PauseView(self)
            pause.setup()
            self.window.show_view(pause)
        
        elif key == arcade.key.L:
            if not self._dbox:
                self._dbox = DialogueBox(
                    ["Hello", "there"], 
                    height=150, 
                    width=self.camera.viewport_width
                )
                self._ui_manager.add(self._dbox)
        
        elif key == arcade.key.SPACE:
            if self.in_dialogue():
                self._dbox.progress()

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        lvl_text = f"Level: {self.lvl}"
        arcade.draw_text(lvl_text, 10, 10, arcade.csscolor.WHITE, 18, 
            font_name="Kenney Mini Square" )
        
        self._ui_manager.draw()

        if self.player_sprite.cat_meowing():
            x = self.window.width/2
            y = self.window.height/2
            self.text_box.draw_scaled(
                center_x = x, 
                center_y = y,
                scale = SPRITE_SCALING * 2
                )
            arcade.draw_text(
                text = self.player_sprite.meow_text,
                font_size = 11,
                font_name="Kenney Mini Square",
                color = arcade.csscolor.BLACK,
                anchor_x = "center",
                start_x = x,
                start_y = y + (SPRITE_SIZE) - 30 #magic number generated through much trial and error
            )

    def on_update(self, delta_time):
        """ Movement and game logic """
        # TODO Change to a state-based system?
        if not self.in_dialogue():
            self.move_player()
            self.move_dog()

            if self.player_sprite.cat_meowing():
                self.player_sprite.meow_count -= 1
            if self.player_sprite.cat_meowing() and self.player_sprite.meow_count == 0:
                self.player_sprite.end_meow()

            #Update animation sprites
            self.scene.update_animation(delta_time, ["Player", LAYER_CHARACTERS])

            #Update physics engine
            self.physics_engine.step()

            # Position the camera
            self.center_camera_to_player()

        # Check for finished dialogue removal
        if self._dbox and not self._dbox.is_active():
                self._ui_manager.remove(self._dbox)
                self._dbox = None

    def resume_video(self):
        """ Resumes the video thread """
        self._video_t.closer.set_active()

    def pause_video(self):
        """ Pauses the video thread """
        self._video_t.closer.set_inactive()

    def end_video(self):
        """ Stops the video thread """
        # Check if the video paused
        if not self._video_t.closer.is_active():
            self.resume_video()

        # Wait for thread to finish   
        self._video_t.finish()