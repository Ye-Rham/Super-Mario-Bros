from pygame.sprite import Sprite
from pygame.transform import flip


class Goomba(Sprite):
    def __init__(self, settings, screen, sprites, x, y):
        super(Goomba, self).__init__()
        self.settings = settings
        self.screen = screen

        self.sprites = sprites
        self.rect = sprites[0].get_rect()
        self.rect.x = x * self.settings.scale["tile_width"]
        self.rect.y = y * self.settings.scale["tile_height"] + self.settings.scale["tile_height"] * 1.5

        self.frame = 0
        self.x_velocity = self.settings.scale["pixel_width"]/3
        self.y_velocity = 0
        self.direction = False  # False = left, True = right
        self.fall = False
        self.alive = True
        self.squish = False  # If mario jumps on goomba, squishes
        self.expire = 0  # Timer for destruction if squished

    def update(self):
        if not self.direction and not self.squish and self.alive:
            self.rect.x -= self.x_velocity
        elif not self.squish:
            self.rect.x += self.x_velocity
        if (self.fall or not self.alive) and not self.squish:
            self.rect.y += self.y_velocity
            if self.rect.y > self.settings.screen_height:
                self.kill()
        elif self.squish:
            self.expire += 1
            if self.expire == 60:
                self.kill()

    def update_frame(self):
        if self.alive:
            if self.frame == 0:
                self.frame += 1
            else:
                self.frame -= 1

    def draw(self, x_offset):
        if self.alive or self.squish:
            self.screen.blit(self.sprites[self.frame], self.rect.move(x_offset, 0))
        else:
            self.screen.blit(flip(self.sprites[self.frame], False, True), self.rect.move(x_offset, 0))


class GreenKoopa(Sprite):
    def __init__(self, settings, screen, sprites, x, y):
        super(GreenKoopa, self).__init__()
        self.settings = settings
        self.screen = screen

        self.sprites = sprites
        self.rect = self.sprites[0].get_rect()
        self.rect.x = x * self.settings.scale["tile_width"]
        self.rect.y = y * self.settings.scale["tile_height"] + self.settings.scale["tile_height"]

        self.frame = 0
        self.x_velocity = self.settings.scale["pixel_width"]/3
        self.x_velocity_kick = self.settings.scale["pixel_width"]*3
        self.y_velocity = 0
        self.direction = False
        self.fall = False
        self.tuck = False  # If mario jumps on koopa, tucks in shell
        self.tuck_timer = 0
        self.alive = True
        self.kicked = False

    def update(self):
        if not self.direction and self.alive:
            if not self.tuck:
                self.rect.x -= self.x_velocity
            elif self.kicked:
                self.rect.x -= self.x_velocity_kick
        elif not self.tuck:
            self.rect.x += self.x_velocity
        elif self.kicked:
            self.rect.x += self.x_velocity_kick
        elif self.tuck:
            self.tuck_timer += 1
            if self.tuck_timer == 3600:
                self.tuck = False
                self.tuck_timer = False
                self.frame = 0
                self.direction = False
        if self.fall or not self.alive:
            self.rect.y += self.y_velocity
            if self.rect.y > self.settings.screen_height:
                self.kill()

    def update_frame(self):
        if not self.tuck and self.alive:
            if self.frame == 0:
                self.frame = 1
            else:
                self.frame = 0
        elif self.tuck and self.tuck_timer > 1800:
            if self.tuck_timer % 10 == 0 and self.tuck_timer % 20 != 0:
                self.frame = 3
            elif self.tuck_timer % 20 == 0 and self.tuck_timer != 3600:
                self.frame = 2

    def draw(self, x_offset):
        if (not self.direction or self.tuck) and self.alive:
            self.screen.blit(self.sprites[self.frame], self.rect.move(x_offset, 0))
        elif self.direction and self.alive:
            self.screen.blit(flip(self.sprites[self.frame], True, False), self.rect.move(x_offset, 0))
        else:
            self.screen.blit(flip(self.sprites[self.frame], False, True), self.rect.move(x_offset, 0))
