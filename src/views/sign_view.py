import arcade

class SignView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        arcade.draw_text("This is the sign language interaction, for now press any key to return to the game", 10, 10, arcade.csscolor.WHITE, 18)

    
    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)
