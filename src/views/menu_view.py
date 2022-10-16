import arcade

import src.views.game_view as g
import src.views.loading_view as LoadViews 
from src.video.video_control import CameraControl


BACKGROUND_PATH = "assets/backgrounds/"

uni_style = {
            "font_name" : "Kenney Mini Square",
            "font_size" : 15,
            "font_color" : arcade.color.WHITE,
            "boarder_width" : 0,
            "border_color" : None,
            "bg_color" : arcade.color.BLACK,
            "bg_color_pressed" : arcade.color.WHITE,
            "border_color_pressed" : arcade.color.WHITE,
            "font_color_pressed" : arcade.color.BLACK,
        }

class MenuView(arcade.View):
    def __init__(self, cam_controller: CameraControl):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.background = arcade.load_texture(BACKGROUND_PATH + "splash.png")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Store camera controller
        self._cc = cam_controller

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        # look at UITEXTUREBUTTON
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200, style = uni_style)
        self.v_box.add(start_button.with_space_around(bottom=20))
        
        background_button = arcade.gui.UIFlatButton(text="Background", width=200, style = uni_style)
        self.v_box.add(background_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style = uni_style)
        self.v_box.add(exit_button)

        start_button.on_click = self.on_click_start
        background_button.on_click = self.on_click_background
        exit_button.on_click = self.on_click_exit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
                size_hint = (1,1)
            )
        )

    def on_click_start(self, event):
        self.manager.clear()
        game = g.GameView(cam_controller=self._cc)
        game.setup()
        self.window.show_view(game)

    #added brute force os exit, TODO: Close game gracefully and with all threads killed (currently, only the game engine is killed an model keeps running)
    def on_click_exit(self, event):
        self.window.close()

    def on_click_background(self, event):
        self.manager.clear()
        bg_gen = LoadViews.BackgroundGenView(self._cc)
        bg_gen.setup()
        self.window.show_view(bg_gen)

    def on_click_settings(self, event):
        pass

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(self.window.width/2, self.window.height/2, 1024, 640, self.background)
        self.manager.draw()
        arcade.draw_text("Signed Explorations", self.window.width/2, self.window.height/2 + 200, 
            arcade.csscolor.GHOST_WHITE, font_size=50, anchor_x="center", font_name="Kenney Pixel Square")

    def setup(self):
        pass