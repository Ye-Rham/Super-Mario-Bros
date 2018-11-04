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
        self.rect.y = 550
        self.floor = 550

        self.direction = 'still'
        self.moving_right = False
        self.moving_left = False

        # Used to figure out which direction to draw the still standing sprite
        self.last_moved_direction = 'right'
        self.step_tracker = 0
        self.walking_index = 0
        self.update_after_frames = 5

        # Mutex used to prevent jumping while already in the air
        self.jump_active = False
        self.y_velocity = 0
        self.gravity = 2
        self.delta_t = 0

        # Movement (internal float, round to int when needed)
        self.physics_multiplyer = 3.0
        self.min_walk_velocity = 0.130 * self.physics_multiplyer
        self.max_walk_speed = 2.900 * self.physics_multiplyer
        self.walking_acceleration = 0.110 * self.physics_multiplyer
        self.walking_deceleration = -0.110 * self.physics_multiplyer
        self.x_velocity = 0

        # What keys are currently down
        self.right_key_down = False
        self.left_key_down = False


    def calculate_changed_velocity(self):
        # Will be called every frame so t = 1
        # vi will be the x_velocity
        # a * t + vi = vf
        final_velocity = 0.0

        # we are accelerating here, check if we have a keydown
        if self.right_key_down:
            if self.x_velocity is 0:
                final_velocity = self.min_walk_velocity
            else:
                final_velocity = self.walking_acceleration * 1 + self.x_velocity
                if final_velocity > self.max_walk_speed:
                    final_velocity = self.max_walk_speed
        elif self.left_key_down:
            if self.x_velocity is 0:
                final_velocity = -self.min_walk_velocity
            else:
                final_velocity = -self.walking_acceleration * 1 + self.x_velocity
                if final_velocity < -self.max_walk_speed:
                    final_velocity = -self.max_walk_speed
        else:
            if self.x_velocity > 0:
                final_velocity = self.walking_deceleration * 1 + self.x_velocity
                if final_velocity < 0:
                    final_velocity = 0
            elif self.x_velocity < 0:
                final_velocity = -self.walking_deceleration * 1 + self.x_velocity
                if final_velocity > 0:
                    final_velocity = 0

        return final_velocity

    def update_velocity(self):

        if self.x_velocity == 0.0:
            self.moving_left = False
            self.moving_right = False
        if self.x_velocity < 0:
            self.moving_left = True
            self.moving_right = False
        if self.x_velocity > 0:
            self.moving_right = True
            self.moving_left = False

        self.x_velocity = self.calculate_changed_velocity()

    def load_image_list(self, image_list, start_x, start_y, x_offset, y_offset,
                        width, height, scale_width, scale_height, number_sprites):
        for i in range(0, number_sprites):
            image_list.append(self.sprite_sheet.image_at((
                start_x + i * x_offset, start_y + i * y_offset, width, height),
                scale_width, scale_height, self.transparent_color))

    def update(self):
        self.update_velocity()


        self.step_tracker += 1
        self.rect.x += self.x_velocity

        if self.step_tracker > 30:
            self.step_tracker = 1

        if self.x_velocity < 0.1 and self.x_velocity > -0.1:
            self.image = self.image_list[0]

            if self.last_moved_direction == 'left':
                self.image = pygame.transform.flip(self.image, True, False)

        else:
            if self.step_tracker == 1:
                self.image = self.image_list[self.walking_index]
                if self.x_velocity < 0 or self.left_key_down is True:
                    self.image = pygame.transform.flip(self.image, True, False)

            if self.step_tracker % self.update_after_frames == 0:
                self.walking_index += 1
                if self.walking_index > 3:
                    self.walking_index = 1
                self.image = self.image_list[self.walking_index]
                if self.x_velocity < 0 or self.left_key_down is True:
                    self.image = pygame.transform.flip(self.image, True, False)
                if self.x_velocity < 0 and self.left_key_down is False and self.right_key_down is True:
                    self.image = self.image_list[self.walking_index]

        if self.jump_active:
            self.delta_t += 1 # where this is time
            self.y_velocity -= self.gravity * self.delta_t / 10
            self.image = self.image_list[5]
            if self.direction == 'left' or self.last_moved_direction == 'left':
                self.image = pygame.transform.flip(self.image, True, False)

        self.rect.y -= self.y_velocity

        if self.rect.y >= self.floor:  # player hits the ground
            self.jump_active = False
            self.y_velocity = 0
            self.delta_t = 0
            self.rect.y = self.floor

    def change_sprite_image_direction(self, new_direction):
        self.last_moved_direction = self.direction
        self.direction = new_direction
        self.step_tracker = 0

    def jump(self):
        if not self.jump_active:
            self.jump_active = True
            self.y_velocity = 20

    def blitme(self, x_offset):
        self.screen.blit(self.image, self.rect.move(x_offset, 0))
