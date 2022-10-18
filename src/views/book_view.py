import arcade
from src.actors.character import Dog
from src.views.book_view import *
from src.video.video_control import *

class BookView(arcade.View):
    def __init__(self, game_view, npc : Dog, found_list):
        super().__init__()
        self.game_view = game_view
        self.gui_camera = None
        self.npc = npc
        self.found_list = found_list

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

        red_button.on_click = self.on_click_red_button


        a_label = arcade.gui.UILabel(x=134, y=524, width=36, height=50, text="A", text_color=(133,88,77), font_name="Kenney Mini Square", font_size= 36)   
        b_label = arcade.gui.UILabel(x=234, y=524, width=36, height=50, text="B", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        c_label = arcade.gui.UILabel(x=334, y=524, width=36, height=50, text="C", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36) 

        d_label = arcade.gui.UILabel(x=134, y=464, width=36, height=50, text="D", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        if "E" in self.found_list:
            e_label = arcade.gui.UILabel(x=234, y=464, width=36, height=50, text="E", text_color=(0,0,0), font_name="Kenney Mini Square", font_size= 36)            
        else:
            e_label = arcade.gui.UILabel(x=234, y=464, width=36, height=50, text="E", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)   
        f_label = arcade.gui.UILabel(x=334, y=464, width=36, height=50, text="F", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)

        g_label = arcade.gui.UILabel(x=134, y=404, width=36, height=50, text="G", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)   
        i_label = arcade.gui.UILabel(x=234, y=404, width=36, height=50, text="I", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        if "K" in self.found_list:
            k_label = arcade.gui.UILabel(x=334, y=404, width=36, height=50, text="K", text_color=(0,0,0), font_name="Kenney Mini Square", font_size= 36) 
        else:
            k_label = arcade.gui.UILabel(x=334, y=404, width=36, height=50, text="K", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36) 
        l_label = arcade.gui.UILabel(x=134, y=344, width=36, height=50, text="L", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        m_label = arcade.gui.UILabel(x=234, y=344, width=36, height=50, text="M", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)   
        n_label = arcade.gui.UILabel(x=334, y=344, width=36, height=50, text="N", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)

        o_label = arcade.gui.UILabel(x=134, y=284, width=36, height=50, text="O", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)   
        p_label = arcade.gui.UILabel(x=234, y=284, width=36, height=50, text="P", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        q_label = arcade.gui.UILabel(x=334, y=284, width=36, height=50, text="Q", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36) 

        r_label = arcade.gui.UILabel(x=134, y=224, width=36, height=50, text="R", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        s_label = arcade.gui.UILabel(x=234, y=224, width=36, height=50, text="S", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)   
        t_label = arcade.gui.UILabel(x=334, y=224, width=36, height=50, text="T", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)

        u_label = arcade.gui.UILabel(x=134, y=164, width=36, height=50, text="U", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)   
        v_label = arcade.gui.UILabel(x=234, y=164, width=36, height=50, text="V", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        w_label = arcade.gui.UILabel(x=334, y=164, width=36, height=50, text="W", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36) 

        x_label = arcade.gui.UILabel(x=134, y=104, width=36, height=50, text="X", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)
        if "Y" in self.found_list:
            y_label = arcade.gui.UILabel(x=234, y=104, width=36, height=50, text="Y", text_color=(0,0,0), font_name="Kenney Mini Square", font_size= 36)
        else:
            y_label = arcade.gui.UILabel(x=234, y=104, width=36, height=50, text="Y", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)   
        z_label = arcade.gui.UILabel(x=334, y=104, width=36, height=50, text="Z", text_color=(211,211,211), font_name="Kenney Mini Square", font_size= 36)

        a_button = arcade.gui.UIInteractiveWidget(x=134, y=524, width=36, height=50)   
        b_button = arcade.gui.UIInteractiveWidget(x=234, y=524, width=36, height=50)
        c_button = arcade.gui.UIInteractiveWidget(x=334, y=524, width=36, height=50) 

        d_button = arcade.gui.UIInteractiveWidget(x=134, y=464, width=36, height=50)
        e_button = arcade.gui.UIInteractiveWidget(x=234, y=464, width=36, height=50)   
        f_button = arcade.gui.UIInteractiveWidget(x=334, y=464, width=36, height=50)

        g_button = arcade.gui.UIInteractiveWidget(x=134, y=404, width=36, height=50)   
        i_button = arcade.gui.UIInteractiveWidget(x=234, y=404, width=36, height=50)
        k_button = arcade.gui.UIInteractiveWidget(x=334, y=404, width=36, height=50) 

        l_button = arcade.gui.UIInteractiveWidget(x=134, y=344, width=36, height=50)
        m_button = arcade.gui.UIInteractiveWidget(x=234, y=344, width=36, height=50)   
        n_button = arcade.gui.UIInteractiveWidget(x=334, y=344, width=36, height=50)

        o_button = arcade.gui.UIInteractiveWidget(x=134, y=284, width=36, height=50)   
        p_button = arcade.gui.UIInteractiveWidget(x=234, y=284, width=36, height=50)
        q_button = arcade.gui.UIInteractiveWidget(x=334, y=284, width=36, height=50) 

        r_button = arcade.gui.UIInteractiveWidget(x=134, y=224, width=36, height=50)
        s_button = arcade.gui.UIInteractiveWidget(x=234, y=224, width=36, height=50)   
        t_button = arcade.gui.UIInteractiveWidget(x=334, y=224, width=36, height=50)

        u_button = arcade.gui.UIInteractiveWidget(x=134, y=164, width=36, height=50)   
        v_button = arcade.gui.UIInteractiveWidget(x=234, y=164, width=36, height=50)
        w_button = arcade.gui.UIInteractiveWidget(x=334, y=164, width=36, height=50) 

        x_button = arcade.gui.UIInteractiveWidget(x=134, y=104, width=36, height=50)
        y_button = arcade.gui.UIInteractiveWidget(x=234, y=104, width=36, height=50)   
        z_button = arcade.gui.UIInteractiveWidget(x=334, y=104, width=36, height=50)

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
        self.v_box.add(a_label)
        self.v_box.add(b_label)
        self.v_box.add(c_label)
        self.v_box.add(d_label)
        self.v_box.add(e_label)
        self.v_box.add(f_label)
        self.v_box.add(g_label)
        self.v_box.add(i_label)
        self.v_box.add(k_label)
        self.v_box.add(l_label)
        self.v_box.add(m_label)
        self.v_box.add(n_label)
        self.v_box.add(o_label)
        self.v_box.add(p_label)
        self.v_box.add(q_label)
        self.v_box.add(r_label)
        self.v_box.add(s_label)
        self.v_box.add(t_label)
        self.v_box.add(u_label)
        self.v_box.add(v_label)
        self.v_box.add(w_label)
        self.v_box.add(x_label)
        self.v_box.add(y_label)
        self.v_box.add(z_label)

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
            arcade.draw_text("Your View", 610, 575, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
            arcade.draw_texture_rectangle(730, 475, 340, 240, self.front_image)
        else:
            arcade.draw_text("Not Yet discovered", 610, 575, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
        if self.back_image is not None:
            arcade.draw_text("Camera View", 570, 335, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
            arcade.draw_texture_rectangle(730, 225, 340, 240, self.back_image)
        else:
            arcade.draw_text("Not Yet discovered", 570, 335, arcade.color.BLACK, 36, 80, font_name="Kenney Mini Square")
        self.manager.draw()
    
    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        self.window.show_view(self.game_view)

    def on_click_red_button(self, event):
        self.window.show_view(self.game_view)

    def on_click_green_button(self, event):
        pass

    def on_click_letter_button(self, letter):
        if letter in self.found_list:
            image_front = "assets\interface\\" + letter + "-FRONT-VIEW.PNG"
            self.front_image = arcade.load_texture(image_front) 
            if letter == "K" or letter == "E" or letter == "Y":
                image_back = "assets\interface\\" + letter + "-BACK-VIEW.PNG"
                self.back_image = arcade.load_texture(image_back) 
            else:
                self.back_image = None
        else: 
            self.front_image = None
            self.back_image = None


