from turtle import color, width
from typing import List, Tuple

import arcade

class _TalkingHead(arcade.gui.UIWidget):
    def __init__(self, *, x=0, y=0, width=100, height=100, 
    sprite: arcade.Sprite = None, bg_color=(0, 0, 0, 0), **kwargs):
        super().__init__(x, y, width, height)
        self._sprite = sprite
        self._bg = bg_color

    def on_update(self, dt):
        self._sprite.update()
        self._sprite.update_animation(dt)
        self.trigger_render()

    def do_render(self, surface: arcade.gui.surface.Surface):
        self.prepare_render(surface)
        surface.clear(color=self._bg)
        surface.draw_sprite(0, 0, self.width, self.height, self._sprite)

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

    def _create_dialogue(self, text: str, size: int, speaker: arcade.Sprite):
        """ Create a layout containing a text widget with specified text and an
        associated talking head.
        
        Params:
            text (str): The text to put in the widget.
            size (int): The size of the text.
            speaker (Sprite): The sprite of the speaker.

        Returns:
            (UIBoxLayout) the created text widget.
        """
        box = arcade.gui.UIBoxLayout(vertical=False, align="bottom")

        # Make talking head take up 80% of box
        icon_height = icon_width = (self._height / 2)

        sprite = sprite=arcade.Sprite(texture=arcade.load_texture("assets/ui/Cat_Face.png"))
        box.add(_TalkingHead(
            width=icon_width, 
            height=icon_height, 
            sprite=sprite, 
            bg_color=arcade.color.WHITE
        )
        .with_space_around(
            top=(icon_height - self._TEXT_OFF_Y) / 2,
            bottom=(icon_height - self._TEXT_OFF_Y) / 2,
            bg_color=arcade.color.WHITE
        ))
        print(f"icon: {icon_height}")
        print(f"overall: {self._height}")

        box.add(self._create_text(text, size, width_shift=icon_width))

        return box

    def _create_text(
        self, 
        text: str, 
        size: int,
        width_shift: float = 0,
        height_shift: float = 0,
        width_offset: float = _TEXT_OFF_X,
        height_offset: float = _TEXT_OFF_Y
    ) -> arcade.gui.UIWidget:
        """ Create a text widget with the specified text.
        
        Params:
            text (str): The text to put in the widget.
            size (int): The size of the text.

        Returns:
            (UIWidget) the created text widget.
        """
        return arcade.gui.UITextArea(
            text = text,
            width = self._width - self._TEXT_OFF_X - width_shift,
            height = (self._height - self._TEXT_OFF_Y) / 2,
            font_size = size,
            font_name = self._FONT,
            text_color = self._TEXT_COLOUR
        ).with_space_around( 
            top = height_offset, # Offset the top
            right = self._TEXT_OFF_X - width_offset, # Offset horiz difference
            bottom = self._TEXT_OFF_Y - height_offset, # Offset vert difference
            left = width_offset, # Offset left
            bg_color = self._BG_COLOUR
        )

    def update(self):
        """ """
        # Remove previous texts
        self.clear()

        # Draw main text
        self.add(self._create_dialogue(self._current_text, 24, None))

        # Draw helper text
        self.add(self._create_text(self._HELP_MSG, 14))


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