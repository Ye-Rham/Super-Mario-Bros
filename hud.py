from pygame.sprite import Sprite


class HUD(Sprite):
    def __init__(self, settings, screen, spritesheet, font):
        super(HUD, self).__init__()
        self.settings = settings
        self.screen = screen

        self.image_rects0 = ((0, 160, 8, 8), (8, 160, 8, 8), (16, 160, 8, 8))
        self.image_rects1 = ((144, 160, 8, 8), (152, 160, 8, 8), (160, 160, 8, 8))

        self.coin_sprites0 = spritesheet.images_at(self.image_rects0, self.settings.scale["pixel_width"] * 8,
                                                   self.settings.scale["pixel_height"] * 8,
                                                   colorkey=self.settings.bg_color[0])
        self.coin_sprites1 = spritesheet.images_at(self.image_rects1, self.settings.scale["pixel_width"] * 8,
                                                   self.settings.scale["pixel_height"] * 8,
                                                   colorkey=self.settings.bg_color[0])

        self.font = font
        self.rect = self.font["0"].get_rect()
        self.rect.x = self.settings.scale["pixel_width"] * 24
        self.rect.y = self.settings.scale["pixel_width"] * 8

        self.score = 0
        self.coin_count = 0
        self.countdown = None
        self.lives = 3
        self.level = "1-1"
        self.mario = "MARIO"
        self.world = "WORLD"
        self.time = "TIME"
        self.gameover = "GAME OVER"

    def reset(self):
        self.score = 0
        self.score = 0
        self.coin_count = 0
        self.countdown = None
        self.lives = 3

    def draw(self, level_type, global_frame):
        # Score display
        for x in range(0, len(self.mario)):
            self.screen.blit(self.font[self.mario[x]], self.rect.move(self.settings.scale["pixel_width"] * 8 * x, 0))
        for x in range(0, 6):
            if x < 6 - len(str(self.score)):
                self.screen.blit(self.font["0"], self.rect.move(self.settings.scale["pixel_width"] * 8 * x,
                                                                self.settings.scale["pixel_height"] * 8))
            else:
                self.screen.blit(self.font[str(self.score)[x - (6 - len(str(self.score)))]],
                                 self.rect.move(self.settings.scale["pixel_width"] * 8 * x,
                                 self.settings.scale["pixel_height"] * 8))
        # Coin display
        if level_type == 0:
            self.screen.blit(self.coin_sprites0[global_frame], self.rect.move(self.settings.scale["pixel_width"] * 64,
                                                                              self.settings.scale["pixel_height"] * 8))
        else:
            self.screen.blit(self.coin_sprites1[global_frame], self.rect.move(self.settings.scale["pixel_width"] * 64,
                                                                              self.settings.scale["pixel_height"] * 8))
        self.screen.blit(self.font["x"], self.rect.move(self.settings.scale["pixel_width"] * 72,
                                                        self.settings.scale["pixel_height"] * 8))
        for x in range(0, 2):
            if x < 2 - len(str(self.coin_count)):
                self.screen.blit(self.font["0"], self.rect.move(self.settings.scale["pixel_width"] * (80 + 8 * x),
                                                                self.settings.scale["pixel_height"] * 8))
            else:
                self.screen.blit(self.font[str(self.coin_count)[x - (2 - len(str(self.coin_count)))]],
                                 self.rect.move(self.settings.scale["pixel_width"] * (80 + 8 * x),
                                 self.settings.scale["pixel_height"] * 8))
        # World display
        for x in range(0, len(self.world)):
            self.screen.blit(self.font[self.world[x]], self.rect.move(self.settings.scale["pixel_width"] *
                                                                      (120 + 8 * x), 0))
        for x in range(0, len(self.level)):
            self.screen.blit(self.font[self.level[x]], self.rect.move(self.settings.scale["pixel_width"] *
                                                                      (128 + 8 * x),
                                                                      self.settings.scale["pixel_height"] * 8))
        # Time display
        for x in range(0, len(self.time)):
            self.screen.blit(self.font[self.time[x]], self.rect.move(self.settings.scale["pixel_width"] *
                                                                     (176 + 8 * x), 0))
        if self.countdown is not None:
            for x in range(0, 3):
                if x < 3 - len(str(self.countdown)):
                    self.screen.blit(self.font["0"], self.rect.move(self.settings.scale["pixel_width"] * (184 + 8 * x),
                                                                    self.settings.scale["pixel_height"] * 8))
                else:
                    self.screen.blit(self.font[str(self.countdown)[x - (3 - len(str(self.countdown)))]],
                                     self.rect.move(self.settings.scale["pixel_width"] * (184 + 8 * x),
                                                    self.settings.scale["pixel_height"] * 8))

    def draw_lives_screen(self, mario):
        if self.lives > 0:
            for x in range(0, len(self.world)):
                self.screen.blit(self.font[self.world[x]], self.rect.move(self.settings.scale["pixel_width"] *
                                                                          (64 + 8 * x),
                                                                          self.settings.scale["pixel_height"] * 80))
            for x in range(0, len(self.level)):
                self.screen.blit(self.font[self.level[x]], self.rect.move(self.settings.scale["pixel_width"] *
                                                                          (112 + 8 * x),
                                                                          self.settings.scale["pixel_height"] * 80))
            rect = mario.image_list_small[0].get_rect()
            rect.x = self.rect.x + self.settings.scale["pixel_width"] * 72
            rect.y = self.rect.y + self.settings.scale["pixel_height"] * 104
            self.screen.blit(mario.image_list_small[0], rect)
            self.screen.blit(self.font["x"], self.rect.move(self.settings.scale["pixel_width"] * 96,
                                                            self.settings.scale["pixel_height"] * 112))
            for x in range(0, 2):
                if x < 2 - len(str(self.lives)):
                    self.screen.blit(self.font["0"], self.rect.move(self.settings.scale["pixel_width"] * (112 + 8 * x),
                                                                    self.settings.scale["pixel_height"] * 112))
                else:
                    self.screen.blit(self.font[str(self.lives)[x - len(str(self.lives))]],
                                     self.rect.move(self.settings.scale["pixel_width"] * (112 + 8 * x),
                                     self.settings.scale["pixel_height"] * 112))
        else:
            for x in range(0, len(self.gameover)):
                if self.gameover[x] != " ":
                    self.screen.blit(self.font[self.gameover[x]],
                                     self.rect.move(self.settings.scale["pixel_width"] * (64 + 8 * x),
                                                    self.settings.scale["pixel_height"] * 112))
