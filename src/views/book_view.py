from typing import Callable
import arcade
from src.actors.character import Dog
from src.video.video_control import *
import src.views.sign_view as s


class LetterWidget(arcade.gui.UILabel, arcade.gui.UIInteractiveWidget):
    """ A class to act as a letter and button for the book view. Should display
    a letter and allow for letter clicking.
    """
    _FONT_FACE = "Kenney Mini Square"
    _LETTER_SIZE = 36
    _BAR_HEIGHT = 5
    _WIDTH = 30

    _INACTIVE_COLOUR = (215, 173, 115)
    _ACTIVE_COLOUR = (133,88,77)

    def __init__(
        self, 
        x: int, 
        y: int, 
        letter: str, 
        active: bool, 
        **kwargs
    ) -> None:
        self._active = active
        self._colour = self._ACTIVE_COLOUR if active else self._INACTIVE_COLOUR

        # Set up widgets
        super().__init__(
            x=x, y=y,
            text=letter, 
            width=self._WIDTH,
            align="center",
            text_color=self._colour,
            font_name=self._FONT_FACE, 
            font_size=self._LETTER_SIZE,
            **kwargs
        )

    def do_render(self, surface):
        self.prepare_render(surface)
        surface.clear()

        super().do_render(surface)

        if self.hovered:
            arcade.draw_xywh_rectangle_filled(
                0, 0,
                self.width, self._BAR_HEIGHT,
                self._colour
            )

class BookView(arcade.View):
    _FONT_FACE = "Kenney Mini Square"
    _ACTIVE_COLOUR = (133,88,77)
    _LETTER_BTN_SIZE = 36
    _X_OFFSET = 165
    _Y_OFFSET = 524
    _X_INC = 100
    _Y_INC = -60
    _COL_COUNT = 3

    _LETTERS = (
        "A", "B", "C", "D", "E", "F", "G", "I", "K", "L", "M", "N", "O", 
        "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" 
    )

    def _FRONT_TEXTURE(self, letter) -> str:
        """ Returns the path to a front texture """
        return f"assets/interface/{letter}-FRONT-VIEW.PNG"

    def _BACK_TEXTURE(self, letter) -> str:
        """ Returns the path to a back texture """
        return f"assets/interface/{letter}-BACK-VIEW.PNG"

    def __init__(self, game_view, npc : Dog, found_letters, sign_view = None):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc
        self.found_letters = found_letters

        self._sign_view = sign_view

        self.front_image = None
        self.back_image = None

        self.manager = arcade.gui.UIManager()


        # Generate textures for use
        self._textures = {}
        for letter in self._LETTERS:
            front = arcade.load_texture(self._FRONT_TEXTURE(letter))
            back = arcade.load_texture(self._BACK_TEXTURE(letter)) if letter \
                in "KEY" else None
            
            self._textures[letter] = [front, back]

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.manager.enable()
        self.v_box = arcade.gui.UILayout(x=0, y=0, width=1000, height=650)

        self.background = arcade.load_texture("assets\interface\Guide_UI.png") 

        red_button = arcade.gui.UITextureButton(x=34, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        green_button = arcade.gui.UITextureButton(x=34, y=354, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        self.v_box.add(green_button)
        self.v_box.add(red_button)

        red_button.on_click = self.on_click_game_button
        green_button.on_click = self.on_click_sign_button

        # Generate UI buttons
        self._ui_letters = {}
        for index, letter in enumerate(self._LETTERS):
            # Generate values
            x_pos = self._X_OFFSET + self._X_INC * (index % self._COL_COUNT)
            y_pos = self._Y_OFFSET + self._Y_INC * (index // self._COL_COUNT)

            # Add label to page
            active = letter in self.found_letters
            btn = LetterWidget(x_pos, y_pos, letter, active)

            def make_on_click(letter) -> Callable:
                """ Generates a function for on_click events. Needed to escape
                closure.
                """
                return lambda e: self.on_click_letter_button(letter)
            btn.on_click = make_on_click(letter)
            self.v_box.add(btn)

            # Store ui elements for later
            self._ui_letters[letter] = btn

        self.manager.add(self.v_box)


    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        #arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(35, 0, 930, 650, self.background)
        
        # Add view labels 575
        self.draw_label("Your View", 575)
        self.draw_label("Camera View", 335)

        if self.front_image:
            arcade.draw_texture_rectangle(730, 475, 340, 240, self.front_image)
        else:
            self.draw_undiscovered(y=475)
        if self.back_image:
            arcade.draw_texture_rectangle(730, 225, 340, 240, self.back_image)
        else:
            self.draw_undiscovered(y=235)
        self.manager.draw()
    
    def draw_label(self, text, y):
        """ Draw labels for the book images """
        arcade.draw_text(
            text, 
            745, y, 
            self._ACTIVE_COLOUR, 
            36, 400, 
            anchor_x="center", align="center", 
            font_name="Kenney Mini Square"
        )


    def draw_undiscovered(self, y):
        """ Draw text for the undiscovered image """
        arcade.draw_text(
            "Not Yet discovered", 
            650, y, 
            self._ACTIVE_COLOUR, 
            font_size=24,
            width=200,
            align="center",
            font_name="Kenney Mini Square"
        )

    def on_update(self, delta_time):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        self.show_new_view(self.game_view)

    def on_click_game_button(self, event):
        self.show_new_view(self.game_view)

    def on_click_sign_button(self, event):
        if self._sign_view is not None:
            self._sign_view.setup()
            self.show_new_view(self._sign_view)

    def on_click_letter_button(self, letter):
        self.front_image, self.back_image = self._textures.get(letter)
        self.front_image = self.front_image if letter in self.found_letters \
            else None
        self.back_image = self.back_image if letter in self.found_letters \
            else None

    def show_new_view(self, view):
        """ Transition to a new view with teardown """
        self.manager.clear()
        self.manager.disable()
        self.window.show_view(view)


