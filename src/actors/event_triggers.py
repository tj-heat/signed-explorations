from typing import Tuple

import arcade

TEST_PATH = "assets/tilemaps/tutorial/textures/testing.png"

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

    @staticmethod
    def calc_relative_bbox(width, height) -> Tuple["Point"]:
        """ Calculates the points needed for a relative bounding box, based on 
        width and height.
        """
        x, y, = (width / 2, height / 2)

        return ((-x, -y), (x, -y), (x, y), (-x, y))