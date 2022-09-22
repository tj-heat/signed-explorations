import arcade

import src.views.game_view as g
from src.video.video_control import CameraControl

BACKGROUND_PATH = "assets/backgrounds/"

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        # look at UITEXTUREBUTTON
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(exit_button)

        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        start_button.on_click = self.on_click_start
        exit_button.on_click = self.on_click_exit

        #settings_button.on_click =

        self.anchor = arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
                size_hint = (1,1)
            )

        #TODO fix this for the menu background.
        self.wrapper = arcade.gui.UIWrapper(
            child = self.anchor,
            padding = (self.window.width, self.window.width, self.window.width, self.window.width ),
            size_hint_max = self.window.height
        )


        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UITexturePane(
            child = self.wrapper,
            size_hint = (1,1),
            tex = arcade.load_texture(BACKGROUND_PATH + "placeholder_start_menu.jpg"))
        )


        

    def on_click_start(self, event):
        game = g.GameView(cam_controller=self._cc)
        game.setup()
        self.window.show_view(game)

    #added brute force os exit, TODO: Close game gracefully and with all threads killed (currently, only the game engine is killed an model keeps running)
    def on_click_exit(self, event):
        self.window.close()

    def on_click_settings(self, event):
        pass

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)


    def on_draw(self):
        self.clear()
        self.manager.draw()

    def setup(self):
        # Video capture
        # NOTE The camera control may take several seconds to get cam control
        self._cc = CameraControl() # TODO Need appropriate teardown method.