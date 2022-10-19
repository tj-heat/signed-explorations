import PIL, random
from enum import Enum

import arcade

from src.video.image_processing import add_roi
from src.views.stateful_view import new_button, new_ui_text, StatefulView
import src.views.menu_view as MenuView


class GenerationState(Enum):
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
        "Wielders of this forgotten art are never truly gone.",
        "Their souls, guarded by an ancient being of unfathomable", 
        "power can be ignited once again.",
        "So long as they have the power to learn the ways of",
        "their forgotten language."
    ]
    _TUTORIAL = [
        "",
    ]

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