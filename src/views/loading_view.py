import threading
from enum import Enum
from typing import Callable

import arcade

from src.video.video_control import CameraControl, CameraException
from src.views.menu_view import MenuView

BTN_STYLE = {
            "font_name" : "Kenney Mini Square",
            "font_size" : 15,
            "font_color" : arcade.color.WHITE,
            "bg_color_pressed" : arcade.color.WHITE,
            "border_color_pressed" : arcade.color.WHITE,
            "font_color_pressed" : arcade.color.BLACK,
}

class LoadingState(Enum):
    LOADING     = 0
    HAS_CAM     = 1
    NO_CAM      = 2

class LoadingView(arcade.View):
    """ This view will set up any information needed for the game before the
    game starts. The information currently needed is if a webcam is found."""
    
    # Constants
    _FONT_FACE = "Kenney Mini Square"
    _FONT_SIZE = 24
    _FONT_COLOUR = arcade.color.WHITE

    # Text
    _LOADING_MSG = "The game is loading, please wait"
    _NO_CAM_MSG = "This game requires video camera input to operate."
    _DOT = '.'

    # Control
    _MIN_DOT = 0
    _MAX_DOT = 5
    _DOT_INC_TIME = 0.5

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

        self._num_dots = self._MIN_DOT

        self._cc = None

        # State setups
        self._STATE_SETUP = {
            LoadingState.LOADING: self._init_loading,
            LoadingState.HAS_CAM: self._init_has_cam,
            LoadingState.NO_CAM: self._init_no_cam
        }

    def set_state(self, state) -> None:
        """ Set the next state of the view """
        self._next_state = state

    def set_cam_controller(self, cam_controller) -> None:
        """ Set the camera controller for the view """
        self._cc = cam_controller

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
        """Set up the loading screen """
        self._init_loading()

    def on_draw(self):
        """Render screen"""
        if self.has_new_state():
            if self._do_teardown:
                self._do_teardown()
            self.setup_next_state()

        self.clear()
        self._do_draw()

    def on_key_press(self, key, modifiers):
        if self.in_state(LoadingState.HAS_CAM):
            menu = MenuView(self._cc)
            menu.setup()
            self.window.show_view(menu)

    def _progress_dots(self, delta: float):
        """ Increment the dot counter cyclically, between the MIN and MAX dot 
        count, inclusive.

        Params:
            delta (float): Number of seconds since last call.
        """
        self._num_dots = self._MIN_DOT if self._num_dots >= self._MAX_DOT \
            else self._num_dots + 1

    ##
    # State setup functions
    ##
    def _init_loading(self):
        """ Set up the loading screen for the loading state """
        # Setup state control
        self._state = LoadingState.LOADING
        self._do_draw = self._draw_loading
        self._do_teardown = self._end_loading

        # Update the loading message periodically
        arcade.schedule(self._progress_dots, self._DOT_INC_TIME)

        # Grab camera
        self._cam_grab_t = threading.Thread(
            target=get_client_camera_t,
            args=(self.set_cam_controller, self.set_state)
        )
        self._cam_grab_t.start()
    
    def _init_has_cam(self):
        """ Set up the loading screen for the camera state """
        # Setup state control
        self._state = LoadingState.HAS_CAM
        self._do_draw = self._draw_has_cam
        self._do_teardown = None
    
    def _init_no_cam(self):
        """ Set up the loading screen for the no cam state """
        # Setup state control
        self._state = LoadingState.NO_CAM
        self._do_draw = self._draw_no_cam
        self._do_teardown = self._end_no_cam

        # Setup view
        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()

        # Components
        box = arcade.gui.UIBoxLayout(vertical=False)

        check_btn = new_button(text="Check Again")
        check_btn.on_click = lambda _: self.set_state(LoadingState.LOADING)
        box.add(check_btn.with_space_around(right=25))

        exit_btn = new_button(text="Exit")
        exit_btn.on_click = lambda _: self.window.close()
        box.add(exit_btn.with_space_around(left=25))

        self._ui_manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=box.with_space_around(top=150)
        ))

    ##
    # State teardown functions
    ##
    def _end_loading(self):
        """ Tear down the loading state """
        arcade.unschedule(self._progress_dots)
    
    def _end_no_cam(self):
        """ Tear down the no cam state """
        self._ui_manager.clear()
        self._ui_manager.disable()
        self._ui_manager = None

    ##
    # Draw functions
    ##
    def _draw_loading(self):
        """ Draw the view for the loading state """
        text_msg = f"{self._LOADING_MSG}{self._DOT * self._num_dots}"
        arcade.Text(
            text_msg, 
            self._x_mid, self._y_mid, 
            self._FONT_COLOUR, self._FONT_SIZE,
            anchor_x="center", anchor_y="center",
            font_name=self._FONT_FACE
        ).draw()

    def _draw_has_cam(self):
        """ Draw the view for the has camera state """
        text_msg = f"Loading complete. Press any button to continue."
        arcade.Text(
            text_msg, 
            self._x_mid, self._y_mid, 
            self._FONT_COLOUR, self._FONT_SIZE,
            anchor_x="center", anchor_y="center",
            font_name=self._FONT_FACE
        ).draw()

    def _draw_no_cam(self):
        """ Draw the view for the no camera state """
        arcade.Text(
            self._NO_CAM_MSG, 
            self._x_mid, self._y_mid, 
            self._FONT_COLOUR, self._FONT_SIZE,
            anchor_x="center", anchor_y="center",
            font_name=self._FONT_FACE
        ).draw()

        self._ui_manager.draw()

def get_client_camera_t(
    set_cam_controller: Callable,
    set_state: Callable
) -> None:
    """ Thread that will attempt to latch the client's webcam. """
    try:
        cc = CameraControl()
        set_cam_controller(cc)
        set_state(LoadingState.HAS_CAM)
    
    except CameraException as e:
        print(e)
        set_state(LoadingState.NO_CAM)

def new_button(text: str, width: int = 200) -> arcade.gui.UIFlatButton:
    """ Create a new, styled button for the loading screen """
    return arcade.gui.UIFlatButton(text=text, width=width, style=BTN_STYLE)