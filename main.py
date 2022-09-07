import arcade
import arcade.gui
import game

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Signed Explorations"
BACKGROUND_PATH = "assets/backgrounds/"
SPRITE_PATH = "assets/sprites/"

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

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.RED_ORANGE)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(exit_button)

        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        start_button.on_click = self.on_click_start


        #settings_button.on_click =

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )


    def on_click_start(self, event):
        game_view = game.GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.GHOST_WHITE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)


    def on_draw(self):
        self.clear()
        self.manager.draw()

    def setup(self):
        pass

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable = True) #resizable = True
    start_view = StartView() #StartView() #game.GameView() 
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

