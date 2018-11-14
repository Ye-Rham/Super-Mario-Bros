import pygame
from pygame.sprite import Group
import sys

from game_settings import Settings
from sprite_sheet import SpriteSheet
from map import Map
from camera import Camera
from hud import HUD
from start_menu import StartMenu
from mario import Mario


def run_game():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/01-main-theme-overworld.mp3')
    mario_jump = pygame.mixer.Sound('sounds/Jump.wav')

    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Super Mario Bros")
    mario_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Mario & Luigi.png", screen)
    tile_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Tileset.png", screen)
    item_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Items & Objects.png", screen)
    enemy_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Enemies & Bosses.png", screen)
    font_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Time Up Game Over Screens and Text.png", screen)
    title_spritesheet = SpriteSheet("images/NES - Super Mario Bros - Title Screen.png", screen)
    tilesets = []
    block_content_sprites = []
    score_sprites = []
    enemy_sprites = []
    font = initialize_font(settings, font_spritesheet)
    initialize_tilesets(settings, tile_spritesheet, tilesets)
    initialize_animated_item_sprites(settings, item_spritesheet, block_content_sprites)
    initialize_enemy_sprites(settings, enemy_spritesheet, enemy_sprites)

    camera = Camera(settings)
    hud = HUD(settings, screen, item_spritesheet, font)
    startmenu = StartMenu(settings, screen, title_spritesheet, font)
    mario = Mario(settings, screen, mario_spritesheet)
    mario_group = Group()
    mario_group.add(mario)
    background = Group()
    foreground = Group()
    blocks = Group()
    hidden_blocks = Group()
    coins = Group()
    block_contents = Group()
    flagpole = Group()
    enemies = Group()
    level_1_1 = Map(settings, screen, "level_maps/1-1 Overworld.txt", tilesets[0], camera)
    level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins, enemies, enemy_sprites,
                             mario)

    timer = pygame.time.Clock()
    time = 1

    while True:
        timer.tick(60)
        time += 1
        if time == 61:
            time = 1

        check_events(mario, startmenu, mario_jump)
        mario.update(mario_group, foreground, blocks)
        for enemy in enemies:
            enemy.update()
        camera.camera_tracking(mario)
        level_1_1.sprite_cycler(camera, background, foreground, blocks, hidden_blocks, coins, block_contents,
                                enemies, enemy_sprites, flagpole)
        camera.update_screen(screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks, coins, mario,
                             block_contents, enemies, flagpole)
        if startmenu.playgame_select:
            while startmenu.playgame_select:
                pygame.mixer.music.play()
                camera.lives_screen = True
                camera.global_frame = 0
                camera.update_screen(screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks, coins,
                                     mario, block_contents, enemies, flagpole)
                reset_sprites(background, foreground, blocks, hidden_blocks, coins, block_contents, enemies, flagpole)
                level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins, enemies,
                                         enemy_sprites, mario)
                hud.countdown = 400
                while not camera.lives_screen:
                    timer.tick(60)
                    time += 1
                    if time == 61:
                        time = 1
                    check_events(mario, startmenu, mario_jump)
                    if time % 60 == 0:
                        hud.countdown -= 1
                    mario.update(mario_group, foreground, blocks)
                    for enemy in enemies:
                        enemy.update()
                    camera.camera_tracking(mario)
                    level_1_1.sprite_cycler(camera, background, foreground, blocks, hidden_blocks, coins,
                                            block_contents, enemies, enemy_sprites, flagpole)
                    camera.update_screen(screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks,
                                         coins, mario, block_contents, enemies, flagpole)


def check_events(mario, startmenu, mario_jump):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if startmenu.playgame_select:
                    mario.change_sprite_image_direction('right')
                    mario.right_key_down = True

            if event.key == pygame.K_LEFT:
                if startmenu.playgame_select:
                    mario.change_sprite_image_direction('left')
                    mario.left_key_down = True
            if event.key == pygame.K_SPACE:
                if startmenu.playgame_select:
                    mario.jump()
                    mario_jump.play()
                elif not startmenu.selection:
                    if not startmenu.highscore_select:
                        startmenu.highscore_select = True
                    else:
                        startmenu.highscore_select = False
                else:
                    startmenu.playgame_select = True
            if event.key == pygame.K_UP and not startmenu.selection and not startmenu.highscore_select:
                startmenu.selection = True
            if event.key == pygame.K_DOWN:
                if startmenu.playgame_select:
                    # mario crouch
                    placeholder = "placeholder"
                elif startmenu.selection:
                    startmenu.selection = False


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if startmenu.playgame_select:
                    mario.change_sprite_image_direction('still')
                    mario.right_key_down = False
                    #mario.moving_right = False
            if event.key == pygame.K_LEFT:
                if startmenu.playgame_select:
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

    tilesets.append(spritesheet.images_at(tileset1_rects, settings.scale["tile_width"], settings.scale["tile_height"],
                    colorkey=settings.bg_color[0]))
    tilesets.append(spritesheet.images_at(tileset2_rects, settings.scale["tile_width"], settings.scale["tile_height"],
                                          colorkey=settings.bg_color[0]))


def initialize_animated_item_sprites(settings, item_spritesheet, block_content_sprites):
    coin_image_rects = ((0, 112, 16, 16), (16, 112, 16, 16), (32, 112, 16, 16), (48, 112, 16, 16))
    brick_image_rects = ((64, 0, 8, 8), (72, 0, 8, 8), (64, 8, 8, 8), (72, 8, 8, 8))
    block_content_sprites.append(item_spritesheet.images_at(coin_image_rects, settings.scale["tile_width"],
                                                            settings.scale["tile_height"],
                                                            colorkey=settings.bg_color[0]))
    block_content_sprites.append(item_spritesheet.images_at(brick_image_rects, settings.scale["tile_width"]/4,
                                                            settings.scale["tile_height"]/4,
                                                            colorkey=settings.bg_color[0]))


def initialize_enemy_sprites(settings, enemy_spritesheet, enemy_sprites):
    goomba_image_rects = ((0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16))
    koopa_image_rects = ((96, 8, 16, 24), (112, 8, 16, 24), (160, 8, 16, 24), (176, 8, 16, 24))
    enemy_sprites.append(enemy_spritesheet.images_at(goomba_image_rects, settings.scale["tile_width"],
                                                     settings.scale["tile_height"], colorkey=settings.bg_color[0]))
    enemy_sprites.append(enemy_spritesheet.images_at(koopa_image_rects, settings.scale["tile_width"],
                                                     settings.scale["tile_height"]*3/2, colorkey=settings.bg_color[0]))


def initialize_font(settings, font_spritesheet):
    font_rects = []
    for y in range(0, 2):
        for x in range(0, 16):
            font_rects.append((3 + x * 8, 460 + y * 8, 8, 8))
    for x in range(0, 4):
        font_rects.append((3 + x * 8, 476, 8, 8))
    font_rects.append((67, 476, 8, 8))
    font_rects.append((75, 476, 8, 8))
    font_sprites = font_spritesheet.images_at(font_rects, settings.scale["tile_width"]/2,
                                              settings.scale["tile_height"]/2, colorkey=settings.bg_color[0])
    return {"0": font_sprites[0], "1": font_sprites[1], "2": font_sprites[2], "3": font_sprites[3],
            "4": font_sprites[4], "5": font_sprites[5], "6": font_sprites[6], "7": font_sprites[7],
            "8": font_sprites[8], "9": font_sprites[9], "A": font_sprites[10], "B": font_sprites[11],
            "C": font_sprites[12], "D": font_sprites[13], "E": font_sprites[14], "F": font_sprites[15],
            "G": font_sprites[16], "H": font_sprites[17], "I": font_sprites[18], "J": font_sprites[19],
            "K": font_sprites[20], "L": font_sprites[21], "M": font_sprites[22], "N": font_sprites[23],
            "O": font_sprites[24], "P": font_sprites[25], "Q": font_sprites[26], "R": font_sprites[27],
            "S": font_sprites[28], "T": font_sprites[29], "U": font_sprites[30], "V": font_sprites[31],
            "W": font_sprites[32], "X": font_sprites[33], "Y": font_sprites[34], "Z": font_sprites[35],
            "-": font_sprites[36], "x": font_sprites[37]}


def reset_sprites(background, foreground, blocks, hidden_blocks, coins, block_contents, enemies, flagpole):
    for sprite in background:
        sprite.kill()
    for sprite in foreground:
        sprite.kill()
    for sprite in blocks:
        sprite.kill()
    for sprite in hidden_blocks:
        sprite.kill()
    for sprite in coins:
        sprite.kill()
    for sprite in block_contents:
        sprite.kill()
    for sprite in enemies:
        sprite.kill()
    for sprite in flagpole:
        sprite.kill()


run_game()
