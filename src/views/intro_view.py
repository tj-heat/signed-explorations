from enum import Enum

import arcade

from src.views.stateful_view import new_button, new_ui_text, StatefulView
from src.views.game_view import GameView

LINE_SPACER = " "

class IntroState(Enum):
    LORE        = 0
    TUTORIAL    = 1


class IntroView(StatefulView):
    """ This view will show a camera feed and generate the background for image
    processing.
    """
    # Text
    _LORE = [
        "Sometimes the end is a new beginning, ",
        "especially for those who have power over MAGIC.",
        LINE_SPACER,
        "Wielders of this forgotten art are never truly gone.",
        LINE_SPACER,
        "Their souls, guarded by an ancient being of unfathomable", 
        "power can be ignited once again.",
        LINE_SPACER,
        "So long as they have the power to learn the ways of",
        "their forgotten language."
    ]
    _TUTORIAL = [
        "...",
        "What happened to you? It's dark here",
        "Oh that's right...",
        LINE_SPACER,
        "You died.",
        LINE_SPACER,
        "But don't worry there's still time, you're a wizard after all.",
        "As long as you make your way into the centre of the cat-acombs,",
        "you can be resurrected",
        LINE_SPACER,
        "Good luck in getting your body back"
    ]

    def __init__(self, cam_controller):
        super().__init__()
        self._cc = cam_controller

        # State setups
        self._STATE_SETUP = {
            IntroState.LORE: self._init_inform,
            IntroState.TUTORIAL: self._init_tutorial,
        }

    def setup(self):
        """Set up the loading screen """
        self._init_inform()

    ##
    # State setup functions
    ##
    def _init_state(self, state, draw, teardown) -> None:
        """ Setup the state control """
        self._state = state
        self._do_draw = draw
        self._do_teardown = teardown

    def _init_inform(self):
        self._init_state(
            IntroState.LORE, 
            self._draw_inform, 
            self._end_ui_state
        )

        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()

        box = arcade.gui.UIBoxLayout()

        # Add text
        for text in self._LORE:
            box.add(new_ui_text(text))

        # Add proceed button
        self._begin_btn = new_button("Proceed")
        self._begin_btn.on_click = lambda e: self.set_state(IntroState.TUTORIAL)
        box.add(self._begin_btn.with_space_around(top=25, bottom=25))

        self._ui_manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=box
        ))
    
    def _init_tutorial(self):
        self._init_state(
            IntroState.TUTORIAL, 
            self._draw_tutorial, 
            self._end_ui_state
        )

        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()

        box = arcade.gui.UIBoxLayout()

        # Add text
        for text in self._TUTORIAL:
            box.add(new_ui_text(text))

        # Add proceed button
        self._begin_btn = new_button("Begin")
        self._begin_btn.on_click = lambda e: self._end_tutorial_state()
        box.add(self._begin_btn.with_space_around(top=25, bottom=25))

        self._ui_manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=box
        ))

    ##
    # State teardown functions
    ##  
    def _end_ui_state(self):
        """ Tear down states that use UI """
        self._ui_manager.clear()
        self._ui_manager.disable()
        #self._ui_manager = None

    def _end_tutorial_state(self):
        """ Tear down the tutorial state """
        self._end_ui_state()

        game = GameView(cam_controller=self._cc)
        game.setup()
        self.window.show_view(game)

    ##
    # Draw functions
    ##
    def _draw_inform(self):
        """ Draw the view for the inform state """
        self._ui_manager.draw()

    def _draw_tutorial(self):
        """ Draw the view for the tutorial state """
        # Draw UI
        self._ui_manager.draw()