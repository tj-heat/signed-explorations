import PIL, random, threading
from enum import Enum
from typing import Callable

import arcade

from src.video.image_processing import add_roi
from src.video.video_control import CameraControl, CameraException
import src.views.menu_view as MenuView

FONT_FACE = "Kenney Mini Square"
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


class GenerationState(Enum):
    INFORM      = 0
    GENERATE    = 1


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


class LoadingView(StatefulView):
    """ This view will set up any information needed for the game before the
    game starts. The information currently needed is if a webcam is found."""
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

        self._num_dots = self._MIN_DOT

        self._cc = None

        # State setups
        self._STATE_SETUP = {
            LoadingState.LOADING: self._init_loading,
            LoadingState.HAS_CAM: self._init_has_cam,
            LoadingState.NO_CAM: self._init_no_cam
        }

    def set_cam_controller(self, cam_controller) -> None:
        """ Set the camera controller for the view """
        self._cc = cam_controller

    def setup(self):
        """Set up the loading screen """
        self._init_loading()

    def on_key_press(self, key, modifiers):
        if self.in_state(LoadingState.HAS_CAM):
            bg_gen = BackgroundGenView(self._cc)
            bg_gen.setup()
            self.window.show_view(bg_gen)

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
            font_name=FONT_FACE
        ).draw()

    def _draw_has_cam(self):
        """ Draw the view for the has camera state """
        text_msg = f"Loading complete. Press any button to continue."
        arcade.Text(
            text_msg, 
            self._x_mid, self._y_mid, 
            self._FONT_COLOUR, self._FONT_SIZE,
            anchor_x="center", anchor_y="center",
            font_name=FONT_FACE
        ).draw()

    def _draw_no_cam(self):
        """ Draw the view for the no camera state """
        arcade.Text(
            self._NO_CAM_MSG, 
            self._x_mid, self._y_mid, 
            self._FONT_COLOUR, self._FONT_SIZE,
            anchor_x="center", anchor_y="center",
            font_name=FONT_FACE
        ).draw()

        self._ui_manager.draw()


# TODO Abstract to StatefulView
class BackgroundGenView(StatefulView):
    """ This view will show a camera feed and generate the background for image
    processing.
    """
    # Text
    _INFORM = [
        "Before playing the game a camera background is needed.",
        "This background will be used to better detect hand signs made while playing.",
        "The background should be a uniformly coloured, unchanging area.",
        "The background should be behind where your hands will be when signing.",
        "The ideal distance for the background is roughly 1m from the camera.",
        "Try not to move or record any body parts when generating the background.",
        "The generation should take five seconds at most.",
        "Click to proceed when you are ready to generate a background.",
        "The generation process can be repeated later if needed."
    ]
    _GENERATE_MSG = "Line the coloured box up with the ideal background position."

    def __init__(self, cc):
        super().__init__()
        self._cc = cc

        # State setups
        self._STATE_SETUP = {
            GenerationState.INFORM: self._init_inform,
            GenerationState.GENERATE: self._init_generate,
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
            GenerationState.INFORM, 
            self._draw_inform, 
            self._end_ui_state
        )

        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()

        box = arcade.gui.UIBoxLayout()

        # Add text
        for text in self._INFORM:
            box.add(new_ui_text(text))

        # Add proceed button
        btn = new_button("Proceed")
        btn.on_click = lambda e: self.set_state(GenerationState.GENERATE)
        box.add(btn.with_space_around(top=50))

        self._ui_manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=box
        ))
    
    def _init_generate(self):
        self._init_state(
            GenerationState.GENERATE, 
            self._draw_generate, 
            self._end_ui_state
        )
        self._img_roi = self._cc.get_roi()
        self._cam_texture = None

        self._ui_manager = arcade.gui.UIManager()
        self._ui_manager.enable()

        box = arcade.gui.UIBoxLayout()

        # Add text
        self._gen_text = new_ui_text(self._GENERATE_MSG, top_pad=0)
        box.add(self._gen_text)

        # Add proceed button
        self._gen_btn = new_button("Generate")
        self._gen_btn.on_click = self._handle_generate_click
        box.add(self._gen_btn.with_space_around(top=10, bottom=25))

        self._ui_manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="bottom",
            child=box
        ))

    def _handle_generate_click(self, event):
        """ Handle clicking on the generate background button. """
        # FIXME This does not change text
        self._gen_btn.text = "Generating..."
        self._gen_text.text = "Generating. Please wait..."

        self._cc.create_background()
        self._end_ui_state()

        menu = MenuView.MenuView(self._cc)
        menu.setup()
        self.window.show_view(menu)

    ##
    # State teardown functions
    ##  
    def _end_ui_state(self):
        """ Tear down states that use UI """
        self._ui_manager.clear()
        self._ui_manager.disable()
        self._ui_manager = None

    ##
    # Draw functions
    ##
    def _draw_inform(self):
        """ Draw the view for the inform state """
        self._ui_manager.draw()

    def _draw_generate(self):
        """ Draw the view for the generate state """
        img = self._cc.read_cam(rgb = True)
        add_roi(img, self._img_roi)
        img = PIL.Image.fromarray(img)

        if self._cam_texture:
            # Remove the old texture from the global texture atlas
            self.window.ctx.default_atlas.remove(self._cam_texture)
            # Rebuild atlas to make removed space usable again
            self.window.ctx.default_atlas.rebuild()
        # Overwrite old texture
        self._cam_texture = arcade.Texture(str(random.randint(0,100000)), img)

        # Draw textures
        v_shift = 75
        width, height = self._cam_texture.width, self._cam_texture.height
        bl_x = self._x_mid - (self._cam_texture.width / 2)
        bl_y = self._y_mid - (self._cam_texture.height / 2) + v_shift
        arcade.draw_lrwh_rectangle_textured(
            bl_x, bl_y, 
            self._cam_texture.width, self._cam_texture.height,
            self._cam_texture
        )

        # Draw UI
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

def new_ui_text(text: str, top_pad : int = 10) -> arcade.gui.UIWidget:
    """ Generate a widget containing text """
    return arcade.gui.UILabel(
        text=text,
        font_name=FONT_FACE,
        font_size=18,
        align="center",
    ).with_space_around(top=top_pad)