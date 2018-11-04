import pygame
from pygame.sprite import Group
import sys

from game_settings import Settings
from sprite_sheet import SpriteSheet
from map import Map
from camera import Camera
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

    camera = Camera(settings)
    mario = Mario(settings, screen, mario_spritesheet)
    background = Group()
    foreground = Group()
    blocks = Group()
    hidden_blocks = Group()
    coins = Group()
    level_1_1 = Map(settings, screen, "level_maps/1-1 Overworld.txt", tilesets[0], camera)
    level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins)

    timer = pygame.time.Clock()

    while True:
        timer.tick(60)

        check_events(mario)
        mario.update()
        camera.camera_tracking(mario)
        level_1_1.sprite_cycler(camera, background, foreground, blocks, hidden_blocks, coins)
        camera.update_screen(screen, background, foreground, blocks, hidden_blocks, coins, mario)


def check_events(mario):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mario.change_sprite_image_direction('right')
                mario.right_key_down = True
            if event.key == pygame.K_LEFT:
                mario.change_sprite_image_direction('left')
                mario.left_key_down = True
            if event.key == pygame.K_SPACE:
                mario.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                mario.change_sprite_image_direction('still')
                mario.right_key_down = False
                #mario.moving_right = False
            if event.key == pygame.K_LEFT:
                mario.change_sprite_image_direction('still')
                mario.left_key_down = False
                #mario.moving_left = False


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

    tilesets.append(spritesheet.images_at(tileset1_rects, settings.scale["tile_width"], settings.scale["tile_height"]))
    tilesets.append(spritesheet.images_at(tileset2_rects, settings.scale["tile_width"], settings.scale["tile_height"]))


run_game()
