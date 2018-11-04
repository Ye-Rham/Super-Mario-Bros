import pygame
from pygame.sprite import Group
import sys

from game_settings import Settings
from sprite_sheet import SpriteSheet
from map import Map
from mario import Mario


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Super Mario Bros")
    mario_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Mario & Luigi.png", screen)
    tile_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Tileset.png", screen)
    tilesets = []
    initialize_tilesets(settings, tile_spritesheet, tilesets)

    mario = Mario(settings, screen, mario_spritesheet)
    background = Group()
    foreground = Group()
    blocks = Group()
    hidden_blocks = Group()
    coins = Group()
    level_1_1 = Map(settings, screen, "level_maps/1-1 Overworld.txt", tilesets[0])
    level_1_1.build_map(background, foreground, blocks, hidden_blocks, coins)

    timer = pygame.time.Clock()

    while True:
        timer.tick(60)
        check_events(mario)
        update_screen(settings, screen, background, foreground, blocks, hidden_blocks, coins, mario)


def check_events(mario):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mario.change_direction('right')
            if event.key == pygame.K_LEFT:
                mario.change_direction('left')
            if event.key == pygame.K_SPACE:
                mario.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                mario.change_direction('still')
                mario.moving_right = False
                print("not moving right")
            if event.key == pygame.K_LEFT:
                mario.change_direction('still')
                mario.moving_left = False
                print("not moving left")


def initialize_tilesets(settings, spritesheet, tilesets):
    tileset1_rects = []
    tileset2_rects = []
    for x in range(0, 28):
        for y in range(0, 2):
            tileset1_rects.append((x * 16, y * 16, 16, 16))
        for y in range(2, 4):
            tileset2_rects.append((x * 16, y * 16, 16, 16))
    for x in range(0, 17):
        for y in range(8, 10):
            tileset1_rects.append((x * 16, y * 16, 16, 16))
            tileset2_rects.append((x * 16, y * 16, 16, 16))
    for x in range(0, 3):
        for y in range(20, 22):
            tileset1_rects.append((x * 16, y * 16, 16, 16))
            tileset2_rects.append((x * 16, y * 16, 16, 16))

    print(str(len(tileset1_rects)))
    tilesets.append(spritesheet.images_at(tileset1_rects, settings.scale["tile_width"], settings.scale["tile_height"],
                    colorkey=(255, 255, 255)))
    tilesets.append(spritesheet.images_at(tileset2_rects, settings.scale["tile_width"], settings.scale["tile_height"],
                    colorkey=(255, 255, 255)))


def draw_level(background, foreground, blocks, hidden_blocks, coins, mario, settings):
    for tile in background:
        if isOnScreen(mario, settings, tile):
            tile.draw()
    for tile in foreground:
        if isOnScreen(mario, settings, tile):
            tile.draw()
    for tile in blocks:
        if isOnScreen(mario, settings, tile):
            tile.draw()
    for tile in hidden_blocks:
        if isOnScreen(mario, settings, tile):
            tile.draw()
    for tile in coins:
        if isOnScreen(mario, settings, tile):
            tile.draw()

def isOnScreen(mario, settings, tile):
    if tile.rect.x < mario.rect.x - settings.screen_width:
        return False
    if tile.rect.x > mario.rect.x + settings.screen_width:
        return False
    return True

def update_screen(settings, screen, background, foreground, blocks, hidden_blocks, coins, mario):
    screen.fill(settings.bg_color[0])
    draw_level(background, foreground, blocks, hidden_blocks, coins, mario, settings)

    mario.update()
    mario.blitme()

    pygame.display.flip()


run_game()
