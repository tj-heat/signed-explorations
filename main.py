import arcade
import arcade.gui

import src.views.start_view as StartView

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Signed Explorations"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True) #fullscreen = True resizable = True
    start_view = StartView.StartView() #StartView() #game.GameView() 
    start_view.setup()
    window.show_view(start_view)
    arcade.run() 

if __name__ == "__main__":
    main()

