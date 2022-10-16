import arcade
from src.actors.character import Dog, Task

class BookView(arcade.View):
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

    def on_click_button(self, event):
        print("hellp")
