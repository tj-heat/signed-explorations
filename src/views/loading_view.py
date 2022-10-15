import arcade

from src.views.menu_view import MenuView

BACKGROUND_PATH = "assets/backgrounds/"

class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.background = arcade.load_texture(BACKGROUND_PATH + "placeholder_start_menu.jpg")

    def setup(self):
        """Set up screen here"""
        pass

    def on_draw(self):
        """Render screen"""
        self.clear()

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, key, modifiers):
        menu = MenuView()
        menu.setup()
        self.window.show_view(menu)