import arcade, PIL, random
from src.actors.character import Dog, Task
from src.views.Book_view import *

from src.video.video_control import *

class SignView(arcade.View):
    def __init__(
        self, 
        game_view, 
        npc: Dog, 
        goal: str, 
        task: Task, 
        helper: arcade.Sprite = None
    ) -> None:
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc
        self._complete_task = task
        self._helper = helper

        # Spelling requirements
        self._goal = goal.upper()
        self._count = 0
        self._length = len(goal)

        self._predicted = None
        self._cam_texture = None
        self.state = True

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout(x=0, y=0, width=1000, height=650)

        self.background = arcade.load_texture("assets\interface\Puzzle_UI.png") 
        self.key = arcade.load_texture("assets\sprites\items\Object_key.png")       

        red_button = arcade.gui.UITextureButton(x=34, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        blue_button = arcade.gui.UITextureButton(x=34, y=440, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Blue.png'))
        self.v_box.add(blue_button)
        self.v_box.add(red_button)

        blue_button.on_click = self.on_click_blue_button
        red_button.on_click = self.on_click_red_button

        self.manager.add(self.v_box)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

    def switch(self, count, length):
        width = int((float(314) / (length + 1)))
        for i in range(length):
            if i > count:
                arcade.draw_text(self._goal[i], 105 + (width * (i + 1)), 380, arcade.color.BLACK, 40, 80, font_name="Kenney Mini Square")
            else:
                arcade.draw_text(self._goal[i], 105 + (width * (i + 1)), 380, arcade.color.RED, 40, 80, font_name="Kenney Mini Square")
    
    def on_draw(self):
        self.clear()
        self.gui_camera.use()

        # Get image to draw
        img, self._predicted = self.game_view._cam_buf.get()
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
        self.switch(self._count, self._length)
        self.draw_helper()
        self.manager.draw()
    
    def draw_helper(self):
        """ Draws the helper image in the view """
        if self._helper and self._helper.texture:
            arcade.draw_texture_rectangle(
                278, 182, 
                128, 128, 
                self.key
            )

    def on_update(self, delta_time):
        print(self._predicted)
        if self._complete_task == Task.DOOR:
            self.npc.task = self._complete_task
            return

        if self._predicted == self.get_current_target():
            print("Well Done")
            self.progress_sign()
        
            if self.goal_reached():
                print("Word has been spelt")
                self.npc.task = self._complete_task
                self.window.show_view(self.game_view)

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)

    def on_click_blue_button(self, event):
        book_view = BookView(self, self.npc, self._complete_task)
        book_view.setup()
        self.window.show_view(book_view)
        print("hellp")

    def on_click_red_button(self, event):
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
