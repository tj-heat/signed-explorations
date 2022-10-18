from copyreg import constructor
from typing import List, Optional

import arcade, bisect, math, threading
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

import src.actors.character as character
import src.actors.items as items
import src.views.pause_view as p
import src.views.end_view as w
import src.dialogue.speech_items as Speech
from src.actors.event_triggers import *
from src.actors.character import Task
from src.actors.interactibles import INTERACTIBLES, Interactible
from src.dialogue.dialogue_box import DialogueBox
from src.util.ring_buffer import RingBuffer
from src.util.thread_control import ThreadCloser, ThreadController
from src.views.book_view import BookView
from src.views.focus_view import FocusView
from src.views.sign_view import SignView
from src.video.video_control import CAPTURING, CameraControl, display_video_t

MOVEMENT_SPEED = 3

TILE_SCALING = 1
TILE_SIZE = 64
GRID_SIZE = TILE_SCALING * TILE_SIZE

SPRITE_SCALING = 0.3 #must match what is in character.py
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

PLAYER_MOVE_FORCE = 3000

RADIUS = 200.0

LAYER_WALLS = "Walls"
LAYER_LOW_WALLS = "Lower Walls"
LAYER_FLOOR = "Floor"
LAYER_DOORS = "Doors"
LAYER_ITEMS = "Items"
LAYER_EVENTS = "Events"
LAYER_INTERACTS = "Interactibles"
LAYER_CHARACTERS = "Characters"
LAYER_EDGES = "Edges"

TEXT_PATH = "assets/ui/text_box.PNG"
ICON_PATH = "assets/ui/interact_icon.PNG"

UP_KEYS = (arcade.key.UP, arcade.key.W)
DOWN_KEYS = (arcade.key.DOWN, arcade.key.S)
LEFT_KEYS = (arcade.key.LEFT, arcade.key.A)
RIGHT_KEYS = (arcade.key.RIGHT, arcade.key.D)
MOVE_KEYS = (*UP_KEYS, *DOWN_KEYS, *LEFT_KEYS, *RIGHT_KEYS)

class GameView(arcade.View):
    
    def __init__(self, cam_controller = None) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        #Tilemap
        self.tile_map = None
        self.scene = None
        self.player_sprite: Optional[character.Cat] = None
        self.dog_sprite: Optional[character.Dog] = None
        self.physics_engine: Optional[PymunkPhysicsEngine] = None

        # Player sprite
        self.player_sprite: Optional[arcade.Sprite] = None

        # Video capture 
        self._cc = cam_controller

        self.camera = None
        self.gui_camera = None
        self._ui_manager = None
        self.lvl = 1

        # Control variables
        self._done_tutorial = False

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

        #load necessary textures
        self.text_box = arcade.load_texture(TEXT_PATH)
        self.interact_icon = arcade.load_texture(ICON_PATH)
    
    @property
    def cam_controller(self) -> CameraControl:
        return self._cc

    def setup(self):
        # Control variables
        self._seen_key = False

        # Visual system
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()
        
        #set up tilemap
 
        map_name = "assets/tilemaps/lvl1.tmx"
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
            LAYER_EVENTS: {
                "use_spation_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #self.scene.add_sprite_list_after("Player", LAYER_DOORS)

        # Create video capture display thread
        self._cam_buf = RingBuffer()
        self.video_t_closer = ThreadCloser()
        video_t = threading.Thread(
            target=display_video_t, 
            args=(self._cc, self._cam_buf, self.video_t_closer)
        )
        # Track the video thread and closer
        self._video_t = ThreadController(video_t, self.video_t_closer)
        if CAPTURING:
            self._video_t.start()

        ### Create physics engine
        # Create Sprites
        npc_layer = self.tile_map.object_lists[LAYER_CHARACTERS]
        for npc in npc_layer:
            cartesian = self.tile_map.get_cartesian(npc.shape[0], npc.shape[1])
            if npc.name == "Dog":
                body = character.Dog() 
                body.center_x, body.center_y = \
                    self.get_center_from_cartesian(cartesian)
                self.dog_sprite = body
                self.scene.add_sprite(LAYER_CHARACTERS, body)
            elif npc.name == "Cat":
                self.player_sprite = character.Cat()
                self.player_sprite.center_x, self.player_sprite.center_y = \
                    self.get_center_from_cartesian(cartesian)
                self.scene.add_sprite("Player", self.player_sprite)
            else: 
                raise Exception(f"Unknown npc type {npc.name}")

        item_layer = self.tile_map.object_lists[LAYER_ITEMS]
        for item in item_layer:
            cartesian = self.tile_map.get_cartesian(item.shape[0], item.shape[1])
            if item.name == "Key":
                body = items.Key()
                body.center_x, body.center_y = \
                    self.get_center_from_cartesian(cartesian)

                self.scene.add_sprite(LAYER_ITEMS, body)
            else:
                raise Exception (f"Unknown item type {item.name}")

        door_layer = self.tile_map.object_lists[LAYER_DOORS]
        for door in door_layer:
            x, y = door.shape[3]
            cartesian = self.tile_map.get_cartesian(x, y)
            y2 = (cartesian[1] + self.tile_map.height) % self.tile_map.height
            info = door.name.split("_")
            if len(info) != 5:
                body = items.Door("orthogonal", "Key", "n", "n", "-1")
            else:
                body = items.Door(info[0], info[1], info[2], info[3], info[4])
            body.center_x = math.floor((cartesian[0] + 0.5) * TILE_SCALING * self.tile_map.tile_width)
            body.center_y = math.floor((y2 + 0.5) * (self.tile_map.tile_height * TILE_SCALING))

            self.scene.add_sprite(LAYER_DOORS, body)

        self._create_interactibles()
        self._create_events(self.tile_map.object_lists[LAYER_EVENTS])

        # Create the physics engine and register collisions
        self.physics_engine = PymunkPhysicsEngine(damping=2, gravity=(0,0))
        self._add_physics_to_sprites()
        self._register_colliders()

        # Dialogue box object tracker
        self._dbox = []
        self._in_dialogue = False

        # Event tracker
        self._in_event = False

        # View tracker
        self._upcoming_views = []

        # Key press notifier
        self._notify_interaction = False

    def _create_interactibles(self):
        """ Load all of the interactibles into the game """
        interactibles = self.tile_map.object_lists[LAYER_INTERACTS]

        for interactible in interactibles:           
            x, y = interactible.shape
            cartesian = self.tile_map.get_cartesian(x, y)
            cartesian = cartesian[0], \
                (cartesian[1] + self.tile_map.height) % self.tile_map.height
            
            # Create instance of interactible
            obj_constructor = INTERACTIBLES.get(interactible.name)
            body = obj_constructor(self.tile_map.tile_width)
            body.set_center(*self.get_center_from_cartesian(cartesian))

            self.scene.add_sprite(LAYER_INTERACTS, body)

    def _add_physics_to_sprites(self):
        """ Add all of the sprites to the physics engine. """
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("Player"),
            friction = 0.6,
            moment_of_intertia=PymunkPhysicsEngine.MOMENT_INF,
            damping = 0.01,
            collision_type = "player"
        )

        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_WALLS),
            friction = 0.6,
            collision_type = "wall",
            body_type = PymunkPhysicsEngine.STATIC
        )

        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_ITEMS),
            mass = 0.5,
            friction = 0.8,
            damping = 0.4,
            collision_type = "item"
        )

        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_CHARACTERS),
            friction = 0.6,
            moment_of_intertia = PymunkPhysicsEngine.MOMENT_INF,
            damping = 0.01,
            collision_type = "npc"
        )

        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_EDGES),
            friction = 0.6,
            collision_type = "wall",
            body_type = PymunkPhysicsEngine.STATIC
        )

        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_EVENTS),
            friction = 0.6,
            collision_type = "event",
            body_type = PymunkPhysicsEngine.STATIC
        )
        
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_DOORS),
            friction = 0.6,
            collision_type = "door",
            body_type = PymunkPhysicsEngine.STATIC
        )
        
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(LAYER_INTERACTS),
            friction = 0.6,
            collision_type = "interact",
            body_type = PymunkPhysicsEngine.STATIC
        )

    def _register_colliders(self):
        """ Register all of the collisions in the game, with the physics engine.
        """
        def npc_hit_handler(player_sprite, npc_sprite, _arbiter, _space, _data):
            npc_sprite.stop_follow()
            player_sprite.touched = True
            npc_sprite.talk = True
            self.start_interact_notify()
            return player_sprite.touched
            #ADD AS PREHANDLER

        def npc_separate_handler(player_sprite, npc_sprite, _arbiter, _space, _data):
            player_sprite.touched = False
            npc_sprite.talk = False
            self.end_interact_notify()

        def item_hit_handler(npc_sprite, item_sprite, _arbiter, _space, _data):
            if npc_sprite.task == item_sprite.task:
                if npc_sprite.task == Task.KEY:
                    self.key_task(npc_sprite, item_sprite)

        def door_hit_handler(npc_sprite, door_sprite, _arbiter, _space, _data):
            return self.door_task(npc_sprite, door_sprite)

        def event_hit_handler(_p, event_sprite, _a, _s, _d):
            # NOTE This might be needed later
            # if self.event_possible(event_sprite):
            #     event_sprite.task()
            self.start_event()

        def event_hit_pre_handler(_p, event_sprite, _a, _s, _d):
            # Interactible events should not activate on collide
            if self.event_possible(event_sprite) \
                    and not event_sprite.interactible:
                event_sprite.task()

            return event_sprite.collides

        def event_collider_checker(_sprite, event, _a, _s, _d):
            return event.collides

        def event_hit_separate_handler(_p, _e, _a, _s, _d):
            self.end_event()

        def player_near_item_handler(_player_sprite, _event_sprite, _arbiter, _space, _data):
            self.start_interact_notify()

        def player_leave_item_handler(_player_sprite, _event_sprite, _arbiter, _space, _data):
            self.end_interact_notify()

        def non_handler(_n, _e, _a, _s, _d):
            """ Collision pre handler that will cause no collisions to occur """
            return 0 # Falsian value

        self.physics_engine.add_collision_handler(
            "player", "event",
            pre_handler=event_hit_pre_handler,
            post_handler=event_hit_handler, 
            separate_handler=event_hit_separate_handler
        )
        
        self.physics_engine.add_collision_handler(
            "player", "item", 
            post_handler=player_near_item_handler, 
            separate_handler=player_leave_item_handler
        )

        self.physics_engine.add_collision_handler(
            "player", "interact", 
            post_handler=player_near_item_handler, 
            separate_handler=player_leave_item_handler
        )

        self.physics_engine.add_collision_handler(
            "player", "npc", 
            begin_handler= npc_hit_handler, 
            separate_handler = npc_separate_handler)

        self.physics_engine.add_collision_handler("npc", "item", post_handler = item_hit_handler)
        self.physics_engine.add_collision_handler("npc", "door", begin_handler = door_hit_handler)
        self.physics_engine.add_collision_handler("npc", "event", pre_handler = non_handler)
        self.physics_engine.add_collision_handler("item", "event", pre_handler = event_collider_checker)

    def event_possible(self, event) -> bool:
        """ Check if a given event can go ahead """
        return event.task and not self._in_event

    def key_task(self, npc, key):
        npc.inventory.append(f"{key.type}")
        key.remove_from_sprite_lists()
        npc.task = Task.DOOR

    def door_task(self, npc : character.Dog, door : items.Door):
        if door.key == "Key" and "Key" in npc.inventory:
            npc.inventory.remove("Key")
            self.npc_opens_door(door)
        
        if "Key" not in npc.inventory:
            npc.task = Task.NONE
        
        return True

    def create_dbox(self, text, speaker=None) -> DialogueBox:
        """ Create a dialogue box instance """
        return DialogueBox(
            text=text, 
            width=self.camera.viewport_width, 
            speaker=speaker
        )

    def register_dialogue(self, dbox: DialogueBox) -> None:
        """ Keep track of a given dialogue box. """
        self._dbox.append(dbox)

    def enable_dialogue(self, dbox: DialogueBox) -> None:
        """ Display a given dialogue box in the UI manager and flag dialogue """
        self._in_dialogue = True
        self._ui_manager.add(dbox)

    def disable_dialogue(self, dbox: DialogueBox) -> None:
        """ End dialogue being tracked and remove the dialogue box """
        self._in_dialogue = False
        self._ui_manager.remove(dbox)
        self._dbox.remove(dbox)

    def queue_new_view(self, view: arcade.View) -> None:
        """ Schedule a new view to show when available. This should only be used
        to show views after events or dialogue. """
        self._upcoming_views.append(view)

    def npc_opens_door(self, door : items.Door):
        if door.dual_pos == "n":
            self.door_physics_change(door)
        else:
            all_doors = self.scene.get_sprite_list(LAYER_DOORS).sprite_list
            for d in all_doors:
                if d.door_num == door.door_num and d.dual_pos != door.dual_pos :
                    self.door_physics_change(d)
                    self.door_physics_change(door)             

    def door_physics_change(self, door):
        door.open_door()
        self.physics_engine.remove_sprite(door)
        self.dog_sprite.task = Task.NONE

    @property
    def current_dbox(self) -> DialogueBox:
        """ Returns the current dialogue box """
        return self._dbox[0]

    def in_dialogue(self) -> bool:
        """ (bool) Returns True if the game is currently in dialogue. False
        otherwise.
        """
        return self._in_dialogue

    def start_event(self) -> None:
        """ Flag that the game is in an event """
        self._in_event = True

    def end_event(self) -> None:
        """ Flag that the game is no longer in an event """
        self._in_event = False

    def start_interact_notify(self):
        """ Begin informing the player that they can interact with something """
        self._notify_interaction = True

    def end_interact_notify(self):
        """ Stop informing the player that they can interact with something """
        self._notify_interaction = False

    def check_items_in_radius(
        self, 
        x_range: int = 96, 
        y_range: int = 96
    ) -> List[arcade.Sprite]:
        return self.check_in_range(LAYER_ITEMS, x_range, y_range)

    def check_events_in_radius(
        self, 
        x_range: int = 96, 
        y_range: int = 96
    ) -> List[EventTrigger]:
        """ Check for interactible events in a given radius around the player """
        events = self.check_in_range(LAYER_EVENTS, x_range, y_range)
        return list(filter(lambda e: e.interactible, events))

    def check_objects_in_radius(
        self, 
        x_range: int = 96, 
        y_range: int = 128
    ) -> List[Interactible]:
        """ Check for interactible objects in a given radius around the player. 
        """
        return self.check_in_range(LAYER_INTERACTS, x_range, y_range)

    def check_in_range(
        self, 
        layer: str, 
        x_range: int, 
        y_range: int
    ) -> List[arcade.Sprite]:
        """ Check for all sprites on a given layer within a provided radius """
        sprites = self.scene.get_sprite_list(layer).sprite_list
        nearby = []

        for sprite in sprites:
            dx = abs(self.player_sprite.center_x - sprite.center_x)
            dy = abs(self.player_sprite.center_y - sprite.center_y)

            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dx < x_range and dy < y_range:
                # Insert sorted by distance
                bisect.insort(nearby, (sprite, dist), key=lambda s: s[1])

        # Return only the sprites (still sorted)
        if nearby:
            nearby, _ = zip(*nearby)
            nearby = list(nearby)
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

    def move_dog(self):
        force = (0,0)
        if self.dog_sprite.follow == True:
            self.dog_sprite.set_goal((self.dog_sprite.center_x - self.player_sprite.center_x, 
                self.dog_sprite.center_y - self.player_sprite.center_y))
        elif self.dog_sprite.task == Task.KEY:
            items = self.check_items_in_radius()
            if len(items) == 0:
                pass
            else:
                self.dog_sprite.set_goal((self.dog_sprite.center_x - items[0].center_x, 
                self.dog_sprite.center_y - items[0].center_y))
        
        if (self.dog_sprite.follow == True or self.dog_sprite.task != Task.NONE):
            x, y = self.dog_sprite.goal
            if y > 0:
                force = (0, -self.dog_sprite.force)
            elif y < 0:
                force = (0, self.dog_sprite.force)
            
            self.physics_engine.apply_force(self.dog_sprite, force)
            if abs(y) > abs(x):
                self.dog_sprite.actual_force = force
           
            if x < 0:
                force = (self.dog_sprite.force, 0)
            elif x > 0:
                force = (-self.dog_sprite.force, 0)

            self.physics_engine.apply_force(self.dog_sprite, force)
            if abs(x) > abs(y):
                self.dog_sprite.actual_force = force
        
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key in UP_KEYS:
            self.up_pressed = True
        elif key in DOWN_KEYS:
            self.down_pressed = True
        elif key in LEFT_KEYS:
            self.left_pressed = True
        elif key in RIGHT_KEYS:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key in UP_KEYS:
            self.up_pressed = False
        elif key in DOWN_KEYS:
            self.down_pressed = False
        elif key in LEFT_KEYS:
            self.left_pressed = False
        elif key in RIGHT_KEYS:
            self.right_pressed = False
        
        elif key == arcade.key.E:
            processed = False # Could replace with if/else for performance hit

            items = self.check_items_in_radius()
            if items and not processed:
                if self.do_item_interact(items):
                    processed = True # Stop additional processing

            events = self.check_events_in_radius()
            if events and not processed:
                event = events[0]
                event.task()

                # Remove the event once it has been interacted with
                if isinstance(event, ContactEventTrigger):
                    event.kill()
                processed = True

            interactibles = self.check_objects_in_radius()
            if interactibles and not processed:
                self.do_object_interact(interactibles)

            if self.dog_sprite.talk and not processed:
                self.talk_to_dog()
                processed = True
        
        elif key == arcade.key.Q:
            if not self.in_dialogue():
                self.dog_sprite.follow_cat()
                self.player_sprite.start_meow(25)
        
        elif key == arcade.key.I:
            book_view = BookView(self, self.dog_sprite)
            book_view.setup()
            self.window.show_view(book_view)
        
        elif key == arcade.key.ESCAPE:
            self.pause_video()
            pause = p.PauseView(self)
            pause.setup()
            self.window.show_view(pause)
        
        elif key == arcade.key.SPACE:
            if self.in_dialogue():
                self.current_dbox.progress()

    def talk_to_dog(self):
        self.register_dialogue(self.create_dbox(self.dog_sprite.get_dialogue(), Speech.DOG_SPEAKER))
    
    def do_item_interact(self, interactibles: List[arcade.Sprite]):
        """ Handle the interactions of the player character with items """
        target = interactibles[0]
        retval = False

        # Check for signing action first
        if self.player_sprite.is_touched():
            if target.type == "Key":
                goal = "KEY"
                task = Task.KEY
            
                # FIXME to be more generic this should only fire for signables
                sign_view = SignView(self, self.dog_sprite, goal, task, target)
                sign_view.setup()
                self.window.show_view(sign_view)
                retval = True

        # If not signing then process as normal
        elif isinstance(target, items.Key):
            if self._seen_key:
                self.register_dialogue(self.create_dbox(
                    Speech.get_msgs(Speech.PUZZLE_INTERACT)
                ))
            else:
                self._seen_key = True
                msgs, speaker = Speech.get_dialogue(Speech.KEY_FIRST)
                self.register_dialogue(self.create_dbox(msgs, speaker))
            retval = True

        return retval

    def do_object_interact(self, interactibles: List[Interactible]):
        """ Handle the interactions of the player character with objects """
        target = interactibles[0]

        pre_msgs = target.get_pre_msgs()
        post_msgs = target.get_post_msgs()
        focus_texture = target.get_focus_texture()

        if pre_msgs:
            self.register_dialogue(self.create_dbox(
                pre_msgs, Speech.CAT_SPEAKER
            ))
            self.enable_dialogue(self.current_dbox)

        if post_msgs:
            self.register_dialogue(self.create_dbox(
                post_msgs, Speech.CAT_SPEAKER
            ))

        if focus_texture:
            focus_view = FocusView(self, focus_texture)
            self.queue_new_view(focus_view)

    def draw_interact_symbol(self) -> None:
        """ Draws a symbol showing the interact key """
        x, y = self.window.width / 2, self.window.height / 2
        
        self.interact_icon.draw_scaled(
            center_x = x, 
            center_y = y,
            scale = SPRITE_SCALING * 2
        )
        arcade.draw_text(
            text = "E",
            font_size = 18,
            font_name="Kenney Mini Square",
            color = arcade.csscolor.BLACK,
            anchor_x = "center",
            start_x = x - (SPRITE_SIZE / 2) - 2,
            start_y = y + (SPRITE_SIZE / 2) - 21 #magic number
        )

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

        if self._notify_interaction:
            self.draw_interact_symbol()

        if self.player_sprite.cat_meowing():
            x = self.window.width/2
            y = self.window.height/2
            self.text_box.draw_scaled(
                center_x = x, 
                center_y = y,
                scale = SPRITE_SCALING * 2.5
                )
            arcade.draw_text(
                text = self.player_sprite.meow_text,
                font_size = 13,
                font_name="Kenney Mini Square",
                color = arcade.csscolor.BLACK,
                anchor_x = "center",
                start_x = x,
                start_y = y + (SPRITE_SIZE) - 17 #magic number generated through much trial and error
            )

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Check for finished dialogue for removal
        if self._in_dialogue and not self.current_dbox.is_active():
            self.disable_dialogue(self.current_dbox)

        # If a new view should be shown, do so
        if self._upcoming_views and not self.in_dialogue():
            self.window.show_view(self._upcoming_views.pop(0))

        # If a dbox is scheduled, display it and set dialogue on
        if self._dbox and self.current_dbox.is_active() and \
            not self.in_dialogue():
            self.enable_dialogue(self.current_dbox)

        if not self.in_dialogue():
            self.move_player()
            self.move_dog()

            # Check for nearby events
            if self.check_events_in_radius():
                self.start_interact_notify
            else:
                self.end_interact_notify

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

    def on_show_view(self):
        self.center_camera_to_player()
        if not self._done_tutorial:
            # System message
            self.register_dialogue(self.create_dbox(
                Speech.DIALOGUE_INTRODUCTION_P1[Speech.MSGS]
            ))
            # Dog message
            p2_msg = Speech.DIALOGUE_INTRODUCTION_P2[Speech.MSGS]
            p2_speaker = Speech.DIALOGUE_INTRODUCTION_P2[Speech.SPEAKER]
            self.register_dialogue(self.create_dbox(p2_msg, p2_speaker))
            self._done_tutorial = True
        
        return super().on_show_view()

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

    def _create_events(self, event_layer):
        map_height = self.tile_map.height * self.tile_map.tile_height

        for event in event_layer:
            # Calculate geometries
            tl, tr, br, bl = \
                [(x, (y + map_height) % map_height) for x, y in event.shape]
            width, height = (int(br[0] - tl[0]), int(tl[1] - br[1]))
            mid_x, mid_y = (tl[0] + width // 2, tl[1] - height // 2)
            
            # Look for event
            event_data = EVENT_DATA.get(event.name, EventType.NONE)
            if event_data == EventType.NONE:
                raise Exception (f"Unknown item type {event.name}")

            # Create task
            event_type = event_data[EVENT_TYPE]
            if event_type == EventType.MSG:
                speaker = None
                def task(msg, speaker=None):
                    # Return lambda to force evaluation and get around closure                   
                    return lambda: self.register_dialogue(self.create_dbox(msg))
            
            elif event_type == EventType.THOUGHT:
                speaker = None
                def task(msg, speaker=None):
                    return lambda: self.player_sprite.start_meow(25, msg)

            elif event_type == EventType.DIALOGUE:
                speaker = event_data[EVENT_MSG_SPEAKER]
                def task(msg, speaker):
                    return lambda: self.register_dialogue(
                        self.create_dbox(msg, speaker)
                    )
            
            elif event_type == EventType.WIN:
                speaker = None
                def task(msg, speaker=None):
                    return lambda: self.endgame()

            # Create event
            body = event_data[EVENT_PERSIST](
                width=width, 
                height=height, 
                task=task(msg=event_data[EVENT_MSGS], speaker=speaker),
                interactible=event_data[EVENT_INTERACT],
            )

            # Add event to scene
            body.center_x, body.center_y = mid_x, mid_y
            self.scene.add_sprite(LAYER_EVENTS, body)

    def endgame(self):
        win_view = w.EndView(self)
        win_view.setup()
        self.window.show_view(win_view)

    def get_center_from_cartesian(self, cartesian: Tuple[int]) -> Tuple[float]:
        """ Get the center position of a given cartesian"""
        x = int((cartesian[0] + 0.5) * TILE_SCALING * self.tile_map.tile_width)
        y = int((cartesian[1] + 0.5) * TILE_SCALING * self.tile_map.tile_height)
        
        return (x, y)
