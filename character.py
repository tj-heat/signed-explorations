import arcade

SPRITE_SCALING = 0.3
SPRITE_IMAGE_SIZE = 250
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)
CAT_PATH = "assets/sprites/cat/Cat_"

FRONT_FACING = 0
BACK_FACING = 1
RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Animal(arcade.Sprite):
    def __init__(self, path):
        super().__init__()

        self.cur_texture= 0
        self.scale = SPRITE_SCALING

        #texture 0 is right facing
        self.side_texture_pair = load_texture_pair(f"{path}side.PNG")
        #texture 0 is front
        self.front_texture_pair = [arcade.load_texture(f"{path}front.PNG"),
                                    arcade.load_texture(f"{path}back.PNG")]

        self.texture = self.front_texture_pair[0]

        self.hit_box = self.texture.hit_box_points

        self.actual_force = (0,0)

    def update_animation(self, delta_time: float = 1 / 60):
        x, y = self.actual_force
        if x < 0:
            self.texture = self.side_texture_pair[LEFT_FACING]
        if x > 0:
            self.texture = self.side_texture_pair[RIGHT_FACING]
        if y > 0:
            self.texture = self.front_texture_pair[BACK_FACING]
        if y < 0:
            self.texture = self.front_texture_pair[FRONT_FACING]
        if x == 0 and y == 0:
            self.texture = self.front_texture_pair[FRONT_FACING]
        return

class Cat(Animal):
    def __init__(self):
        super().__init__(CAT_PATH)