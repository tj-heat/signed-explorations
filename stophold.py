self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash = True)
        self.scene.add_sprite_list("Floor")
        self.camera = arcade.Camera(self.window.width, self.window.height)

        self.player_sprite = arcade.Sprite(CAT_PATH, SPRITE_SCALING) #diff might be in scaling, check val
        self.player_sprite.center_x = self.window.width/2
        self.player_sprite.center_y = self.window.height/2
        self.scene.add_sprite("Player", self.player_sprite)

        for x in range(0, self.window.width, SPRITE_SIZE):
            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = SPRITE_SIZE/2
            self.scene.add_sprite("Walls", wall)

            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = self.window.height - SPRITE_SIZE/2
            self.scene.add_sprite("Walls", wall)

        for y in range(SPRITE_SIZE, self.window.height - SPRITE_SIZE, SPRITE_SIZE):
            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = SPRITE_SIZE/2
            wall.center_y = y
            self.scene.add_sprite("Walls", wall)

            wall = arcade.Sprite(STONE_PATH, SPRITE_SCALING)
            wall.center_x = self.window.width - SPRITE_SIZE/2
            wall.center_y = y
            self.scene.add_sprite("Walls", wall)
        