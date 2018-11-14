import pygame
import math
from pygame.sprite import Sprite

from enemies import Goomba
from enemies import GreenKoopa
from points_sprite import PointsSprite


class Mario(Sprite):

    def __init__(self, settings, screen, sprite_sheet, warp):
        super(Mario, self).__init__()
        self.settings = settings
        self.screen = screen
        self.warp = warp
        self.warp_count = 0

        # 0 -> dead, 1 -> small mario, 2 -> big mario
        self.health = 1

        # Sprite Sizes: Big - 16x32, Small - 16x16
        self.sprite_sheet = sprite_sheet
        self.transparent_color = (146, 39, 143)
        self.image_list_big = []
        self.image_list_small = []
        self.load_image_list(self.image_list_big, 80, 0, 17, 0, 16, 32, self.settings.scale["tile_width"],
                             self.settings.scale["tile_height"] * 2, 21)
        self.load_image_list(self.image_list_small, 80, 33, 17, 0, 16, 16, self.settings.scale["tile_width"],
                             self.settings.scale["tile_height"], 14)

        self.image = self.image_list_small[0]

        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 552
        self.small_difference = 45

        if self.health == 1:
            self.rect.y += self.small_difference

        self.floor = 1000
        self.natural_floor = 1000

        self.direction = 'still'
        self.moving_right = False
        self.moving_left = False

        # Used to figure out which direction to draw the still standing sprite
        self.last_moved_direction = 'right'
        self.step_tracker = 0
        self.walking_index = 0
        self.update_after_frames = 5

        # Mutex used to prevent jumping while already in the air
        self.jump_active = True
        self.y_velocity = 0
        self.gravity = 1.0
        self.delta_t = 0

        # Movement (internal float, round to int when needed)
        self.physics_multiplyer = 3.0
        self.min_walk_velocity = 0.130 * self.physics_multiplyer
        self.max_walk_speed = 2.900 * self.physics_multiplyer
        self.walking_acceleration = 0.110 * self.physics_multiplyer
        self.walking_deceleration = -0.110 * self.physics_multiplyer
        self.x_velocity = 0
        self.max_y_velocity = 15

        # What keys are currently down
        self.right_key_down = False
        self.left_key_down = False

        # Default block values
        self.block_x = 0
        self.block_width = 10000
        self.block_height = 10000
        self.colliding = False

        self.activate_underworld = False
        self.activate_overworld = False
        self.forced = False

        # Points related values
        self.point_values = (100, 200, 400, 500, 800, 1000, 2000, 4000, 5000, 8000, 0)
        self.jump_counter = 0

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

    def isColliding(self, mario_group, blocks):
        collisions = pygame.sprite.groupcollide(mario_group, blocks, False, False)
        if collisions:
            return True

    def update(self, mario_group, foreground, blocks, hidden_blocks, enemies, points, hud, font, block_contents,
               block_content_sprites, camera, game_sounds, channel1):
        self.update_velocity()

        if not self.activate_overworld and self.settings.current_level == "underworld":
            self.check_overworld()

        if self.activate_underworld:
            self.warp_count += 1
            self.rect.y += 1
            self.warp.play()

            if self.warp_count == 50:
                self.warp_count = 0
                self.activate_underworld = False
                self.settings.current_level = "underworld"

        elif self.activate_overworld:
            self.warp_count += 1
            self.rect.x += 1
            self.warp.play()

            if self.warp_count == 50:
                self.warp_count = 0
                self.activate_overworld = False
                self.settings.current_level = "overworld"

        else:

            self.update_velocity()

            self.step_tracker += 1
            if abs(self.x_velocity) > 1:
                self.rect.x += self.x_velocity
            # Collision Checking
            if self.isColliding(mario_group, foreground) or self.isColliding(mario_group, blocks):
                # Difference between floor and ceiling

                self.rect.x += self.x_velocity * -1 * 2
                self.x_velocity = 0

            if self.step_tracker > 30:
                self.step_tracker = 1

            if self.x_velocity < 0.1 and self.x_velocity > -0.1:
                if self.health == 1:
                    self.image = self.image_list_small[0]
                elif self.health == 2:
                    self.image = self.image_list_big[0]

                if self.last_moved_direction == 'left':
                    self.image = pygame.transform.flip(self.image, True, False)

            else:
                if self.step_tracker == 1:
                    if self.health == 1:
                        self.image = self.image_list_small[self.walking_index]
                    elif self.health == 2:
                        self.image = self.image_list_big[self.walking_index]
                    if self.x_velocity < 0 or self.left_key_down is True:
                        self.image = pygame.transform.flip(self.image, True, False)

                if self.step_tracker % self.update_after_frames == 0:
                    self.walking_index += 1
                    if self.walking_index > 3:
                        self.walking_index = 1
                    if self.health == 1:
                        self.image = self.image_list_small[self.walking_index]
                    elif self.health == 2:
                        self.image = self.image_list_big[self.walking_index]
                    if self.x_velocity < 0 or self.left_key_down is True:
                        self.image = pygame.transform.flip(self.image, True, False)
                    if self.x_velocity < 0 and self.left_key_down is False and self.right_key_down is True:
                        if self.health == 1:
                            self.image = self.image_list_small[self.walking_index]
                        elif self.health == 2:
                            self.image = self.image_list_big[self.walking_index]

            if self.jump_active:
                self.delta_t += 1  # where this is time
                self.y_velocity -= self.gravity * self.delta_t / 20
                if self.y_velocity > self.max_y_velocity:
                    self.y_velocity = self.max_y_velocity
                if self.health == 1:
                    self.image = self.image_list_small[5]
                elif self.health == 2:
                    self.image = self.image_list_big[5]
                self.floor = self.natural_floor
                if self.direction == 'left' or self.last_moved_direction == 'left':
                    self.image = pygame.transform.flip(self.image, True, False)

            self.rect.y -= math.floor(self.y_velocity)

        self.colliding = False

        # if self.isColliding(mario_group, blocks) or self.isColliding(mario_group, foreground):
        #     # check if colliding with bottom or top of block
        #     collisions = pygame.sprite.groupcollide(mario_group, blocks, False, False)
        #     if collisions:
        #         self.colliding = True
        #         for collides in collisions.values():
        #             for collide in collides:
        #                 difference_one = abs(self.rect.top - collide.rect.bottom)
        #                 difference_two = abs(self.rect.bottom - collide.rect.top)
        #                 potential_floor = collide.rect.top - 96
        #                 self.block_width = collide.rect.right - collide.rect.left
        #                 self.block_height = collide.rect.top - collide.rect.bottom
        #                 self.block_x = collide.rect.x
        #
        #     collisions = pygame.sprite.groupcollide(mario_group, foreground, False, False)
        #     if collisions:
        #         #print("Collided!")
        #         #print(self.rect.y)
        #         self.colliding = True
        #         for collides in collisions.values():
        #             for collide in collides:
        #                 difference_one = abs(self.rect.top - collide.rect.bottom)
        #                 difference_two = abs(self.rect.bottom - collide.rect.top)
        #                 potential_floor = collide.rect.top - 96
        #                 self.block_width = collide.rect.right - collide.rect.left
        #                 self.block_height = collide.rect.top - collide.rect.bottom
        #                 self.block_x = collide.rect.x
        #
        #     # collided with bottom
        #     if difference_one < difference_two:
        #         self.delta_t += 40
        #     else:  # collided with top
        #         self.floor = potential_floor
        #
        # if self.rect.y >= self.floor:  # player hits the ground
        #     print("hits ground")
        #     self.jump_active = False
        #     self.y_velocity = 0
        #     self.delta_t = 0
        #     self.rect.y = self.floor
        #     self.jump_counter = 0
        #     if self.health == 1:
        #         self.rect.y += self.small_difference
        #
        # # Only kicks in if above the natural floor
        # if (self.rect.x > (self.block_x + (self.block_width)) + 5 or
        #    self.rect.x < (self.block_x - (self.block_width)) - 5) and self.rect.y < self.natural_floor and self.colliding is False:
        #     # If future you is colliding, skip
        #
        #     self.rect.y += 76
        #     mario_group.add(self)
        #     #self.rect.x += self.block_width / 2

        if self.isColliding(mario_group, blocks) or self.isColliding(mario_group, foreground):
            self.forced = False
            # check if colliding with bottom or top of block
            collisions = pygame.sprite.groupcollide(mario_group, blocks, False, False)
            if collisions:
                self.colliding = True
                for collides in collisions.values():
                    for collide in collides:
                        difference_one = abs(self.rect.top - collide.rect.bottom)
                        difference_two = abs(self.rect.bottom - collide.rect.top)
                        potential_floor = collide.rect.top - 96
                        self.block_width = collide.rect.right - collide.rect.left
                        self.block_height = collide.rect.top - collide.rect.bottom
                        self.block_x = collide.rect.x

            collisions = pygame.sprite.groupcollide(mario_group, foreground, False, False)
            if collisions:
                self.colliding = True
                for collides in collisions.values():
                    for collide in collides:
                        difference_one = abs(self.rect.top - collide.rect.bottom)
                        difference_two = abs(self.rect.bottom - collide.rect.top)
                        potential_floor = collide.rect.top - 96
                        self.block_width = collide.rect.right - collide.rect.left
                        self.block_height = collide.rect.top - collide.rect.bottom
                        self.block_x = collide.rect.x

            # collided with bottom
            if difference_one < difference_two:
                #self.rect.y += math.floor(self.y_velocity)
                self.delta_t += 40
            else:  # collided with top
                self.floor = potential_floor

        if self.rect.y >= self.floor:  # player hits the ground
            self.jump_active = False
            self.y_velocity = 0
            self.delta_t = 0
            self.rect.y = self.floor
            if self.health == 1:
                self.rect.y += self.small_difference

        # Only kicks in if above the natural floor
        if (self.rect.x > (self.block_x + (self.block_width)) + 5 or
            self.rect.x < (self.block_x - (self.block_width)) - 5) and self.rect.y < self.natural_floor \
                and self.colliding is False:
            # If future you is colliding, skip

            self.rect.y += 76
            mario_group.add(self)
            # self.rect.x += self.block_width / 2
            if self.isColliding(mario_group, blocks) or self.isColliding(mario_group, foreground):
                self.future_collide(mario_group, blocks, foreground)
            else:
                self.jump_active = True

            self.rect.y -= 76
            # self.rect.x -= self.block_width / 2

        collisions1 = pygame.sprite.spritecollide(self, enemies, False)
        collisions2 = pygame.sprite.spritecollide(self, blocks, False)
        collisions3 = pygame.sprite.spritecollide(self, hidden_blocks, False)
        for enemy in collisions1:
            if self.jump_active and self.y_velocity < 0 and enemy.alive:
                if isinstance(enemy, Goomba):
                    enemy.squish = True
                    enemy.alive = False
                    enemy.frame = 2
                    hud.score += self.point_values[self.jump_counter]
                    if self.jump_counter == 11:
                        hud.lives += 1
                    newpoints = PointsSprite(self.settings, self.screen, font, enemy.rect.x, enemy.rect.y,
                                             self.point_values[self.jump_counter])
                    points.add(newpoints)
                    if self.jump_counter < 10:
                        self.jump_counter += 1
                    self.y_velocity = 5
                    self.delta_t = 1
                    channel1.play(game_sounds["Squish"])
                    if self.jump_counter == 11:
                        channel1.play(game_sounds["1UP"])
                elif isinstance(enemy, GreenKoopa):
                    if not enemy.tuck:
                        enemy.tuck = True
                        enemy.frame = 2
                        hud.score += self.point_values[self.jump_counter]
                        if self.jump_counter == 11:
                            hud.lives += 1
                        newpoints = PointsSprite(self.settings, self.screen, font, enemy.rect.x, enemy.rect.y,
                                                 self.point_values[self.jump_counter])
                        points.add(newpoints)
                        if self.jump_counter < 10:
                            self.jump_counter += 1
                        self.y_velocity = 5
                        self.delta_t = 1
                        self.rect.bottom = enemy.rect.top
                        channel1.play(game_sounds["Squish"])
                        if self.jump_counter == 10:
                            channel1.play(game_sounds["1UP"])
                    elif enemy.tuck and not enemy.kicked:
                        enemy.kicked = True
                        enemy.tuck_timer = 0
                        if self.last_moved_direction == 'left':
                            enemy.direction = False
                            enemy.rect.right = self.rect.left
                        elif self.last_moved_direction == 'right':
                            enemy.direction = True
                            enemy.rect.left = self.rect.right
                        channel1.play(game_sounds["Kick"])
                    elif enemy.tuck and enemy.kicked:
                        enemy.kicked = False
                        hud.score += self.point_values[self.jump_counter]
                        if self.jump_counter == 10:
                            hud.lives += 1
                        newpoints = PointsSprite(self.settings, self.screen, font, enemy.rect.x, enemy.rect.y,
                                                 self.point_values[self.jump_counter])
                        points.add(newpoints)
                        if self.jump_counter < 10:
                            self.jump_counter += 1
                        self.y_velocity = 5
                        self.delta_t = 1
                        self.rect.bottom = enemy.rect.top
                        channel1.play(game_sounds["Squish"])
                        if self.jump_counter == 10:
                            channel1.play(game_sounds["1UP"])
        for block in collisions2:
            if self.y_velocity > 0 and self.jump_active:
                block.block_reaction(block_content_sprites, block_contents, hud, self, game_sounds, channel1)
                self.rect.y = block.rect.bottom
                self.y_velocity = 0
        for hidden_block in collisions3:
            if self.y_velocity > 0 and self.jump_active:
                hidden_block.block_reaction(block_content_sprites, block_contents, hud, self, game_sounds, channel1)
                self.rect.y = hidden_block.rect.bottom
                self.y_velocity = 0

        if self.rect.x < camera.rect.x:
            self.rect.x = camera.rect.x
            self.x_velocity = 0

    def future_collide(self, mario_group, blocks, foreground):
        collisions = pygame.sprite.groupcollide(mario_group, blocks, False, False)
        if collisions:
            self.colliding = True
            for collides in collisions.values():
                for collide in collides:
                    self.floor = collide.rect.top - 96

        collisions = pygame.sprite.groupcollide(mario_group, foreground, False, False)
        if collisions:
            self.colliding = True
            for collides in collisions.values():
                for collide in collides:
                    self.floor = collide.rect.top - 96

    def check_underworld(self):
        if self.rect.x >= 2825 and self.rect.x <= 2905 and self.rect.y <= 415 and self.rect.y >= 350:
            self.activate_underworld = True

    def check_overworld(self):
        if self.rect.x >= 565 and self.rect.x <= 575 and self.rect.y <= 600 and self.rect.y >= 540:
            self.activate_overworld = True


    def change_sprite_image_direction(self, new_direction):
        self.last_moved_direction = self.direction
        self.direction = new_direction
        self.step_tracker = 0

    def jump(self, game_sounds, channel1):
        if not self.jump_active:
            if self.health == 1:
                channel1.play(game_sounds["Small Jump"])
            elif self.health == 2:
                channel1.play(game_sounds["Big Jump"])
            self.jump_active = True
            self.y_velocity = 20

    def blitme(self, x_offset):
        self.screen.blit(self.image, self.rect.move(x_offset, 0))
