import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Signed Explorations"
BACKGROUND_PATH = "assets/backgrounds/"
SPRITE_PATH = "assets/sprites/"
LOGO_PATH = "assets/logos/TJHeat_L_C_250.png"

class StartView(arcade.View):

    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(False)
        self.background = arcade.load_texture(BACKGROUND_PATH + "placeholder_start_menu.jpg")

    def setup(self):
        """Set up screen here"""
        pass

    def on_draw(self):
        """Render screen"""
        self.clear()
        arcade.draw_texture_rectangle(1920, 1080, 3840, 2160, self.background)
        
        arcade.draw_text(SCREEN_TITLE, self.window.width/2, self.window.height/2, 
            arcade.csscolor.GHOST_WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press any key to contiue", self.window.width/2, self.window.height/2 - 75, 
            arcade.csscolor.GHOST_WHITE, font_size=20, anchor_x="center")

    def on_show_view(self):
        
        #arcade.set_background_color(arcade.csscolor.GHOST_WHITE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, key, modifiers):
        menu_view = MenuView()
        menu_view.setup()
        self.window.show_view(menu_view)

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.logo = arcade.load_texture(LOGO_PATH)


    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.GHOST_WHITE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        self.logo.draw_sized(self.window.width/2, self.window.height/2 + 75, 
            250, 250)
        
        

    def setup(self):
        pass
    


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable = True)
    start_view = StartView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

