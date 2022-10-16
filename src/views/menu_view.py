import imp
import arcade, threading

import src.views.game_view as g
from src.video.video_control import CameraControl, display_video_t
from src.util.ring_buffer import RingBuffer
from src.util.thread_control import ThreadCloser, ThreadController
import arcade.experimental.uistyle as uistyle

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
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.background = arcade.load_texture(BACKGROUND_PATH + "placeholder_start_menu.jpg")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        # look at UITEXTUREBUTTON
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200, style = uni_style)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200, style = uni_style)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style = uni_style)
        self.v_box.add(exit_button)

        start_button.on_click = self.on_click_start
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
        arcade.draw_texture_rectangle(1920, 1080, 3840, 2160, self.background)
        self.manager.draw()
        arcade.draw_text("Signed Explorations", self.window.width/2, self.window.height/2 + 200, 
            arcade.csscolor.GHOST_WHITE, font_size=50, anchor_x="center", font_name="Kenney Pixel Square")

    def setup(self):
        # Video capture
        # NOTE The camera control may take several seconds to get cam control
        self._cc = CameraControl()

        # # Create video capture display thread
        # self._cam_buf = RingBuffer()
        # video_t_closer = ThreadCloser()
        # video_t = threading.Thread(
        #     target=display_video_t, 
        #     args=(self._cc, self._cam_buf, video_t_closer)
        # )

        # # Track the video thread and closer
        # self._video_t = ThreadController(video_t, video_t_closer)