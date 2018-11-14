import pygame
from animations import Popcoin
from animations import Brokebricks
from enemies import Goomba
from enemies import GreenKoopa
from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, settings, screen, sprite, x, y, animated, block_type):
        super(Tile, self).__init__()
        self.settings = settings
        self.screen = screen
        self.tile_sprite = sprite
        self.rect = pygame.Rect(0, 0, settings.scale["tile_width"], settings.scale["tile_height"])
        self.rect.x = x * settings.scale["tile_width"]
        self.rect.y = y * settings.scale["tile_height"] + settings.scale["tile_height"] * 1.5

        self.active = True  # Boolean variable for interactive blocks
        self.animated = animated  # Boolean variable for animated objects
        self.frame = 0
        self.block_type = block_type  # 0 = ? Block Coin, 1 = ? Block Powerup, 2 = Breakable Bricks, 3 = Coin Bricks,
        # 4 = Star Bricks, 5 = Hidden 1UP
        self.time = 3000 # Time that the coins brick block stays active after hit
        self.countdown = False # Check when mario hits coins brick block
        self.y_offset = 0 # For block_push_animation
        self.fall = False # For block_push_animation

    def draw(self, x_offset, global_frame):
        if not isinstance(self.tile_sprite, list) and not self.block_type == 5:
            self.screen.blit(self.tile_sprite, self.rect.move(x_offset, self.y_offset))
        elif not self.block_type == 5 and self.active and self.animated:
            self.screen.blit(self.tile_sprite[global_frame], self.rect.move(x_offset, self.y_offset))
        elif not self.block_type == 5 and self.active:
            self.screen.blit(self.tile_sprite[0], self.rect.move(x_offset, self.y_offset))
        elif not self.block_type == 5 and not self.active:
            self.screen.blit(self.tile_sprite[len(self.tile_sprite)], self.rect.move(x_offset, self.y_offset))
        elif self.block_type == 5 and not self.active:
            self.screen.blit(self.tile_sprite, self.rect.move(x_offset, self.y_offset))

    def block_push_animation(self):
        if not self.fall:
            self.y_offset += 1
            if self.y_offset == 4:
                self.y_offset -= 2
                self.fall = True
        elif self.y_offset > 0:
            self.y_offset -= 1
            if self.y_offset == 0 and not self.active:
                self.frame = len(self.tile_sprite)

    def block_reaction(self, block_content_sprites, block_contents):
        # Pushes out the contents of the block
        if self.block_type == 0:
            newpopcoin = Popcoin(self.settings, self.screen, block_content_sprites[0], self.rect.x, self.rect.top)
            block_contents.add(newpopcoin)
            self.block_push_animation()
            self.active = False
        elif self.block_type == 1:
            self.block_push_animation()
            # spawn_powerup()
            self.active = False
        elif self.block_type == 2:
            if True: # mario is big
                newbrokebricks = Brokebricks(self.settings, self.screen, block_content_sprites[1], self.rect.center)
                block_contents.add(newbrokebricks)
                self.kill()
            else:
                self.block_push_animation()
        elif self.block_type == 3:
            if self.countdown:
                newpopcoin = Popcoin(self.settings, self.screen, block_content_sprites[0], self.rect.x, self.rect.top)
                block_contents.add(newpopcoin)
                self.block_push_animation()
                if self.time == 0:
                    self.active = False
            else:
                newpopcoin = Popcoin(self.settings, self.screen, block_content_sprites[0], self.rect.x, self.rect.top)
                block_contents.add(newpopcoin)
                self.block_push_animation()
                self.countdown = True

        elif self.block_type == 4:
            self.block_push_animation()
            # spawn_star()
            self.active = False
        elif self.block_type == 5:
            self.block_push_animation()
            # spawn_1up()
            self.active = False

    @staticmethod
    def expire_time(bricks):
        for brick in bricks:
            if brick.countdown and brick.active and brick.time > 0:
                brick.time -= 1


class Map:
    def __init__(self, settings, screen, mapfile, tileset, camera):
        self.settings = settings
        self.screen = screen
        self.textmap = open(mapfile, "r")
        self.mapmatrix = []
        for line in self.textmap:  # Initiation of map coordinates
            newlist = line.split()
            self.mapmatrix.append(newlist)
        self.textmap.close()
        self.tileset = tileset  # Separate tilesets for levels

        camera.cap = len(self.mapmatrix[0]) - 1

    def initialize_map(self, camera, background, foreground, blocks, hidden_blocks, coins, enemies, enemy_sprites,
                       mario):
        x_length = camera.milestone + 1
        if x_length > camera.cap:
            x_length = camera.cap
        for y in range(len(self.mapmatrix)):
            for x in range(x_length + 1):
                if self.mapmatrix[y][x][0] == "G":
                    newtile = Tile(self.settings, self.screen, self.tileset[0 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    foreground.add(newtile)
                elif self.mapmatrix[y][x][0] == "P":
                    newtile = Tile(self.settings, self.screen, self.tileset[56 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    foreground.add(newtile)
                elif self.mapmatrix[y][x][0] == "M":
                    newtile = Tile(self.settings, self.screen, self.tileset[72 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "C":
                    newtile = Tile(self.settings, self.screen, self.tileset[90 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    coins.add(newtile)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "S":
                    newtile = Tile(self.settings, self.screen, self.tileset[78 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "F":
                    newtile = Tile(self.settings, self.screen, self.tileset[24 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "?":
                    newtile = Tile(self.settings, self.screen, self.tileset[48:55:2],
                                   x, y, True,  int(self.mapmatrix[y][x][1]))
                    blocks.add(newtile)
                elif self.mapmatrix[y][x][0] == "B":
                    newtile = Tile(self.settings, self.screen, self.tileset[2:6:4], x, y,
                                   False,  int(self.mapmatrix[y][x][1]) + 2)
                    blocks.add(newtile)
                elif self.mapmatrix[y][x][0] == "H":
                    newtile = Tile(self.settings, self.screen, self.tileset[55], x, y,
                                   False,  int(self.mapmatrix[y][x][1]) + 5)
                    hidden_blocks.add(newtile)
                elif self.mapmatrix[y][x][0] == "I":
                    newtile = Tile(self.settings, self.screen, self.tileset[49:54:2],
                                   x, y, True,  None)
                    coins.add(newtile)
                if len(self.mapmatrix[y][x - 8]) == 3:
                    if self.mapmatrix[y][x - 8][2] == "G":
                        newenemy = Goomba(self.settings, self.screen, enemy_sprites[0], x, y)
                        enemies.add(newenemy)
                    elif self.mapmatrix[y][x - 8][2] == "K":
                        newenemy = GreenKoopa(self.settings, self.screen, enemy_sprites[1], x, y)
                        enemies.add(newenemy)
                    elif self.mapmatrix[y][x - 8][2] == "M":
                        mario.rect.x = self.settings.scale["tile_width"] * (x - 8) + \
                                       self.settings.scale["tile_width"] / 2
                        mario.rect.y = self.settings.scale["tile_height"] * y + self.settings.scale["tile_width"] / 2

    def sprite_cycler(self, camera, background, foreground, blocks, hidden_blocks, coins, block_contents, enemies,
                      enemy_sprites, flagpole):
        for tile in background:
            if tile.rect.x <= camera.rect.x - self.settings.screen_width/2:
                tile.kill()
        for tile in foreground:
            if tile.rect.x <= camera.rect.x - self.settings.screen_width/2:
                tile.kill()
        for tile in blocks:
            if tile.rect.x <= camera.rect.x - self.settings.screen_width/2:
                tile.kill()
        for tile in hidden_blocks:
            if tile.rect.x <= camera.rect.x - self.settings.screen_width/2:
                tile.kill()
        for entity in coins:
            if entity.rect.x <= camera.rect.x - self.settings.screen_width/2:
                entity.kill()
        for sprite in block_contents:
            if isinstance(sprite, Popcoin):
                if sprite.frame == 9:
                    sprite.kill()
            if isinstance(sprite, Brokebricks):
                if sprite.left_rect1.y > self.settings.screen_height:
                    sprite.kill()
        if int((camera.rect.right + camera.rect.width/2)/self.settings.scale["tile_width"]) > camera.milestone \
                and camera.milestone < camera.cap:
            camera.milestone = int((camera.rect.right + camera.rect.width/2)/self.settings.scale["tile_width"])
            x = camera.milestone
            for y in range(len(self.mapmatrix)):
                if self.mapmatrix[y][x][0] == "G":
                    newtile = Tile(self.settings, self.screen, self.tileset[0 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    foreground.add(newtile)
                elif self.mapmatrix[y][x][0] == "P":
                    newtile = Tile(self.settings, self.screen, self.tileset[56 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    foreground.add(newtile)
                elif self.mapmatrix[y][x][0] == "M":
                    newtile = Tile(self.settings, self.screen, self.tileset[72 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "C":
                    newtile = Tile(self.settings, self.screen, self.tileset[90 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "S":
                    newtile = Tile(self.settings, self.screen, self.tileset[78 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "F":
                    newtile = Tile(self.settings, self.screen, self.tileset[22 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "?":
                    newtile = Tile(self.settings, self.screen, self.tileset[48:55:2],
                                   x, y, True,  int(self.mapmatrix[y][x][1]))
                    blocks.add(newtile)
                elif self.mapmatrix[y][x][0] == "B":
                    newtile = Tile(self.settings, self.screen, self.tileset[2:6:4], x, y,
                                   False,  int(self.mapmatrix[y][x][1]) + 2)
                    blocks.add(newtile)
                elif self.mapmatrix[y][x][0] == "H":
                    newtile = Tile(self.settings, self.screen, self.tileset[55], x, y,
                                   False,  int(self.mapmatrix[y][x][1]) + 5)
                    hidden_blocks.add(newtile)
                elif self.mapmatrix[y][x][0] == "IC":
                    newtile = Tile(self.settings, self.screen, self.tileset[49:54:2],
                                   x, y, True,  None)
                    coins.add(newtile)
                elif self.mapmatrix[y][x][0] == "E":
                    newtile = Tile(self.settings, self.screen, self.tileset[88 + int(self.mapmatrix[y][x][1])],
                                   x, y, False, None)
                    flagpole.add(newtile)
                if len(self.mapmatrix[y][x - 8]) == 3:
                    if self.mapmatrix[y][x - 8][2] == "G":
                        newenemy = Goomba(self.settings, self.screen, enemy_sprites[0], x-8, y)
                        enemies.add(newenemy)
                    elif self.mapmatrix[y][x - 8][2] == "K":
                        newenemy = GreenKoopa(self.settings, self.screen, enemy_sprites[1], x-8, y)
                        enemies.add(newenemy)
