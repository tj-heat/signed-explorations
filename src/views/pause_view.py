import arcade
import src.views.game_view as GameView
import src.views.menu_view as m

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

class PauseView(arcade.View):
    def __init__(self, game_view : "GameView.GameView"):
        super().__init__()
        self.background = arcade.load_texture(BACKGROUND_PATH + "placeholder_start_menu.jpg")
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        # look at UITEXTUREBUTTON
        restart_button = arcade.gui.UIFlatButton(text="Restart Game", width=200, style = uni_style)
        self.v_box.add(restart_button.with_space_around(bottom=20))

        return_button = arcade.gui.UIFlatButton(text="Return to Game", width=200, style = uni_style)
        self.v_box.add(return_button.with_space_around(bottom=20))
        
        quit_button = arcade.gui.UIFlatButton(text="Quit to Menu", width=200, style = uni_style)
        self.v_box.add(quit_button)


        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        restart_button.on_click = self.on_click_restart
        return_button.on_click = self.on_click_return
        quit_button.on_click = self.on_click_quit


        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
                size_hint = (1,1)
            )
        )

    def on_click_restart(self, event):
        self.game_view.end_video()
        self.game_view.setup()
        self.show_new_view(self.game_view)

    def on_click_return(self, event):
        self.game_view.resume_video()
        self.show_new_view(self.game_view)

    def on_click_quit(self, event):
        self.game_view.end_video()
        menu = m.MenuView(self.game_view.cam_controller)
        menu.setup()
        self.show_new_view(menu)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        #replace with camera feed

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(1920, 1080, 3840, 2160, self.background)
        self.manager.draw()
        arcade.draw_text("Paused", self.window.width/2, self.window.height/2 + 200, 
            arcade.csscolor.GHOST_WHITE, font_size=50, anchor_x="center", font_name="Kenney Pixel Square")
    
    def show_new_view(self, view):
        """ Transition to a new view with teardown """
        self.clear()
        self.manager.clear()
        self.manager.disable()
        self.window.show_view(view)

    def on_update(self, delta_time):
        pass

    def setup(self):
        pass
