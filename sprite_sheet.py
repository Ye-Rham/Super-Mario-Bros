import pygame
from pygame.transform import scale
# https://www.pygame.org/wiki/Spritesheet


class SpriteSheet(object):
    def __init__(self, filename, screen):
        self.sheet = pygame.image.load(filename).convert()
        self.screen = screen

    def image_at(self, rectangle, scalewidth, scaleheight, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image = pygame.Surface.convert(image)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image = scale(image, (int(scalewidth), int(scaleheight)))
        return image

    def images_at(self, rects, scalewidth, scaleheight, colorkey=None):
        return [self.image_at(rect, scalewidth, scaleheight, colorkey) for rect in rects]
