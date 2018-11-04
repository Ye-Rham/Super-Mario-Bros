import pygame
from pygame.sprite import Sprite


class Mario(Sprite):

    def __init__(self, settings, screen, sprite_sheet):
        super(Mario, self).__init__()
        self.settings = settings
        self.screen = screen

        # Sprite Sizes: Big - 16x32, Small - 16x16
        self.sprite_sheet = sprite_sheet
        self.transparent_color = (146, 39, 143)
        self.image_list = []
        self.load_image_list(self.image_list, 80, 0, 17, 0, 16, 32, self.settings.scale["tile_width"],
                             self.settings.scale["tile_height"] * 2, 21)
        self.image = self.image_list[0]

        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300

        self.direction = 'still'
        # Used to figure out which direction to draw the still standing sprite
        self.last_moved_direction = 'right'
        self.step_tracker = 0
        self.walking_index = 0
        self.update_after_frames = 5

        # Mutex used to prevent jumping while already in the air
        self.jump_active = False
        self.y_velocity = 0
        self.gravity = 1.2
        self.delta_t = 0

    def load_image_list(self, image_list, start_x, start_y, x_offset, y_offset,
                        width, height, scale_width, scale_height, number_sprites):
        for i in range(0, number_sprites):
            image_list.append(self.sprite_sheet.image_at((
                start_x + i * x_offset, start_y + i * y_offset, width, height),
                scale_width, scale_height, self.transparent_color))

    def update(self):
        self.step_tracker += 1
        if self.step_tracker > 30:
            self.step_tracker = 1

        if self.direction == 'still':
            self.image = self.image_list[0]

            if self.last_moved_direction == 'left':
                self.image = pygame.transform.flip(self.image, True, False)

        elif self.direction == 'right':
            # self.rect.x += 1

            if self.step_tracker == 1:
                self.image = self.image_list[self.walking_index]

            if self.step_tracker % self.update_after_frames == 0:
                self.walking_index += 1
                if self.walking_index > 3:
                    self.walking_index = 1
                self.image = self.image_list[self.walking_index]

        elif self.direction == 'left':
            # self.rect.x -= 1

            if self.step_tracker == 1:
                self.image = self.image_list[self.walking_index]
                self.image = pygame.transform.flip(self.image, True, False)

            if self.step_tracker % self.update_after_frames == 0:
                self.walking_index += 1
                if self.walking_index > 3:
                    self.walking_index = 1
                self.image = self.image_list[self.walking_index]
                self.image = pygame.transform.flip(self.image, True, False)

        if self.jump_active == True:
            self.delta_t += 1 # where this is time
            self.y_velocity -= self.gravity * self.delta_t / 10
            self.image = self.image_list[5]
            if self.last_moved_direction == 'left':
                self.image = pygame.transform.flip(self.image, True, False)

        self.rect.y -= self.y_velocity
        # player hits the ground
        if self.rect.y >= 300:
            self.jump_active = False
            self.y_velocity = 0
            self.delta_t = 0
            self.rect.y = 300

    def change_direction(self, new_direction):
        self.last_moved_direction = self.direction
        self.direction = new_direction
        self.step_tracker = 0

    def jump(self):
        if not self.jump_active:
            self.jump_active = True
            self.y_velocity = 20

    def blitme(self, x_offset):
        self.screen.blit(self.image, self.rect.move(x_offset, 0))
