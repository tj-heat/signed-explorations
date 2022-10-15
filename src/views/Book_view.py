import arcade, PIL, random
from src.actors.character import Dog, Task
from src.views.Book_view import *
from src.video.video_control import *

class BookView(arcade.View):
    def __init__(self, game_view, npc : Dog, task: Task):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout(x=0, y=0, width=1000, height=650)

        self.background = arcade.load_texture("assets\interface\Guide_UI.png") 

        red_button = arcade.gui.UITextureButton(x=34, y=404, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        green_button = arcade.gui.UITextureButton(x=34, y=444, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        self.v_box.add(green_button)
        self.v_box.add(red_button)

        green_button.on_click = self.on_click_green_button
        red_button.on_click = self.on_click_red_button

        self.manager.add(self.v_box)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)


    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(35, 0, 930, 650, self.background)
        self.manager.draw()
    
    def on_update(self, delta_time):
        if True:
            if self.items[0].type == "Key":
                self.npc.task = Task.KEY
            else:
                raise Exception(f"Unknown item type {self.items[0].type}")
        self.game_view.setup()

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)

    def on_click_red_button(self, event):
        print("hellp")

    def on_click_green_button(self, event):
        print("hellp")

