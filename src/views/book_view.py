from cgitb import text
from typing import Callable
import arcade
from src.actors.character import Dog
from src.views.book_view import *
from src.video.video_control import *

class BookView(arcade.View):
    _FONT_FACE = "Kenney Mini Square"
    _INACTIVE_COLOUR = (215, 173, 115)
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

    def __init__(self, game_view, npc : Dog, found_letters):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc
        self.found = found_letters

        self.front_image = None
        self.back_image = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout(x=0, y=0, width=1000, height=650)

        self.background = arcade.load_texture("assets\interface\Guide_UI.png") 

        red_button = arcade.gui.UITextureButton(x=34, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        green_button = arcade.gui.UITextureButton(x=34, y=354, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        self.v_box.add(green_button)
        self.v_box.add(red_button)

        red_button.on_click = self.on_click_red_button

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

                # Generate UI buttons
        self._ui_letters = {}
        for index, letter in enumerate(self._LETTERS):
            # Generate values
            x_pos = self._X_OFFSET + self._X_INC * (index % self._COL_COUNT)
            y_pos = self._Y_OFFSET + self._Y_INC * (index // self._COL_COUNT)
            colour = self._ACTIVE_COLOUR if letter in self.found else \
                self._INACTIVE_COLOUR

            # Add label to page
            label = arcade.gui.UILabel(
                x=x_pos, y=y_pos,
                text = letter, text_color=colour,
                font_name=self._FONT_FACE, font_size=self._LETTER_BTN_SIZE
            )
            self.v_box.add(label)

            # Add interactive widget on top of label
            # FIXME This should probably be a wrapper
            btn = arcade.gui.UIInteractiveWidget(
                x=x_pos, y=y_pos,
                width=50, height=50,
            )

            def make_on_click(letter) -> Callable:
                """ Generates a function for on_click events. Needed to escape
                closure.
                """
                return lambda e: self.on_click_letter_button(letter)
            btn.on_click = make_on_click(letter)
            self.v_box.add(btn)

            # Store ui elements for later
            self._ui_letters[letter] = [label, btn]

        self.manager.add(self.v_box)


    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        #arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(35, 0, 930, 650, self.background)
        
        if self.front_image:
            arcade.draw_text("Your View", 610, 575, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
            arcade.draw_texture_rectangle(730, 475, 340, 240, self.front_image)
        else:
            arcade.draw_text("Not Yet discovered", 610, 575, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
        
        if self.back_image:
            arcade.draw_text("Camera View", 570, 335, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
            arcade.draw_texture_rectangle(730, 225, 340, 240, self.back_image)
        else:
            arcade.draw_text("Not Yet discovered", 570, 335, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
        self.manager.draw()
    
    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)

    def on_click_red_button(self, event):
        self.window.show_view(self.game_view)

    def on_click_green_button(self, event):
        pass

    def on_click_letter_button(self, letter):
        self.front_image, self.back_image = self._textures.get(letter)
        self.front_image = self.front_image if letter in self.found else None


