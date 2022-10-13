from typing import Tuple
from enum import Enum

import arcade

class EventType(Enum):
    NONE    = 0
    MSG     = 1 

class EventTrigger(arcade.Sprite):   
    def __init__(
        self, 
        width, 
        height, 
        task, 
        interactible=False, 
        debug=False
    ) -> None:
        """ Constructs an event trigger. Event triggers are invisible blocks of
        a given width and height that on collision or interaction perform a 
        task.
        
        When in debug mode an event trigger will show as a blue rectangle.
        """
        super().__init__(
            image_width=width, 
            image_height=height, 
            texture=None
        )
        
        self.hit_box = EventTrigger.calc_relative_bbox(width, height)
        self._task = task
        self._interactible = interactible

        self._debug = debug

        # Conditionally construct
        self._d_texture = arcade.Texture.create_filled(
            f"FILLED_EVENT_{self.guid}", 
            [width, height], 
            color=arcade.color.BLUE
        )

        if self._debug:
            self.set_debug_texture()

    def set_none_texture(self):
        self.texture = None

    def set_debug_texture(self):
        self.texture = self._d_texture

    def update_texture(self):
        if self._debug:
            self.set_debug_texture()
        else:
            self.set_none_texture()

    def set_debug(self):
        self._debug = True
        self.update_texture()

    def clear_debug(self):
        self._debug = False
        self.update_texture()

    @property
    def task(self):
        return self._task

    @property
    def interactible(self) -> bool:
        return self.interactible

    @staticmethod
    def calc_relative_bbox(width, height) -> Tuple["Point"]:
        """ Calculates the points needed for a relative bounding box, based on 
        width and height.
        """
        x, y, = (width / 2, height / 2)

        return ((-x, -y), (x, -y), (x, y), (-x, y))

class SingleEventTrigger(EventTrigger):
    @property
    def task(self):
        self.kill()
        return self._task

# Event Information
EVENT_TYPE = "type"
EVENT_MSGS = "msgs"
EVENT_PERSIST = "persistence"
EVENT_INTERACT = "interactible"

EVENT_DATA = {
    "door_locked": {
        "type": EventType.MSG, 
        "msgs": ["The door's locked..."],
        "persistence": SingleEventTrigger,
    },
}