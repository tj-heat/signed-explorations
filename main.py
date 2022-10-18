import arcade
import arcade.gui

import src.views.start_view as StartView
import pyglet

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Signed Explorations"
LOGO_PATH = "assets/logos/TJHeat_L_C_250.png"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable  = True) #fullscreen = True resizable = True
    window.set_icon(pyglet.resource.image(LOGO_PATH))
    start_view = StartView.StartView() #StartView() #game.GameView() 
    start_view.setup()
    window.show_view(start_view)
    arcade.run() 

if __name__ == "__main__":
    main()

