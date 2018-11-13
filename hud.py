from pygame.sprite import Sprite


class HUD(Sprite):
    def __init__(self, settings, screen, spritesheet, font_sprites):
        self.settings = settings
        self.screen = screen

        self.font = {"0": font_sprites[0], "1": font_sprites[1], "2": font_sprites[2], "3": font_sprites[3],
                     "4": font_sprites[4], "5": font_sprites[5], "6": font_sprites[6], "7": font_sprites[7],
                     "8": font_sprites[8], "9": font_sprites[9], "A": font_sprites[10], "B": font_sprites[11],
                     "C": font_sprites[12], "D": font_sprites[13], "E": font_sprites[14], "F": font_sprites[15],
                     "G": font_sprites[16], "H": font_sprites[17], "I": font_sprites[18], "J": font_sprites[19],
                     "K": font_sprites[20], "L": font_sprites[21], "M": font_sprites[22], "N": font_sprites[23],
                     "O": font_sprites[24], "P": font_sprites[25], "Q": font_sprites[26], "R": font_sprites[27],
                     "S": font_sprites[28], "T": font_sprites[29], "U": font_sprites[30], "V": font_sprites[31],
                     "W": font_sprites[32], "X": font_sprites[33], "Y": font_sprites[34], "Z": font_sprites[35],
                     "-": font_sprites[36], "x": font_sprites[37]}

        self.score = 0
        self.coin_count = 0
        self.time = None
        self.lives = 3
        self.level = "1-1"
