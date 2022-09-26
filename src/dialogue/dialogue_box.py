from turtle import color
from typing import List, Tuple

import arcade

class _DialogueBoxInt(arcade.gui.UIInteractiveWidget):
    _BG_COLOUR = arcade.color.WHITE
    _NO_TEXT = ""

    def __init__(self, text: Tuple[str], height: int, width: int, **kwargs):
        super().__init__(height=height, width=width, kwargs=kwargs)

        # Store dimensions
        # TODO remove this as widget has internal rectangle
        self._width = width
        self._height = height

        # Set up text display
        self._active = True
        self._text = text
        self._text_count = len(self._text)
        self._text_index = 0
        self._current_text = self._text[self._text_index]

    def _next_text(self) -> None:
        """ Move to the next text item """
        self._text_index += 1

        if self._text_index < self._text_count:
            self._current_text = self._text[self._text_index]
        else:
            self._current_text = self._NO_TEXT

    def _handle_interact(self) -> None:
        """ Handles interacting with the dialogue box. """
        self._next_text()

        if self._current_text == self._NO_TEXT:
            self._active = False

    def on_click(self, event) -> None:
        """ Manage on click event """
        self._handle_interact()

    def is_active(self) -> bool:
        """ Returns true if the dialogue box is active. False otherwise. """
        return self._active

    def do_render(self, surface: arcade.gui.Surface):
        """ """
        # Render background
        self.prepare_render(surface)
        surface.clear(self._BG_COLOUR)

        # Render text
        self.clear()
        self.add(arcade.gui.UITextArea(
            text=self._current_text,
            width=self._width - 50,
            height=self._height - 50,
            font_size=24,
            font_name="Arial",
            text_color=arcade.color.BLACK
        ))

        if self.pressed:
            arcade.draw_xywh_rectangle_outline(0, 0,
                                               self.width, self.height,
                                               color=arcade.color.BATTLESHIP_GREY,
                                               border_width=3)


class DialogueBox(arcade.gui.UIAnchorWidget):
    _BG_COLOUR = arcade.color.BLACK
    def __init__(
        self, 
        text: List[str],
        height: int = 100,
        width: int = 100,
        **kwargs
    ) -> None:
        """ """
        # Create interactive frame
        self._i_child = _DialogueBoxInt(text, height, width)
        
        super().__init__(
            child=self._i_child,
            anchor_y = "bottom",
            kwargs=kwargs
        )

        self._text = text

    def is_active(self) -> bool:
        """ Returns true if the dialogue box is active. False otherwise. """
        return self._i_child.is_active()

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