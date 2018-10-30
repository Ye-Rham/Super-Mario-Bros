import pygame
import time

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Super Mario Bros")

    while True:
        time.sleep(10)

run_game()