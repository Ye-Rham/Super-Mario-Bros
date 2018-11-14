import pygame
from pygame.sprite import Group
import sys

from game_settings import Settings
from sprite_sheet import SpriteSheet
from map import Map
from map import Flag
from camera import Camera
from hud import HUD
from start_menu import StartMenu
from mario import Mario


def run_game():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/01-main-theme-overworld.mp3')
    mario_jump = pygame.mixer.Sound('sounds/Jump.wav')
    warp = pygame.mixer.Sound('sounds/Warp.wav')

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
    enemy_sprites = []
    font = initialize_font(settings, font_spritesheet)
    initialize_tilesets(settings, tile_spritesheet, tilesets)
    points_font = initialize_animated_item_sprites(settings, item_spritesheet, block_content_sprites)
    initialize_enemy_sprites(settings, enemy_spritesheet, enemy_sprites)
    game_sounds = {"Small Jump": pygame.mixer.Sound('sounds/Jump.wav'),
                   "Big Jump": pygame.mixer.Sound('sounds/Big Jump.wav'),
                   "Bump": pygame.mixer.Sound('sounds/Bump.wav'),
                   "Beep": pygame.mixer.Sound('sounds/Beep.wav'),
                   "Break": pygame.mixer.Sound('sounds/Break.wav'),
                   "Coin": pygame.mixer.Sound('sounds/Coin.wav'),
                   "Item": pygame.mixer.Sound('sounds/Item.wav'),
                   "Die": pygame.mixer.Sound('sounds/Die.wav'),
                   "Game Over": pygame.mixer.Sound('sounds/Game Over.wav'),
                   "Fireball": pygame.mixer.Sound('sounds/Fire Ball.wav'),
                   "Squish": pygame.mixer.Sound('sounds/Squish.wav'),
                   "Kick": pygame.mixer.Sound('sounds/Kick.wav'),
                   "1UP": pygame.mixer.Sound('sounds/1up.wav'),
                   "Skid": pygame.mixer.Sound('sounds/Skid.wav'),
                   "Flagpole": pygame.mixer.Sound('sounds/Flagpole.wav'),
                   "Warppipe": pygame.mixer.Sound('sounds/Warp.wav')}
    channel1 = pygame.mixer.Channel(1)

    camera = Camera(settings)
    hud = HUD(settings, screen, item_spritesheet, font)
    startmenu = StartMenu(settings, screen, title_spritesheet, font)
    mario = Mario(settings, screen, mario_spritesheet, warp)
    mario_group = Group()
    mario_group.add(mario)
    background = Group()
    foreground = Group()
    blocks = Group()
    hidden_blocks = Group()
    coins = Group()
    block_contents = Group()
    flagpole = Group()
    flag = Flag(settings, screen, item_spritesheet.image_at((128, 32, 16, 16), settings.scale["tile_width"],
                                                            settings.scale["tile_height"],
                                                            colorkey=settings.bg_color[0]))
    enemies = Group()
    switched = False
    points = Group()
    level_1_1 = Map(settings, screen, "level_maps/1-1 Overworld.txt", tilesets[0], camera)
    level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins, enemies, enemy_sprites,
                             mario, False)

    timer = pygame.time.Clock()
    time = 1

    while True:
        timer.tick(60)
        time += 1
        if time == 61:
            time = 1

        check_events(mario, startmenu, game_sounds, channel1)
        mario.update(mario_group, foreground, blocks, hidden_blocks, enemies, points, hud, font, block_contents,
                     block_content_sprites, camera, game_sounds, channel1)
        for enemy in enemies:
            enemy.update()
        camera.camera_tracking(mario)
        if settings.current_level == "overworld":
            level_1_1.sprite_cycler(camera, background, foreground, blocks, hidden_blocks, coins, block_contents,
                                enemies, enemy_sprites, flagpole, flag, points, points_font)
        camera.update_screen(screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks, coins, mario,
                             block_contents, enemies, flagpole, points, flag)
        if startmenu.playgame_select:
            while startmenu.playgame_select:

                pygame.mixer.music.play()
                reset_sprites(background, foreground, blocks, hidden_blocks, coins, block_contents, enemies, flagpole,
                              points)
                level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins, enemies,
                                         enemy_sprites, mario, False)
                camera.lives_screen = True
                camera.global_frame = 0
                camera.update_screen(screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks, coins,
                                     mario, block_contents, enemies, flagpole, points, flag)

                hud.countdown = 400
                while not camera.lives_screen and startmenu.playgame_select:
                    timer.tick(60)
                    time += 1
                    if time == 61:
                        time = 1
                    check_events(mario, startmenu, game_sounds, channel1)
                    if time % 60 == 0:
                        hud.countdown -= 1

                    mario.update(mario_group, foreground, blocks, hidden_blocks, enemies, points, hud, points_font,
                                 block_contents, block_content_sprites, camera, game_sounds, channel1)

                    for enemy in enemies:
                        enemy.update()
                    camera.camera_tracking(mario)
                    if settings.current_level == "overworld":
                        if switched is True:
                            if first:
                                mario.jump_active = True
                                mario.rect.x = 7947
                                mario.rect.y = 450
                                mario.floor = mario.rect.y
                                first = False
                            camera.rect.x = mario.rect.x - 200
                            level_1_1 = Map(settings, screen, "level_maps/1-1 Overworld.txt", tilesets[0], camera)
                            level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins,
                                                     enemies, enemy_sprites, mario, True)

                    elif settings.current_level == "underworld":
                        if not switched:
                            camera = Camera(settings)
                            mario.rect.x = 80
                            mario.rect.y = 100
                            level_1_1 = Map(settings, screen, "level_maps/1-1 Underworld.txt", tilesets[0], camera)
                            level_1_1.sprite_cycler(camera, background, foreground, blocks, hidden_blocks, coins,
                                            block_contents, enemies, enemy_sprites, flagpole, flag, points,
                                            points_font)
                            level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins, enemies,
                                                     enemy_sprites,
                                                     mario, False)
                            switched = True
                            first = True

                    level_1_1.sprite_cycler(camera, background, foreground, blocks, hidden_blocks, coins,
                                            block_contents, enemies, enemy_sprites, flagpole, flag, points,
                                            points_font)

                    camera.update_screen(screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks,
                                         coins, mario, block_contents, enemies, flagpole, points, flag)
            reset_sprites(background, foreground, blocks, hidden_blocks, coins, block_contents, enemies, flagpole,
                          points)
            level_1_1.initialize_map(camera, background, foreground, blocks, hidden_blocks, coins, enemies,
                                     enemy_sprites, mario)
            channel1.play(game_sounds["Game Over"])

            camera.update_screen(screen, time, hud, startmenu, background, foreground, blocks, hidden_blocks, coins,
                                 mario, block_contents, enemies, flagpole, points, flag)
            for x in range(0, len(startmenu.high_score_list)):
                if hud.score > startmenu.high_score_list[x]:
                    startmenu.high_score_list.insert(x, hud.score)
                    startmenu.high_score_list.pop()
                    break
            high_score_file = open("High_Scores.txt", "w")
            for x in range(0, len(startmenu.high_score_list) - 1):
                high_score_file.write(str(startmenu.high_score_list[x]) + "\n")
            high_score_file.write(str(startmenu.high_score_list[8]))
            high_score_file.close()
            hud.reset()


def check_events(mario, startmenu, game_sounds, channel1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                mario.check_underworld()
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
                    mario.jump(game_sounds, channel1)
                elif not startmenu.selection:
                    if not startmenu.highscore_select:
                        startmenu.highscore_select = True
                    else:
                        startmenu.highscore_select = False
                else:
                    startmenu.playgame_select = True
            if event.key == pygame.K_UP and not startmenu.selection and not startmenu.highscore_select:
                startmenu.selection = True
                channel1.play(game_sounds["Beep"])
            if event.key == pygame.K_DOWN:
                if startmenu.playgame_select:
                    # mario crouch
                    placeholder = "placeholder"
                elif startmenu.selection:
                    startmenu.selection = False
                    channel1.play(game_sounds["Beep"])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if startmenu.playgame_select:
                    mario.change_sprite_image_direction('still')
                    mario.right_key_down = False
            if event.key == pygame.K_LEFT:
                if startmenu.playgame_select:
                    mario.change_sprite_image_direction('still')
                    mario.left_key_down = False


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
    score_image_rects = ((0, 168, 4, 8), (4, 168, 4, 8), (8, 168, 4, 8), (12, 168, 4, 8), (16, 168, 4, 8),
                         (20, 168, 4, 8))
    block_content_sprites.append(item_spritesheet.images_at(coin_image_rects, settings.scale["tile_width"],
                                                            settings.scale["tile_height"],
                                                            colorkey=settings.bg_color[0]))
    block_content_sprites.append(item_spritesheet.images_at(brick_image_rects, settings.scale["tile_width"]/4,
                                                            settings.scale["tile_height"]/4,
                                                            colorkey=settings.bg_color[0]))
    score_sprites = item_spritesheet.images_at(score_image_rects, settings.scale["pixel_width"] * 4,
                                               settings.scale["pixel_height"] * 8, colorkey=settings.bg_color[0])
    score_sprites.append(item_spritesheet.image_at((32, 168, 16, 8), settings.scale["tile_width"],
                                                   settings.scale["pixel_height"] * 8, colorkey=settings.bg_color[0]))

    return {"0": score_sprites[0], "1": score_sprites[1], "2": score_sprites[2], "4": score_sprites[3],
            "5": score_sprites[4], "8": score_sprites[5], "1UP": score_sprites[6]}


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


def reset_sprites(background, foreground, blocks, hidden_blocks, coins, block_contents, enemies, flagpole, points):
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
    for sprite in points:
        sprite.kill()


run_game()
