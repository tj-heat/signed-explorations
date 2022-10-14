import arcade
import src.views.menu_view as m
import src.views.game_view as g
from src.util.style import uni_style

BACKGROUND_PATH = "assets/backgrounds/"

class EndView(arcade.View):
    def __init__(self, game_view : "g.GameView"):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.game_view = game_view
        self.background = arcade.load_texture(BACKGROUND_PATH + "placeholder_start_menu.jpg")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        # look at UITEXTUREBUTTON
        restart_button = arcade.gui.UIFlatButton(text="Replay", width=200, style = uni_style)
        self.v_box.add(restart_button.with_space_around(bottom=20))
        
        quit_button = arcade.gui.UIFlatButton(text="Return to Menu", width=200, style = uni_style)
        self.v_box.add(quit_button)


        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        restart_button.on_click = self.on_click_restart
        quit_button.on_click = self.on_click_return

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
                size_hint = (1,1)
            )
        )


    def setup(self):
        """Set up screen here"""
        pass

    def on_draw(self):
        """Render screen"""
        self.clear()
        arcade.draw_texture_rectangle(1920, 1080, 3840, 2160, self.background)
        
        self.manager.draw()

        arcade.draw_text("You've made it through the first stage of your journey...", self.window.width/2, self.window.height/2 + 200, 
            arcade.csscolor.GHOST_WHITE, font_size=25, anchor_x="center", font_name="Kenney Pixel Square")
        arcade.draw_text("Who knows what awaits you next?", self.window.width/2, self.window.height/2 + 150, 
            arcade.csscolor.GHOST_WHITE, font_size=25, anchor_x="center", font_name="Kenney Pixel Square")
        arcade.draw_text("Thank you for playing our demo!", self.window.width/2, self.window.height/2 + 100, 
            arcade.csscolor.GHOST_WHITE, font_size=25, anchor_x="center", font_name="Kenney Mini Square")

    def on_show_view(self):
        
        #arcade.set_background_color(arcade.csscolor.GHOST_WHITE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, key, modifiers):
        menu = m.MenuView()
        menu.setup()
        self.window.show_view(menu)

    def on_click_restart(self, event):
        self.game_view.end_video()
        self.game_view.setup()
        self.window.show_view(self.game_view)

    def on_click_return(self, event):
        self.game_view.end_video()
        menu = m.MenuView()
        menu.setup()
        self.window.show_view(menu)