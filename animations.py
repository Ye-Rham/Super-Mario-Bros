from pygame.sprite import Sprite


class Popcoin(Sprite):
    def __init__(self, settings, screen, sprites, x, bottom):
        super(Popcoin, self).__init__()
        self.screen = screen

        self.sprites = sprites
        self.rect = self.sprites[0].get_rect()
        self.rect.x = x
        self.rect.bottom = bottom

        self.frame = 0
        self.velocity = settings.scale["pixel_height"] * 4
        self.decceleration = settings.scale["pixel_height"] * 1

    def draw(self, x_offset):
        self.screen.blit(self.sprites[self.frame % 4], self.rect.move(x_offset, 0))
        self.rect.y -= self.velocity
        if self.frame % 2 == 0:
            self.velocity -= self.decceleration


class Brokebricks(Sprite):
    def __init__(self, settings, screen, sprites, center):
        super(Brokebricks, self).__init__()
        self.screen = screen

        self.sprites = sprites
        self.left_rect1 = self.sprites[0].get_rect()
        self.left_rect2 = self.sprites[0].get_rect()
        self.right_rect1 = self.sprites[0].get_rect()
        self.right_rect2 = self.sprites[0].get_rect()
        self.left_rect1.bottomright = center
        self.left_rect2.topright = center
        self.right_rect1.bottomleft = center
        self.right_rect2.topleft = center

        self.frame = 0
        self.x_velocity = settings.scale["pixel_width"] * 1
        self.y_velocity1 = settings.scale["pixel_height"] * 4
        self.y_velocity2 = settings.scale["pixel_height"] * 2
        self.decceleration = 1

    def draw(self, x_offset):
        self.screen.blit(self.sprites[self.frame % 4], self.left_rect1.move(x_offset, 0))
        self.screen.blit(self.sprites[self.frame % 4], self.left_rect2.move(x_offset, 0))
        self.screen.blit(self.sprites[self.frame % 4], self.right_rect1.move(x_offset, 0))
        self.screen.blit(self.sprites[self.frame % 4], self.right_rect2.move(x_offset, 0))

        self.left_rect1.x -= self.x_velocity
        self.left_rect1.y -= self.y_velocity1
        self.left_rect2.x -= self.x_velocity
        self.left_rect2.y -= self.y_velocity2
        self.right_rect1.x += self.x_velocity
        self.right_rect1.y -= self.y_velocity1
        self.right_rect2.x += self.x_velocity
        self.right_rect2.y -= self.y_velocity2

        if self.frame % 2 == 0:
            self.velocity -= self.decceleration
