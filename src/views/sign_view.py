import arcade, PIL
from src.actors.character import Dog, Task
import uuid

from src.video.video_control import *

class SignView(arcade.View):
    def __init__(self, game_view, npc: Dog, items, goal: str = None):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc
        self.items = items

        # Spelling requirements
        self._goal = goal.upper()
        self._count = 0

        self._predicted = None
        self._cam_texture = None
        self.state = True

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout(x=0, y=0, width=1000, height=650)

        self.background = arcade.load_texture("assets\interface\Puzzle_UI.png") 
        self.key = arcade.load_texture("assets\sprites\key.png")       

        button = arcade.gui.UITextureButton(x=34, y=444, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Blue.png'))
        self.v_box.add(button)

        button.on_click = self.on_click_button

        self.manager.add(self.v_box)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

    def on_draw(self):
        self.clear()
        self.gui_camera.use()

        # Get image to draw
        img, self._predicted = self.game_view._cam_buf.get()
        ui_frame = PIL.Image.fromarray(img)
        name = str(uuid.uuid4())

        if self._cam_texture:
            # Remove the old texture from the global texture atlas
            self.window.ctx.default_atlas.remove(self._cam_texture)
            # Rebuild atlas to make removed space usable again
            self.window.ctx.default_atlas.rebuild()
        # Overwrite old texture
        self._cam_texture = arcade.Texture(name, ui_frame)

        # Draw textures
        arcade.draw_lrwh_rectangle_textured(35, 0, 930, 650, self.background)
        arcade.draw_lrwh_rectangle_textured(244, 154, 64, 64, self.key)
        arcade.draw_lrwh_rectangle_textured(560, 280, 340, 240, self._cam_texture)
        self.manager.draw()
        arcade.cleanup_texture_cache()
    
    def on_update(self, delta_time):
        print(self._predicted)
        
        if self._predicted == self.get_current_target():
            print("Well Done")
            self.progress_sign()
        
            if self.goal_reached():
                print("Word has been spelt")
                self.npc.task = Task.KEY
                self.game_view.set == True
                self.window.show_view(self.game_view)

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)

    def on_click_button(self, event):
        print("hellp")

    def get_current_target(self) -> str:
        """ Return the current letter that should be signed. """
        return self._goal[self._count]

    def goal_reached(self) -> bool:
        """ Return a bool indicating if the complete word has been signed. True 
        indicates it has. False otherwise. """
        return self._count == len(self._goal)

    def progress_sign(self) -> None:
        """ Move to the next letter to sign of the goal word. """
        self._count += 1
