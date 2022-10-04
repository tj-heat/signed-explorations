import arcade

TEST_PATH = "assets/tilemaps/tutorial/textures/testing.png"

class EventTrigger(arcade.Sprite):
    # def __init__(self, width, height, task) -> None:
    #     super().__init__()

    #     self.type = "Event"
    #     self.texture = arcade.load_texture(TEST_PATH)
    #     self.hit_box = self.texture.hit_box_points
    
    def __init__(self, width, height, task) -> None:
        texture = arcade.Texture.create_empty("EMPTY", [64, 64])
        super().__init__(image_width=width, image_height=height)
        self.hit_box = texture.hit_box_points
        print(self.hit_box)

        self._width = width
        self._height = height
        self._task = task