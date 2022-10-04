from typing import Tuple
from enum import Enum

import arcade

class EventType(Enum):
    NONE    = 0
    MSG     = 1 

EVENT_DATA = {
    "door_a": {
        "type": EventType.MSG, 
        "msgs": ["The door's locked..."]
    },
}

class EventTrigger(arcade.Sprite):   
    def __init__(self, width, height, task, debug=False) -> None:
        super().__init__(
            image_width=width, 
            image_height=height, 
            texture=None
        )
        
        self.hit_box = EventTrigger.calc_relative_bbox(width, height)
        self._task = task
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