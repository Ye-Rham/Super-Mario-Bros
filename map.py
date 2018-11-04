import pygame
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

    def draw(self):
        if not isinstance(self.tile_sprite, list) and not self.block_type == 5:
            self.screen.blit(self.tile_sprite, self.rect)
        elif self.block_type == 5 and not self.active:
            self.screen.blit(self.tile_sprite, self.rect)
        elif not self.block_type == 5:
            self.screen.blit(self.tile_sprite[self.frame], self.rect)


class Map:
    def __init__(self, settings, screen, mapfile, tileset):
        self.settings = settings
        self.screen = screen
        self.textmap = open(mapfile, "r")
        self.mapmatrix = []
        for line in self.textmap:  # Initiation of map coordinates
            newlist = line.split()
            self.mapmatrix.append(newlist)
        self.textmap.close()
        self.tileset = tileset  # Separate tilesets for levels

    def build_map(self, background, foreground, blocks, hidden_blocks, coins):
        for y in range(len(self.mapmatrix)):
            for x in range(len(self.mapmatrix[y])):
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
                    newtile = Tile(self.settings, self.screen, self.tileset[88 + int(self.mapmatrix[y][x][1])], x, y,
                                   False, None)
                    background.add(newtile)
                elif self.mapmatrix[y][x][0] == "?":
                    newtile = Tile(self.settings, self.screen, self.tileset[48:55:2],
                                   x, y, True,  int(self.mapmatrix[y][x][1]))
                    blocks.add(newtile)
                elif self.mapmatrix[y][x][0] == "B":
                    newtile = Tile(self.settings, self.screen, self.tileset[3:7:4], x, y,
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
