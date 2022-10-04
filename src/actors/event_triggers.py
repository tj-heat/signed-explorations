import arcade

TEST_PATH = "assets/tilemaps/tutorial/textures/testing.png"

class EventTrigger(arcade.Sprite):   
    def __init__(self, width, height, task) -> None:
        texture = arcade.Texture.create_empty("EMPTY", [width, height])
        super().__init__(image_width=width, image_height=height, texture=None)
        self.hit_box = texture.hit_box_points

        print(self.hit_box)
        self.draw_hit_box()
        self._task = task