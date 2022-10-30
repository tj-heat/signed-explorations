from typing import Tuple
from enum import Enum

import arcade

import src.dialogue.speech_items as Speech

class EventType(Enum):
    NONE        = 0
    MSG         = 1
    THOUGHT     = 2
    DIALOGUE    = 3
    WIN         = 4

class EventTrigger(arcade.Sprite):
    _collides = 1 # Trueian value for Pymunk reasons

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
    def collides(self) -> bool:
        return self._collides

    @property
    def task(self):
        return self._task

    @property
    def interactible(self) -> bool:
        return self._interactible

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


class ContactEventTrigger(EventTrigger):
    """ Works as an event trigger but without collision"""
    _collides = 0 # Falsian value for Pymunk reasons


class PassingEventTrigger(ContactEventTrigger):
    """ Works as a single event trigger but without collision"""

    @property
    def collides(self):
        self.kill()
        return super().collides

# Event Information
EVENT_TYPE = "type"
EVENT_MSGS = "msgs"
EVENT_MSG_SPEAKER = "speaker"
EVENT_PERSIST = "persistence"
EVENT_INTERACT = "interactible"

EVENT_DATA = {
    "door_locked": {
        EVENT_TYPE: EventType.DIALOGUE,
        EVENT_MSGS: [
            "The door's locked...",
            "I wonder what it says beside the door?"
        ],
        EVENT_PERSIST: SingleEventTrigger,
        EVENT_INTERACT: False,
        EVENT_MSG_SPEAKER: Speech.CAT_SPEAKER
    },
    "exit_locked": {
        EVENT_TYPE: EventType.DIALOGUE,
        EVENT_MSGS: [
            "Locked again...",
            "Maybe there's another key somewhere?"
        ],
        EVENT_PERSIST: SingleEventTrigger,
        EVENT_INTERACT: False,
        EVENT_MSG_SPEAKER: Speech.CAT_SPEAKER
    },
    "bridge_mid": {
        EVENT_TYPE: EventType.THOUGHT, 
        EVENT_MSGS: "L'appel du vide",
        EVENT_PERSIST: ContactEventTrigger,
        EVENT_INTERACT: False,
    },
    "marble_start": {
        EVENT_TYPE: EventType.THOUGHT,
        EVENT_MSGS: "Cold marble...",
        EVENT_PERSIST: ContactEventTrigger,
        EVENT_INTERACT: False,
        EVENT_MSG_SPEAKER: Speech.CAT_SPEAKER
    },
    "win" : {
        EVENT_TYPE: EventType.WIN, 
        EVENT_MSGS: ["win"],
        EVENT_PERSIST: SingleEventTrigger,
        EVENT_INTERACT: False,
    },
    "bounds": {
        EVENT_TYPE: EventType.DIALOGUE,
        EVENT_MSGS: ["I can't turn back. I'm not alive yet!"],
        EVENT_PERSIST: EventTrigger,
        EVENT_INTERACT: False,
        EVENT_MSG_SPEAKER: Speech.CAT_SPEAKER
    },
}