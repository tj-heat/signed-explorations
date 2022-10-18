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
        self.background = arcade.load_texture(BACKGROUND_PATH + "End_Screen.png")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        restart_button = arcade.gui.UIFlatButton(text="Replay", width=200, style = uni_style)
        self.v_box.add(restart_button.with_space_around(bottom=20))
        
        quit_button = arcade.gui.UIFlatButton(text="Return to Menu", width=200, style = uni_style)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        restart_button.on_click = self.on_click_restart
        quit_button.on_click = self.on_click_return

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box,
                size_hint = (1,1)
            )
        )

    def setup(self):
        pass

    def on_draw(self):
        """Render screen"""
        self.clear()
        arcade.draw_texture_rectangle(
            self.window.width / 2, self.window.height / 2, 
            self.background.width, self.background.height, 
            self.background
        )
        
        self.manager.draw()
        
        arcade.draw_text(
            "Thank you for playing our demo!", 
            self.window.width/2, self.window.height - 50, 
            arcade.color.WHITE, font_size=32, 
            anchor_x="center", 
            font_name="Kenney Mini Square"
        )

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_click_restart(self, event):
        self.game_view.end_video()
        self.game_view.setup()
        self.show_new_view(self.game_view)

    def on_click_return(self, event):
        self.game_view.end_video()
        menu = m.MenuView(self.game_view.cam_controller)
        menu.setup()
        self.show_new_view(menu)

    def show_new_view(self, view: arcade.View):
        """ Show a new view and close current ui """
        self.manager.clear()
        self.manager.disable()
        self.window.show_view(view)