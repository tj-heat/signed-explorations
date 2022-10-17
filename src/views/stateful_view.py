import arcade

class StatefulView(arcade.View):
    """ Abstract class to set up views with a state. """
    # Constants
    _FONT_SIZE = 24
    _FONT_COLOUR = arcade.color.WHITE
    def __init__(self):
        super().__init__()
     
        # Positions
        self._x_mid = self.window.width / 2
        self._y_mid = self.window.height / 2

        # Control
        self._do_draw = None
        self._do_teardown = None
        self._state = None
        self._next_state = None

    def set_state(self, state) -> None:
        """ Set the next state of the view """
        self._next_state = state

    def in_state(self, state) -> bool:
        return self._state == state

    def has_new_state(self) -> bool:
        """ Returns a bool indicating if there is a new state to trainsition to.
        There is a new state if the next state to move to is different to the
        current state.
        """
        return self._next_state and not self.in_state(self._next_state)

    def setup_next_state(self):
        """ Set the laoding screen up to move to the next state """
        do_setup = self._STATE_SETUP.get(self._next_state)
        do_setup()

    def setup(self):
        """ Sets up the view for showing. Raises NotImplementedError """
        raise NotImplementedError()

    def on_draw(self):
        """Render view"""
        if self.has_new_state():
            if self._do_teardown:
                self._do_teardown()
            self.setup_next_state()

        self.clear()
        self._do_draw()

FONT_FACE = "Kenney Mini Square"
BTN_STYLE = {
    "font_name" : FONT_FACE,
    "font_size" : 15,
    "font_color" : arcade.color.WHITE,
    "bg_color_pressed" : arcade.color.WHITE,
    "border_color_pressed" : arcade.color.WHITE,
    "font_color_pressed" : arcade.color.BLACK,
}

def new_button(text: str, width: int = 200) -> arcade.gui.UIFlatButton:
    """ Create a new, styled button for the loading screen """
    return arcade.gui.UIFlatButton(text=text, width=width, style=BTN_STYLE)

def new_ui_text(text: str, top_pad : int = 10) -> arcade.gui.UIWidget:
    """ Generate a widget containing text """
    return arcade.gui.UILabel(
        text=text,
        font_name=FONT_FACE,
        font_size=18,
        align="center",
    ).with_space_around(top=top_pad)