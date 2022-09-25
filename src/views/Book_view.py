import arcade
from src.actors.character import Dog, Task

class BookView(arcade.View):
    def __init__(self, game_view, npc : Dog):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        self.v_box.add(exit_button)

        exit_button.on_click = self.on_key_press()

        self.background = arcade.load_texture("assets\interface\Guide_UI.png")

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1000, 650, self.background)
        self.manager.draw()
        arcade.draw_text("This is the sign language interaction, for now press any key to return to the game", 10, 10, arcade.csscolor.WHITE, 18)
    
    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)
