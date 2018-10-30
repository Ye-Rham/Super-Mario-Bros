import pygame
import sys
from mario import Mario


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Super Mario Bros")

    mario = Mario(screen)

    while True:
        screen.fill((0, 0, 0))

        check_events(mario)
        mario.update()
        mario.blitme()

        pygame.display.flip()


def check_events(mario):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mario.change_direction('right')
            if event.key == pygame.K_LEFT:
                mario.change_direction('left')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                mario.change_direction('still')
            if event.key == pygame.K_LEFT:
                mario.change_direction('still')


run_game()