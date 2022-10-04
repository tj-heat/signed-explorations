from typing import Tuple

import arcade

TEST_PATH = "assets/tilemaps/tutorial/textures/testing.png"

class EventTrigger(arcade.Sprite):   
    def __init__(self, width, height, task, debug = True) -> None:
        # Construct sprite
        super().__init__(
            image_width=width, 
            image_height=height, 
            texture=None
        )
        if debug:
            texture = arcade.Texture.create_filled(
                f"FILLED_EVENT_{self.guid}", 
                [width, height], 
                color=arcade.color.BLUE
            )
            self.texture = texture

        self.hit_box = EventTrigger.calc_relative_bbox(width, height)
        self._task = task

    @staticmethod
    def calc_relative_bbox(width, height) -> Tuple["Point"]:
        """ Calculates the points needed for a relative bounding box, based on 
        width and height.
        """
        x, y, = (width / 2, height / 2)

        return ((-x, -y), (x, -y), (x, y), (-x, y))