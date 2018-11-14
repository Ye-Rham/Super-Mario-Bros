from pygame.sprite import Sprite


class StartMenu(Sprite):
    def __init__(self, settings, screen, spritesheet, font):
        super(StartMenu, self).__init__()
        self.settings = settings
        self.screen = screen
        self.font = font

        self.sprite_rects = ((1, 60, 176, 88), (3, 155, 8, 8))
        self.sprite0 = spritesheet.image_at(self.sprite_rects[0], self.settings.scale["pixel_width"] * 176,
                                            self.settings.scale["pixel_height"] * 88,
                                            colorkey=self.settings.bg_color[0])
        self.sprite1 = spritesheet.image_at(self.sprite_rects[1], self.settings.scale["pixel_width"] * 8,
                                            self.settings.scale["pixel_height"] * 8,
                                            colorkey=self.settings.bg_color[0])
        self.rect1 = self.sprite0.get_rect()
        self.rect1.x = self.settings.scale["pixel_width"] * 40
        self.rect1.y = self.settings.scale["pixel_height"] * 24
        self.rect2 = self.sprite1.get_rect()
        self.rect2.x = self.settings.scale["pixel_width"] * 72
        self.rect2.y = self.settings.scale["pixel_height"] * 144

        self.high_score_file = open("High_Scores.txt", "r")
        self.high_score_list = []
        for line in self.high_score_file:
            self.high_score_list.append(int(line))
        self.high_score_file.close()
        if self.high_score_list:
            self.high_score = self.high_score_list[0]
        else:
            self.high_score = 0

        self.selection = True  # True = PLAY GAME, False = HIGH SCORES
        self.playgame = "PLAY GAME"
        self.highscores = "HIGH SCORES"
        self.back = "BACK"

        self.playgame_select = False
        self.highscore_select = False

        self.inactive_timer = 0

    def draw(self, x_offset):
        if not self.highscore_select:
            self.screen.blit(self.sprite0, self.rect1.move(x_offset, 0))
            for x in range(0, len(self.playgame)):
                if self.playgame[x] != " ":
                    self.screen.blit(self.font[self.playgame[x]],
                                     self.rect2.move(self.settings.scale["pixel_width"] * (16 + 8 * x), 0))
            for x in range(0, len(self.highscores)):
                if self.highscores[x] != " ":
                    self.screen.blit(self.font[self.highscores[x]],
                                     self.rect2.move(self.settings.scale["pixel_width"] * (16 + 8 * x),
                                                     self.settings.scale["pixel_height"] * 16))
            if self.selection:
                self.screen.blit(self.sprite1, self.rect2.move(x_offset, 0))
            else:
                self.screen.blit(self.sprite1, self.rect2.move(x_offset, self.settings.scale["pixel_height"] * 16))
        else:
            for x in range(0, len(self.back)):
                self.screen.blit(self.font[self.back[x]],
                                 self.rect2.move(self.settings.scale["pixel_width"] * (16 + 8 * x),
                                                 self.settings.scale["pixel_height"] * 32))
            for line in range(0, len(self.high_score_list)):
                self.screen.blit(self.font[str(line + 1)], self.rect2.move(0, self.settings.scale["pixel_height"] *
                                                                           (-112 + 16 * line)))
                self.screen.blit(self.sprite1, self.rect2.move(x_offset, self.settings.scale["pixel_height"] * 32))
                for x in range(0, 6):
                    if x < 6 - len(str(self.high_score_list[line])):
                        self.screen.blit(self.font["0"], self.rect2.move(self.settings.scale["pixel_width"] *
                                                                         (16 + 8 * x),
                                                                         self.settings.scale["pixel_height"] *
                                                                         (-112 + 16 * line)))
                    else:
                        self.screen.blit(self.font[str(self.high_score_list[line])
                                         [x - (6 - len(str(self.high_score_list[line])))]],
                                         self.rect2.move(self.settings.scale["pixel_width"] * (16 + 8 * x),
                                                         self.settings.scale["pixel_height"] * (-112 + 16 * line)))
