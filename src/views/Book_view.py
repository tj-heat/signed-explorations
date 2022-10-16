import arcade, PIL, random
from src.actors.character import Dog, Task
from src.views.book_view import *
from src.video.video_control import *

class BookView(arcade.View):
    def __init__(self, game_view, npc : Dog):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc

        self.front_image = None
        self.back_image = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout(x=0, y=0, width=1000, height=650)

        self.background = arcade.load_texture("assets\interface\Guide_UI.png") 

        red_button = arcade.gui.UITextureButton(x=34, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        green_button = arcade.gui.UITextureButton(x=34, y=354, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        self.v_box.add(green_button)
        self.v_box.add(red_button)

        a_button = arcade.gui.UITextureButton(x=134, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        b_button = arcade.gui.UITextureButton(x=234, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        c_button = arcade.gui.UITextureButton(x=334, y=524, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png')) 

        d_button = arcade.gui.UITextureButton(x=134, y=464, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        e_button = arcade.gui.UITextureButton(x=234, y=464, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        f_button = arcade.gui.UITextureButton(x=334, y=464, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))

        g_button = arcade.gui.UITextureButton(x=134, y=404, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        i_button = arcade.gui.UITextureButton(x=234, y=404, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        k_button = arcade.gui.UITextureButton(x=334, y=404, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png')) 

        l_button = arcade.gui.UITextureButton(x=134, y=344, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        m_button = arcade.gui.UITextureButton(x=234, y=344, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        n_button = arcade.gui.UITextureButton(x=334, y=344, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))

        o_button = arcade.gui.UITextureButton(x=134, y=284, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        p_button = arcade.gui.UITextureButton(x=234, y=284, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        q_button = arcade.gui.UITextureButton(x=334, y=284, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png')) 

        r_button = arcade.gui.UITextureButton(x=134, y=224, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        s_button = arcade.gui.UITextureButton(x=234, y=224, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        t_button = arcade.gui.UITextureButton(x=334, y=224, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))

        u_button = arcade.gui.UITextureButton(x=134, y=164, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        v_button = arcade.gui.UITextureButton(x=234, y=164, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        w_button = arcade.gui.UITextureButton(x=334, y=164, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png')) 

        x_button = arcade.gui.UITextureButton(x=134, y=104, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))
        y_button = arcade.gui.UITextureButton(x=234, y=104, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Red.png'))   
        z_button = arcade.gui.UITextureButton(x=334, y=104, width=36, height=50, texture=arcade.load_texture('assets\interface\Book_UI_Tabs_Green.png'))

        self.v_box.add(a_button)
        self.v_box.add(b_button)
        self.v_box.add(c_button)
        self.v_box.add(d_button)
        self.v_box.add(e_button)
        self.v_box.add(f_button)
        self.v_box.add(g_button)
        self.v_box.add(i_button)
        self.v_box.add(k_button)
        self.v_box.add(l_button)
        self.v_box.add(m_button)
        self.v_box.add(n_button)
        self.v_box.add(o_button)
        self.v_box.add(p_button)
        self.v_box.add(q_button)
        self.v_box.add(r_button)
        self.v_box.add(s_button)
        self.v_box.add(t_button)
        self.v_box.add(u_button)
        self.v_box.add(v_button)
        self.v_box.add(w_button)
        self.v_box.add(x_button)
        self.v_box.add(y_button)
        self.v_box.add(z_button)

        a_button.on_click = lambda e: self.on_click_letter_button(letter= "A")
        b_button.on_click = lambda e: self.on_click_letter_button(letter= "B")
        c_button.on_click = lambda e: self.on_click_letter_button(letter= "C")
        d_button.on_click = lambda e: self.on_click_letter_button(letter= "D")
        e_button.on_click = lambda e: self.on_click_letter_button(letter= "E")
        f_button.on_click = lambda e: self.on_click_letter_button(letter= "F")
        g_button.on_click = lambda e: self.on_click_letter_button(letter= "G")
        i_button.on_click = lambda e: self.on_click_letter_button(letter= "I")
        k_button.on_click = lambda e: self.on_click_letter_button(letter= "K")
        l_button.on_click = lambda e: self.on_click_letter_button(letter= "L")
        m_button.on_click = lambda e: self.on_click_letter_button(letter= "M")
        n_button.on_click = lambda e: self.on_click_letter_button(letter= "N")
        o_button.on_click = lambda e: self.on_click_letter_button(letter= "O")
        p_button.on_click = lambda e: self.on_click_letter_button(letter= "P")
        q_button.on_click = lambda e: self.on_click_letter_button(letter= "Q")
        r_button.on_click = lambda e: self.on_click_letter_button(letter= "R")
        s_button.on_click = lambda e: self.on_click_letter_button(letter= "S")
        t_button.on_click = lambda e: self.on_click_letter_button(letter= "T")
        u_button.on_click = lambda e: self.on_click_letter_button(letter= "U")
        v_button.on_click = lambda e: self.on_click_letter_button(letter= "V")
        w_button.on_click = lambda e: self.on_click_letter_button(letter= "W")
        x_button.on_click = lambda e: self.on_click_letter_button(letter= "X")
        y_button.on_click = lambda e: self.on_click_letter_button(letter= "Y")
        z_button.on_click = lambda e: self.on_click_letter_button(letter= "Z")

        self.manager.add(self.v_box)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        #replace with camera feed

    def setup(self):
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)


    def on_draw(self):
        self.clear()
        self.gui_camera.use()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(35, 0, 930, 650, self.background)
        if self.front_image is not None:
            arcade.draw_texture_rectangle(730, 475, 340, 240, self.front_image)
        if self.back_image is not None:
            arcade.draw_texture_rectangle(560, 120, 340, 240, self.back_image)
        self.manager.draw()
    
    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)

    def on_click_red_button(self, event):
        print("hellp")

    def on_click_green_button(self, event):
        print("hellp")

    def on_click_letter_button(self, letter):
        image_front = "assets\interface\\" + letter + "-FRONT-VIEW.PNG"
        self.front_image = arcade.load_texture(image_front) 
        #image_back = "assets\interface\\" + letter + "-BACK-VIEW.PNG"
        #self.back_image = arcade.load_texture(image_back) 

