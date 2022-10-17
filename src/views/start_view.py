import arcade

from src.views.loading_view import LoadingView 

BACKGROUND_PATH = "assets/backgrounds/"

class StartView(arcade.View):
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
        arcade.draw_texture_rectangle(1920, 1080, 3840, 2160, self.background)
        
        arcade.draw_text("Signed Explorations", self.window.width/2, self.window.height/2, 
            arcade.csscolor.GHOST_WHITE, font_size=50, anchor_x="center", font_name="Kenney Pixel Square")
        arcade.draw_text("Press any key to contiue", self.window.width/2, self.window.height/2 - 75, 
            arcade.csscolor.GHOST_WHITE, font_size=20, anchor_x="center", font_name="Kenney Mini Square")

    def on_show_view(self):
        
        #arcade.set_background_color(arcade.csscolor.GHOST_WHITE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, key, modifiers):
        load_view = LoadingView()
        load_view.setup()
        self.window.show_view(load_view)