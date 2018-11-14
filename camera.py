import pygame
from time import sleep


class Camera:
    def __init__(self, settings):
        self.settings = settings

        self.rect = pygame.Rect(0, 0, self.settings.screen_width, self.settings.screen_height)
        self.x_offset = 0
        self.milestone = int((self.rect.right + self.rect.width/2)/self.settings.scale["tile_width"])
        # map generation goes up to this x
        self.cap = None  # end of level
        self.global_frame = 0
        self.flash = True
        self.flash_count = 0
        self.level_type = 0  # 0 for overworld, 1 for underworld
        self.lives_screen = False

    def camera_tracking(self, mario):
        # Slowly catch the camera location up
        if self.settings.screen_width/4 <= mario.rect.centerx - self.rect.x < self.settings.screen_width/2 and \
                int(self.rect.right/self.settings.scale["tile_width"]) < self.cap and mario.moving_right:
            self.rect.x += mario.x_velocity/2
            if int(self.rect.x/self.settings.scale["tile_width"]) > self.cap:
                self.rect.x = self.cap
            self.x_offset = -self.rect.x

        # Camera is in the right position, move it with mario
        elif mario.rect.centerx - self.rect.x >= self.settings.screen_width/2 and \
                int(self.rect.right/self.settings.scale["tile_width"]) < self.cap and mario.moving_right:
            self.rect.x += mario.x_velocity
            if (self.rect.x/self.settings.scale["tile_width"]) > self.cap:
                self.rect.x = self.cap
            self.x_offset = -self.rect.x

    def set_camera_at_mario(self, mario):
        self.rect.x = mario.rect.x
        self.rect.y = 0

    def update_screen(self, screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks, coins, mario,
                      block_contents, enemies, flagpole):
        if not self.lives_screen:
            screen.fill(self.settings.bg_color[self.level_type])
            self.draw_level(background, foreground, blocks, hidden_blocks, coins, flagpole)
            self.draw_active_objects(block_contents, enemies)
            mario.blitme(self.x_offset)
            if not startmenu.playgame_select:
                startmenu.draw(self.x_offset)
            hud.draw(self.level_type, self.global_frame)

            pygame.display.flip()
        else:
            screen.fill(self.settings.bg_color[1])
            hud.draw(self.level_type, self.global_frame)
            hud.draw_lives_screen(mario)
            pygame.display.flip()
            sleep(3)
            self.lives_screen = False

        self.frame_management(time, block_contents, enemies)

    def draw_level(self, background, foreground, blocks, hidden_blocks, coins, flagpole):
        for tile in background:
            tile.draw(self.x_offset, self.global_frame)
        for tile in foreground:
            tile.draw(self.x_offset, self.global_frame)
        for tile in blocks:
            tile.draw(self.x_offset, self.global_frame)
        for tile in hidden_blocks:
            tile.draw(self.x_offset, self.global_frame)
        for tile in coins:
            tile.draw(self.x_offset, self.global_frame)
        for tile in flagpole:
            tile.draw(self.x_offset, self.global_frame)

    def draw_active_objects(self, block_contents, enemies):
        for sprite in block_contents:
            sprite.draw(self.x_offset)
        for enemy in enemies:
            enemy.draw(self.x_offset)

    def frame_management(self, time, block_contents, enemies):
        for sprite in block_contents:
            sprite.frame += 1
        if self.flash_count < 60:
            self.flash_count += 1
        if time % 10 == 0 and self.flash_count == 60:
            if self.flash:
                self.global_frame += 1
                if self.global_frame > 2:
                    self.global_frame = 1
                    self.flash = False
            elif not self.flash:
                self.global_frame -= 1
                if self.global_frame < 0:
                    self.global_frame = 0
                    self.flash = True
                    self.flash_count = 0
        if time % 10 == 0:
            for enemy in enemies:
                enemy.update_frame()
