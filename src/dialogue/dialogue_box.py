from turtle import color
from typing import List, Tuple

import arcade

class _DialogueBoxInt(arcade.gui.UIBoxLayout, arcade.gui.UIInteractiveWidget):
    _BG_COLOUR = arcade.color.WHITE
    _TEXT_COLOUR = arcade.color.BLACK
    _FONT = "Kenney Mini Square"
    _NO_TEXT = ""    
    _TEXT_OFF_X = 50
    _TEXT_OFF_Y = 50
    _HELP_MSG = "Press <space> or click to continue..."

    def __init__(self, text: Tuple[str], height, width, **kwargs):
        self._container = arcade.gui.UIBoxLayout()
        super().__init__(**kwargs)

        # Store width and height
        self._width = width
        self._height = height
 
        # Set up text display
        self._active = True
        self._text = text
        self._text_count = len(self._text)
        self._text_index = 0
        self._current_text = self._text[self._text_index]

        self.update()

    def _next_text(self) -> None:
        """ Move to the next text item """
        self._text_index += 1

        if self._text_index < self._text_count:
            self._current_text = self._text[self._text_index]
        else:
            self._current_text = self._NO_TEXT

    def progress(self) -> None:
        """ Handles interacting with the dialogue box. """
        self._next_text()

        self.update()

        if self._current_text == self._NO_TEXT:
            self._active = False

    def on_click(self, event) -> None:
        """ Manage on click event """
        self.progress()

    def is_active(self) -> bool:
        """ Returns true if the dialogue box is active. False otherwise. """
        return self._active

    def _generate_text(self, text: str, size: int) -> arcade.gui.UIWidget:
        """ Create a text widget with the specified text.
        
        Params:
            text (str): The text to put in the widget.
            size (int): The size of the text.

        Returns:
            (UIWidget) the created text widget.
        """
        return arcade.gui.UITextArea(
            text = text,
            width = self._width - self._TEXT_OFF_X,
            # Divide height by two to account for two widgetss
            height = (self._height - self._TEXT_OFF_Y) / 2,
            font_size = size,
            font_name = self._FONT,
            text_color = self._TEXT_COLOUR
        ).with_space_around( 
            top = self._TEXT_OFF_Y,
            right = 0,
            bottom = 0,
            left = self._TEXT_OFF_X,
            bg_color = self._BG_COLOUR
        )

    def update(self):
        """ """
        # Remove previous texts
        self.clear()

        # Draw main text
        self.add(self._generate_text(self._current_text, 24))

        # Draw helper text
        self.add(self._generate_text(self._HELP_MSG, 14))


class DialogueBox(arcade.gui.UIAnchorWidget):
    _BG_COLOUR = arcade.color.BLACK
    def __init__(
        self, 
        text: List[str],
        height: int = 150,
        width: int = 150,
        **kwargs
    ) -> None:
        """ """
        # Create interactive frame
        self._i_child = _DialogueBoxInt(text, height=height, width=width)
        
        super().__init__(
            child=self._i_child,
            anchor_y = "bottom",
            kwargs=kwargs
        )

    def is_active(self) -> bool:
        """ Returns true if the dialogue box is active. False otherwise. """
        return self._i_child.is_active()

    def progress(self):
        """ Move to the next text item in the dialogue box. """
        self._i_child.progress()

    # def do_render(self, surface: arcade.gui.Surface):
    #     """ """
    #     self.prepare_render(surface)
    #     surface.clear(self._BG_COLOUR)

    #     if self._i_child.pressed:
    #         print("hello")
    #         arcade.draw_xywh_rectangle_outline(0, 0,
    #                                            self.width, self.height,
    #                                            color=arcade.color.BATTLESHIP_GREY,
    #                                            border_width=3)