import arcade, PIL, threading, random
from src.actors.character import Dog, Task
from src.views.book_view import *

from src.video.video_control import *

import src.dialogue.speech_items as Speech
from src.util.thread_control import ThreadController

class PracticeView(arcade.View):
    _TARGET_DURATION = 11
    _NO_LETTER = '_'

    def __init__(
        self, 
        menu,
        cam_controller: CameraControl
    ) -> None:
        super().__init__()
        self.gui_camera = None
        self._menu = menu
        self._cc = cam_controller

        # Spelling requirements
        self._letter = self._NO_LETTER
        self._duration = 0

        self._previous = None
        self._predicted = None
        self._cam_texture = None
        self.state = True

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout(x=0, y=0, width=1000, height=650)

        self.background = arcade.load_texture("assets\interface\Puzzle_UI.png") 

        red_button = arcade.gui.UITextureButton(x=34, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        blue_button = arcade.gui.UITextureButton(x=34, y=440, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Blue.png'))
        self.v_box.add(blue_button)
        self.v_box.add(red_button)

        self.manager.add(self.v_box)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self._cam_buf = RingBuffer()
        self.video_t_closer = ThreadCloser()
        video_t = threading.Thread(
            target=practice_video_t, 
            args=(self._cc, self._cam_buf, self.video_t_closer)
        )
        # Track the video thread and closer
        self._video_t = ThreadController(video_t, self.video_t_closer)
        if CAPTURING:
            self._video_t.start()

        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
    
    def on_draw(self):
        self.clear()
        self.gui_camera.use()

        # Get image to draw
        img, self._predicted = self._cam_buf.get()
        img = PIL.Image.fromarray(img)

        if self._cam_texture: 
            # Remove the old texture from the global texture atlas
            self.window.ctx.default_atlas.remove(self._cam_texture)
            # Rebuild atlas to make removed space usable again
            self.window.ctx.default_atlas.rebuild()
        # Overwrite old texture
        self._cam_texture = arcade.Texture(str(random.randint(0,100000)), img)

        # Draw textures
        arcade.draw_lrwh_rectangle_textured(35, 0, 930, 650, self.background)
        arcade.draw_lrwh_rectangle_textured(560, 280, 340, 240, self._cam_texture)
        arcade.draw_text(self._letter, 250, 375, arcade.color.BLACK, 64, 80, font_name="Kenney Mini Square")
        self.manager.draw()

    def on_update(self, delta_time):
        print(self._predicted)

        if self._predicted == self._previous:
            self.increase_duration()
        else:
            self._previous = self._predicted
            self.reset_duration()

        if self.at_duration() and self._predicted != None:
            self._letter = self._predicted
        else:
            self._letter = self._NO_LETTER


    def on_key_release(self, symbol: int, modifiers: int):
        self._menu.setup()
        self.show_new_view(self._menu)

    def get_current_target(self) -> str:
        """ Return the current letter that should be signed. """
        return self._goal[self._count]

    def goal_reached(self) -> bool:
        """ Return a bool indicating if the complete word has been signed. True 
        indicates it has. False otherwise. """
        return self._count == len(self._goal)

    def progress_sign(self) -> None:
        """ Move to the next letter to sign of the goal word. """
        self.reset_duration()
        self._count += 1

    def increase_duration(self) -> None:
        """ Increment the duration counter by one """
        self._duration += 1

    def reset_duration(self) -> None:
        """ Reset the duration counter to 0 """
        self._duration = 0

    def at_duration(self) -> bool:
        """ Return true if at or greater than the maximum duration. False 
        otherwise.
        """
        return self._duration >= self._TARGET_DURATION

    def show_new_view(self, view):
        """ Transition to a new view with teardown """
        self.manager.clear()
        self.manager.disable()
        self.window.show_view(view)

def practice_video_t(
    controller: CameraControl, 
    buffer: RingBuffer, 
    closer: ThreadCloser
) -> None:
    """ Thread to display a video feed. 
    
    Params:
        controller (CameraControl): The camera controller to receive video from.
        buffer (RingBuffer): Shared memory location for image producing.
    """
    recog = Recogniser()
    bg = controller.get_background()

    while not closer.is_killed():
        # Ensure active
        closer.wait()

        img = controller.read_cam()
        roi = controller.get_roi()
        predicted = None
        
        # Show annotated image
        add_roi(img, roi)
        if WINDOW_DISPLAY:
            show_image_windowed(img)

        hand = get_hand_segment(bg, img, roi)
        if hand:
            frame, contour = hand
            frame = process_model_image(frame)
            predicted = recog.predict_letter(frame)

        # Add image to buffer
        buffer.put((cv2.cvtColor(img, cv2.COLOR_BGR2RGB), predicted))

    # Thread should die. Begin cleanup
    #controller.release_cam() 
    # FIXME If we release here, can't restart game from menu