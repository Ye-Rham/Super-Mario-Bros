import pygame


class Camera:
    def __init__(self, settings):
        self.settings = settings

        self.rect = pygame.Rect(0, 0, self.settings.screen_width, self.settings.screen_height)
        self.x_offset = 0
        self.milestone = int((self.rect.right + self.rect.width/2)/self.settings.scale["tile_width"])
        # map generation goes up to this x
        self.cap = None  # end of level

    def camera_tracking(self, mario):
        if mario.direction == 'right' and \
                self.settings.screen_width/4 <= mario.rect.centerx - self.rect.x < self.settings.screen_width/2 and \
                int(self.rect.right/self.settings.scale["tile_width"]) < self.cap:
            print(1)
            self.rect.x += mario.movement_speed/2
            if int(self.rect.x/self.settings.scale["tile_width"]) > self.cap:
                self.rect.x = self.cap
            self.x_offset = -self.rect.x
        elif mario.direction == 'right' and mario.rect.centerx - self.rect.x >= self.settings.screen_width/2 and \
                int(self.rect.right/self.settings.scale["tile_width"]) < self.cap:
            self.rect.x += mario.movement_speed
            if (self.rect.x/self.settings.scale["tile_width"]) > self.cap:
                print(self.cap)
                print(self.rect.x)
                self.rect.x = self.cap
            self.x_offset = -self.rect.x
            print(self.x_offset)

    def update_screen(self, screen, background, foreground, blocks, hidden_blocks, coins, mario):
        screen.fill(self.settings.bg_color[0])
        self.draw_level(background, foreground, blocks, hidden_blocks, coins)
        mario.blitme(self.x_offset)

        pygame.display.flip()

    def draw_level(self, background, foreground, blocks, hidden_blocks, coins):
        for tile in background:
            tile.draw(self.x_offset)
        for tile in foreground:
            tile.draw(self.x_offset)
        for tile in blocks:
            tile.draw(self.x_offset)
        for tile in hidden_blocks:
            tile.draw(self.x_offset)
        for tile in coins:
            tile.draw(self.x_offset)

