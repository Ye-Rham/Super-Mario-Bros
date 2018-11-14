from pygame.sprite import Sprite


class PointsSprite(Sprite):
    def __init__(self, settings, screen, font, x, y, points_value):
        super(PointsSprite, self).__init__()
        self.settings = settings
        self.screen = screen
        self.font = font

        if points_value != 0:
            self.rect = self.font["0"].get_rect()
        else:
            self.rect = self.font["1UP"].get_rect()
        self.rect.x = x
        self.rect.y = y

        self.points_value = points_value
        self.expiration = 60

    def draw(self, x_offset):
        if self.points_value != 0:
            for x in range(0, len(str(self.points_value))):
                self.screen.blit(self.font[str(self.points_value)[x]],
                                 self.rect.move(x_offset + x * self.settings.scale["pixel_width"] * 4, 0))
        else:
            self.screen.blit(self.font["1UP"], self.rect.move(x_offset, 0))
        self.rect.y -= self.settings.scale["pixel_height"]
        self.expiration -= 1
        if self.expiration <= 0:
            self.kill()
