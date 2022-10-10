import arcade, threading, PIL
from src.actors.character import Dog, Task
from src.video.image_recognition import Recogniser
from PIL import Image
import uuid

from src.video.video_control import *

from src.video.image_processing import add_roi, crop_and_preprocess, \
    get_hand_segment, process_model_image

class SignView(arcade.View):
    def __init__(self, game_view, npc : Dog, items):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc
        self.items = items


        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        self.background = arcade.load_texture("assets\interface\Puzzle_UI.png")        

        button = arcade.gui.UITextureButton(x=30, y=30, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Blue.png'),
        texture_hovered=arcade.load_texture('assets\interface\Book_UI_Tabs_Blue.png'), texture_pressed=arcade.load_texture('assets\interface\Book_UI_Tabs_Blue.png'))
        self.v_box.add(button)

        button.on_click = self.on_click_button

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                align_x=-400,
                anchor_y="center",
                align_y=300,
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)


    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        UI = self.game_view._cam_buf.get()
        UIFrame = PIL.Image.fromarray(UI[0])
        name = str(uuid.uuid4())
        cam = arcade.Texture(name, UIFrame)
        arcade.draw_lrwh_rectangle_textured(35, 0, 930, 650, self.background)
        arcade.draw_lrwh_rectangle_textured(500, 400, 150, 260, cam)
        self.manager.draw()
        arcade.cleanup_texture_cache()
    
    def on_update(self, delta_time):
        UI = self.game_view._cam_buf.get()
        predicted = UI[1]
        print(predicted)
        if predicted == "K":
            print("Well Done")
            

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)

    def on_click_button(self, event):
        print("hellp")
